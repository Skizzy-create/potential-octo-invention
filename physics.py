# physics.py
import random
import pygame


def resolve_circle_collision(a, b, restitution=0.95):
    """
    Resolve collision between two circle-like sprites a and b.
    Each must have .position (Vector2), .velocity (Vector2), and .radius (number).
    Mass is proportional to radius**2.
    restitution: 1.0 = elastic, <1 = partly inelastic.
    """

    # vector from b -> a
    pos_diff = a.position - b.position
    dist = pos_diff.length()

    # avoid div-by-zero if centers coincide
    if dist == 0:
        pos_diff = pygame.Vector2(
            random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)
        )
        dist = pos_diff.length()
        if dist == 0:
            return  # can't resolve sensibly

    normal = pos_diff / dist

    # relative velocity along normal
    rv = a.velocity - b.velocity
    vel_along_normal = rv.dot(normal)

    # if velocities are separating, do nothing
    if vel_along_normal >= 0:
        return

    # masses (use area ~ r^2)
    m1 = max(a.radius * a.radius, 1e-6)
    m2 = max(b.radius * b.radius, 1e-6)
    inv_m1 = 1.0 / m1
    inv_m2 = 1.0 / m2

    # impulse scalar for 1D along normal (derived from conservation of momentum)
    j = -(1 + restitution) * vel_along_normal
    j = j / (inv_m1 + inv_m2)

    impulse = normal * j

    # apply impulse (note lighter objects change velocity more)
    a.velocity += impulse * inv_m1
    b.velocity -= impulse * inv_m2

    # positional correction — separate overlapping circles to avoid sinking.
    penetration = (a.radius + b.radius) - dist
    if penetration > 0:
        # constants: percent of penetration to correct, slop to allow tiny overlaps
        percent = 0.8
        slop = 0.01
        correction_mag = max(penetration - slop, 0.0) / (inv_m1 + inv_m2) * percent
        correction = normal * correction_mag
        a.position += correction * inv_m1
        b.position -= correction * inv_m2
