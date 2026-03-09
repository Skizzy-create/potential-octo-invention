# Chapter 02 — Player Acceleration

## Goal

The ship currently moves at a fixed speed the moment you press **W** — it goes
from zero to `SKIZZY_SPEED` instantly. Real spacecraft (and the original
Asteroids) use **thrust**: holding W gradually builds up speed, and releasing it
lets the ship coast. Your job is to add acceleration-based movement to the
player.

---

## Background

Look at `player.py`. The `move` method currently sets velocity implicitly by
adding a fixed displacement every frame:

```python
def move(self, dt):
    unit_vector = pygame.Vector2(0, 1)
    rotated_vector = unit_vector.rotate(self.rotation)
    rotated_with_speed_vector = rotated_vector * SKIZZY_SPEED * dt
    self.position += rotated_with_speed_vector
```

It adds a position delta directly instead of updating a persistent velocity.
For acceleration you need the ship to have a **velocity** that changes gradually,
and a **maximum speed** cap to prevent it from flying off infinitely.

The `CircleShape` base class already gives every object a `self.velocity`
attribute (`pygame.Vector2`).

---

## What to Build

Replace the immediate-movement model with a thrust-and-coast model:

1. **Thrust** — holding **W** adds acceleration in the direction the ship is
   facing each frame, increasing `self.velocity`.
2. **Reverse thrust** — holding **S** applies thrust in the opposite direction
   (braking / reversing).
3. **Coasting** — when no key is held the ship drifts at its current velocity.
4. **Speed cap** — clamp `self.velocity` to a maximum magnitude so the ship
   cannot accelerate without limit.
5. **Movement** — update `self.position` using `self.velocity` each frame
   (instead of adding a direct displacement).

---

## New Constants to Add

Add the following to `constants.py` (choose sensible values and tune them):

```
PLAYER_ACCELERATION   # units per second², how fast thrust builds speed
PLAYER_MAX_SPEED      # maximum velocity magnitude the ship can reach
```

You may also want a friction/drag constant if you want the ship to slow down
naturally when no key is pressed (optional but recommended for feel):

```
PLAYER_DRAG           # fraction of velocity kept each frame (e.g. 0.98)
```

---

## Constraints

- Do **not** delete `SKIZZY_SPEED` from `constants.py` until you are sure
  nothing else references it — search the codebase first.
- The ship's position must be updated via `self.velocity`, not via a direct
  displacement add.
- Shooting direction should still depend on `self.rotation`, not velocity —
  the ship can fire in the direction it's pointing even while coasting sideways.

---

## Hints

<details>
<summary>Hint 1 — Updating velocity with thrust</summary>

Each frame that **W** is held:

```python
thrust_direction = pygame.Vector2(0, 1).rotate(self.rotation)
self.velocity += thrust_direction * PLAYER_ACCELERATION * dt
```

Then clamp:

```python
if self.velocity.length() > PLAYER_MAX_SPEED:
    self.velocity.scale_to_length(PLAYER_MAX_SPEED)
```

</details>

<details>
<summary>Hint 2 — Applying velocity to position</summary>

In `update`, after handling input, move the ship:

```python
self.position += self.velocity * dt
```

</details>

<details>
<summary>Hint 3 — Optional drag</summary>

Apply a drag multiplier every frame to let the ship slow down naturally:

```python
self.velocity *= PLAYER_DRAG
```

A value like `0.99` gives a very gradual slowdown; `0.95` slows more
noticeably.

</details>

---

## Files to Modify

- `constants.py` — add `PLAYER_ACCELERATION`, `PLAYER_MAX_SPEED`, and
  optionally `PLAYER_DRAG`.
- `player.py` — rewrite `move()` and update the `update()` method to apply
  velocity-based movement.

---

## Definition of Done

- [ ] Holding **W** gradually builds the ship's speed (you can feel the
  acceleration).
- [ ] Releasing **W** lets the ship coast at its current speed.
- [ ] Holding **S** decelerates or reverses the ship.
- [ ] The ship's speed never exceeds `PLAYER_MAX_SPEED`.
- [ ] The ship's position is updated through `self.velocity`, not a direct
  displacement.
- [ ] Shooting still works correctly, firing in the direction the ship faces.
- [ ] The game runs without errors.
