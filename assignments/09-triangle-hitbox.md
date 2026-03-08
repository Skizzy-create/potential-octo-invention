# Chapter 09 — Triangular Ship Hitbox

## Goal

The ship is currently drawn as a triangle (via `Player.triangle()`) but its
collision detection uses a **circle** (inherited from `CircleShape`). This
means the game treats the ship as if it were a round blob, not a pointy
triangle. Your job is to replace the circular hitbox with a proper
**triangle-based collision test**.

---

## Background

`circleshape.py` provides:

```python
def collides_with(self, other):
    distance_between = self.position.distance_to(other.position)
    return distance_between <= self.radius + other.radius
```

This is fast but inaccurate for the ship. You want the ship to collide with an
asteroid only when the asteroid's circle **intersects the triangle** that is
already computed by `Player.triangle()`.

Asteroids and shots will still use circle–circle tests. Only the player
needs a custom hitbox.

---

## What to Build

Override `collides_with` on the `Player` class so that, when the other object
is an asteroid (or any circle), it performs a **circle vs. triangle** test
instead of a circle vs. circle test.

---

## The Maths (Point of Understanding)

A circle with centre **C** and radius **r** intersects a triangle **ABC** if:

1. **C** is inside the triangle, **OR**
2. The circle intersects any of the three edges of the triangle.

Edge-circle intersection: The circle intersects a line segment if the distance
from **C** to the closest point on the segment is less than **r**.

You do not need to derive this from scratch — pygame has helpers, and the hints
below walk you through the approach.

---

## Constraints

- Only `Player.collides_with` should change — do not alter `CircleShape`,
  `Asteroid`, or `Shot`.
- The `triangle()` method already exists on `Player` and returns the three
  vertices. Use it — do not duplicate the vertex calculation.
- The change must be backward-compatible: if `collides_with` is called with
  another player-like object (unlikely but possible), it should fall back to the
  circle test.

---

## Hints

<details>
<summary>Hint 1 — Checking if a point is inside a triangle</summary>

Use the sign of the cross product for each edge. If the point is on the same
side of all three edges (consistently positive or negative cross products), it
is inside:

```python
def _point_in_triangle(p, a, b, c):
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
    d1, d2, d3 = sign(p, a, b), sign(p, b, c), sign(p, c, a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)
```

</details>

<details>
<summary>Hint 2 — Closest point on a line segment to a circle centre</summary>

```python
def _closest_point_on_segment(p, a, b):
    ab = b - a
    ap = p - a
    t = ap.dot(ab) / ab.dot(ab)
    t = max(0.0, min(1.0, t))
    return a + ab * t
```

The circle intersects segment AB if
`_closest_point_on_segment(centre, a, b).distance_to(centre) < radius`.

</details>

<details>
<summary>Hint 3 — Putting it together in Player.collides_with</summary>

```python
def collides_with(self, other):
    verts = self.triangle()
    a, b, c = pygame.Vector2(verts[0]), pygame.Vector2(verts[1]), pygame.Vector2(verts[2])
    centre = other.position
    r = other.radius

    # Case 1: circle centre inside triangle
    if _point_in_triangle(centre, a, b, c):
        return True

    # Case 2: circle intersects any edge
    for p1, p2 in [(a, b), (b, c), (c, a)]:
        if _closest_point_on_segment(centre, p1, p2).distance_to(centre) < r:
            return True

    return False
```

Put the helper functions `_point_in_triangle` and `_closest_point_on_segment`
as module-level functions in `player.py` (or in a separate `geometry.py`).

</details>

---

## Files to Modify

- `player.py` — override `collides_with`; add geometry helper functions.
- *(Optional)* `geometry.py` (new) — extract helper functions here if you want
  to keep `player.py` clean and make helpers testable.

---

## Definition of Done

- [ ] Player–asteroid collisions use triangle vs. circle detection, not
  circle vs. circle.
- [ ] The player can fly the ship's nose close to an asteroid without dying,
  but contact with the ship body triggers a hit.
- [ ] Shot collisions with asteroids are unaffected (still circle vs. circle).
- [ ] The original `CircleShape.collides_with` is unchanged.
- [ ] The game runs without errors.
