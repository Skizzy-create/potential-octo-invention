# Chapter 07 — Explosion Effect

## Goal

Asteroids currently disappear silently when shot. Add a **particle explosion
effect** that plays when an asteroid is destroyed, making hits feel satisfying
and visually rewarding.

---

## Background

pygame has no built-in particle system, so you'll build a simple one yourself.
An explosion is just a collection of small objects (particles) that:
- Spawn at the asteroid's position when it is destroyed.
- Move outward in random directions.
- Fade out or shrink over time.
- Disappear after a short duration.

Particles need to be updated and drawn each frame, just like any other game
object. The cleanest approach is to make them proper pygame sprites added to the
`updatable` and `drawable` groups.

---

## What to Build

### Part A — Particle Class

Create a new file `particle.py` containing an `Explosion` (or `Particle`) class:

1. On creation, accept a position and a radius (of the destroyed asteroid — use
   it to scale the number and size of particles).
2. Spawn several child particles at that position, each with a random outward
   velocity.
3. Each particle has a lifetime. Each frame, decrement its lifetime and
   update its position. When lifetime reaches 0, call `self.kill()`.
4. Draw each particle as a small circle or line segment.

### Part B — Trigger on Asteroid Destruction

5. In `main.py`, when a shot hits an asteroid, create an `Explosion` at
   `asteroid.position` before (or after) calling `asteroid.split()`.

---

## New Constants to Add

```python
# constants.py
EXPLOSION_PARTICLE_COUNT  = 12    # particles per explosion
EXPLOSION_PARTICLE_SPEED  = 150   # max speed of a particle (units/s)
EXPLOSION_PARTICLE_LIFE   = 0.6   # seconds a particle lives
EXPLOSION_PARTICLE_RADIUS = 3     # drawn size of each particle
```

Tune these to taste.

---

## Constraints

- Particles must be added to the `updatable` and `drawable` sprite groups so
  the main loop handles them automatically.
- Do **not** manage a manual list of particles in `main.py` — use sprite
  groups.
- Particles must clean themselves up (`self.kill()`) — do not leak objects.
- The explosion should scale visually with the asteroid size: a large asteroid
  should produce more or larger particles than a tiny one.

---

## Hints

<details>
<summary>Hint 1 — Class structure</summary>

```python
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * random.uniform(
            speed * 0.3, speed
        )
        self.lifetime = EXPLOSION_PARTICLE_LIFE

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "orange", (int(self.position.x),
                           int(self.position.y)), EXPLOSION_PARTICLE_RADIUS)
```

</details>

<details>
<summary>Hint 2 — Spawning from an explosion manager</summary>

You can create an `Explosion` class whose `__init__` spawns N `Particle`
objects:

```python
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, asteroid_radius):
        super().__init__()   # not added to groups itself
        count = int(EXPLOSION_PARTICLE_COUNT * (asteroid_radius / ASTEROID_MIN_RADIUS))
        for _ in range(count):
            Particle(x, y, EXPLOSION_PARTICLE_SPEED)
```

Or simply spawn particles directly in `main.py` without a wrapper class.

</details>

<details>
<summary>Hint 3 — Colour variation</summary>

Vary particle colour over its lifetime for a more realistic look. Map lifetime
fraction to a colour from white → yellow → orange → red:

```python
fraction = self.lifetime / EXPLOSION_PARTICLE_LIFE
if fraction > 0.6:
    colour = "white"
elif fraction > 0.3:
    colour = "yellow"
else:
    colour = "orange"
```

</details>

<details>
<summary>Hint 4 — Wiring containers</summary>

In `main.py`, before creating any game objects, wire the containers for
`Particle`:

```python
Particle.containers = (updatable, drawable)
```

</details>

---

## Files to Create / Modify

- **`particle.py`** (new) — `Particle` class (and optionally `Explosion`).
- `main.py` — wire `Particle.containers`; trigger explosion on asteroid hit.
- `constants.py` — add explosion constants.

---

## Definition of Done

- [ ] An explosion of particles appears at the position of every destroyed
  asteroid.
- [ ] Particles move outward in random directions.
- [ ] Particles disappear after their lifetime expires.
- [ ] Larger asteroids produce a more impressive explosion than smaller ones.
- [ ] Particles are managed entirely via sprite groups — no manual list in
  `main.py`.
- [ ] No particle objects leak after they expire.
- [ ] The game runs without errors.
