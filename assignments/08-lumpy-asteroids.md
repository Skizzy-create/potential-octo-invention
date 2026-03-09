# Chapter 08 — Lumpy Asteroid Shapes

## Goal

Every asteroid is currently a perfect circle drawn with `pygame.draw.circle`.
Real asteroids are jagged and irregular. In this chapter you will make
asteroids appear **lumpy** by generating a randomised polygon for each one
instead of drawing a circle.

---

## Background

In `asteroid.py`, the `draw` method is:

```python
def draw(self, screen):
    pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
```

To make a lumpy shape you'll instead compute a polygon whose vertices sit at
random distances from the centre — sometimes closer, sometimes further than
`self.radius`. Crucially, the **collision radius** stays the same; only the
visual changes (you can update the hitbox in Chapter 09 if you want accurate
asteroid geometry, but that is a separate concern).

---

## What to Build

### Part A — Generate the Lumpy Shape

1. In `Asteroid.__init__`, generate a list of random "offsets" — one per
   vertex around the circle.
2. Store this list on `self` so the shape stays consistent each frame (do not
   re-randomise every draw call).
3. Use `NUM_ASTEROID_VERTICES` equally-spaced angles around the circle, then
   vary each vertex's distance from the centre by a random factor within a
   configurable range.

### Part B — Draw the Polygon

4. In `Asteroid.draw`, compute the world-space vertex positions from the stored
   offsets and the current `self.position`.
5. Draw the polygon with `pygame.draw.polygon`.

### Part C — Preserve on Split

6. When an asteroid splits, its children are new `Asteroid` objects — they
   will automatically get their own random shapes. No extra work needed here,
   but verify this is the case.

---

## New Constants to Add

```python
# constants.py
NUM_ASTEROID_VERTICES  = 10     # how many points the polygon has
ASTEROID_LUMP_MIN      = 0.7    # minimum radius multiplier per vertex
ASTEROID_LUMP_MAX      = 1.3    # maximum radius multiplier per vertex
```

The multipliers control how lumpy the asteroid looks. A range of `[1.0, 1.0]`
would give a circle; `[0.5, 1.5]` would give very spiky shapes.

---

## Constraints

- The **collision radius** (`self.radius`) must **not** change — the circular
  collision detection in `circleshape.py` must continue to work.
- The shape must be generated **once** in `__init__`, not re-randomised every
  frame.
- The polygon must rotate when the asteroid changes direction — you should
  either track a rotation angle or use a fixed set of offsets that you rotate
  by the asteroid's velocity direction. See Hint 2.

---

## Hints

<details>
<summary>Hint 1 — Generating random offsets</summary>

```python
import math, random

self._offsets = []
for i in range(NUM_ASTEROID_VERTICES):
    angle = (2 * math.pi / NUM_ASTEROID_VERTICES) * i
    distance = self.radius * random.uniform(ASTEROID_LUMP_MIN, ASTEROID_LUMP_MAX)
    self._offsets.append((angle, distance))
```

</details>

<details>
<summary>Hint 2 — Drawing the polygon</summary>

In `draw()`, convert each (angle, distance) pair to world coordinates:

```python
def draw(self, screen):
    points = []
    for angle, distance in self._offsets:
        x = self.position.x + math.cos(angle) * distance
        y = self.position.y + math.sin(angle) * distance
        points.append((x, y))
    pygame.draw.polygon(screen, "white", points, LINE_WIDTH)
```

To make the shape appear to tumble, add a `self.rotation_angle` that
increments each frame (in `update`), and add it to each angle in `draw`.

</details>

<details>
<summary>Hint 3 — Tumbling rotation</summary>

Add to `Asteroid.__init__`:

```python
self.rotation_angle = 0.0
self.rotation_speed = random.uniform(-90, 90)  # degrees per second
```

In `Asteroid.update()`:

```python
self.rotation_angle += self.rotation_speed * dt
```

In `Asteroid.draw()`:

```python
angle_rad = math.radians(angle_deg + self.rotation_angle)
```

</details>

---

## Files to Modify

- `asteroid.py` — update `__init__` to generate offsets; update `draw` to
  render a polygon; optionally add tumbling rotation.
- `constants.py` — add `NUM_ASTEROID_VERTICES`, `ASTEROID_LUMP_MIN`,
  `ASTEROID_LUMP_MAX`.

---

## Definition of Done

- [ ] Asteroids are drawn as randomised lumpy polygons, not circles.
- [ ] Each asteroid has a unique shape generated at spawn time.
- [ ] The shape does not change between frames (no re-randomisation per draw).
- [ ] (Bonus) Asteroids visually rotate/tumble as they move.
- [ ] Circular collision detection still works correctly.
- [ ] Child asteroids from splits also have lumpy shapes.
- [ ] The game runs without errors.
