# Chapter 13 — Power-up: Speed Boost

## Goal

Add a **speed boost power-up** that temporarily increases the player's maximum
speed and acceleration when collected. This chapter reuses the power-up
infrastructure you built in Chapter 12.

---

## Background

You already have:
- A `PowerUp` base class in `powerup.py`.
- A `powerups` sprite group in `main.py`.
- The player acceleration model from Chapter 02 (`PLAYER_MAX_SPEED`,
  `PLAYER_ACCELERATION`).

A speed boost temporarily overrides these constants for the player, then
restores them when the timer expires.

---

## What to Build

### Part A — SpeedPowerUp Class

1. In `powerup.py`, add a `SpeedPowerUp` class that extends `PowerUp`.
2. Draw it distinctively — suggested: a yellow/green lightning-bolt-shaped
   polygon, or a circle with a star inside.
3. Reuse all base-class spawning, lifetime, and update logic.

### Part B — Player Speed Boost

4. Add `speed_boost_timer` to `Player.__init__` (starts at 0).
5. Add `activate_speed_boost()` method that sets the timer to
   `SPEED_BOOST_DURATION`.
6. In `Player.update()`, while `speed_boost_timer > 0`:
   - Apply `PLAYER_BOOST_MAX_SPEED` and `PLAYER_BOOST_ACCELERATION` instead of
     the normal constants.
   - Decrement `speed_boost_timer` each frame.
7. When the timer hits 0, revert to normal speed/acceleration.

### Part C — Spawn & Collection

8. In `main.py`, spawn `SpeedPowerUp` objects alongside shield power-ups (they
   can share the same spawn timer and `MAX_POWERUPS_ON_SCREEN` limit, or have
   their own — your choice).
9. On collection, call `Skizzy.activate_speed_boost()` and kill the power-up.
   (`Skizzy` is the `Player` instance variable name used in `main.py`.)

### Part D — Visual Feedback

10. While the speed boost is active, show a visual indicator (e.g. a different
    colour trail, a small engine glow, or a HUD text label like
    `"BOOST ACTIVE"`).
11. Flash or fade the indicator as the boost is about to expire.

---

## New Constants to Add

```python
# constants.py
SPEED_BOOST_DURATION         = 6.0    # seconds the boost lasts
PLAYER_BOOST_MAX_SPEED       = 800    # boosted max speed (vs normal PLAYER_MAX_SPEED)
PLAYER_BOOST_ACCELERATION    = 600    # boosted acceleration
```

---

## Constraints

- Normal speed constants (`PLAYER_MAX_SPEED`, `PLAYER_ACCELERATION`) must
  **not** be modified — the boost only applies temporarily while the timer is
  active.
- If the player picks up a speed boost while already boosted, the timer resets
  (does not stack).
- The speed boost must not interact with the shield (both can be active
  simultaneously).
- Speed boost state lives entirely on the `Player` object.

---

## Hints

<details>
<summary>Hint 1 — SpeedPowerUp draw method</summary>

A simple lightning-bolt effect using a polygon:

```python
def draw(self, screen):
    cx, cy = int(self.position.x), int(self.position.y)
    r = POWERUP_RADIUS
    # Draw a rotating circle with a zig-zag inset
    pygame.draw.circle(screen, "yellow", (cx, cy), r, 2)
    # Zig-zag arrow pointing up (rotated by self.angle)
    tip = pygame.Vector2(0, -r * 0.8).rotate(self.angle)
    left = pygame.Vector2(-r * 0.3, 0).rotate(self.angle)
    right = pygame.Vector2(r * 0.3, 0).rotate(self.angle)
    base = pygame.Vector2(0, r * 0.5).rotate(self.angle)
    pts = [
        (cx + tip.x, cy + tip.y),
        (cx + left.x, cy + left.y),
        (cx + base.x, cy + base.y),
        (cx + right.x, cy + right.y),
    ]
    pygame.draw.polygon(screen, "yellow", pts)
```

</details>

<details>
<summary>Hint 2 — Applying boost in Player.update()</summary>

```python
if self.speed_boost_timer > 0:
    self.speed_boost_timer -= dt
    max_spd = PLAYER_BOOST_MAX_SPEED
    accel = PLAYER_BOOST_ACCELERATION
else:
    max_spd = PLAYER_MAX_SPEED
    accel = PLAYER_ACCELERATION
```

Use `max_spd` and `accel` in your thrust calculation instead of the raw
constants.

</details>

<details>
<summary>Hint 3 — Engine glow effect</summary>

When boosted, draw a small flame/glow behind the ship's exhaust point. The
exhaust point is the back-centre of the ship — from `Player.triangle()`, the
back edge is between vertices `b` and `c`. Midpoint of b and c is the exhaust:

```python
exhaust = (b + c) / 2
```

Draw a small orange/red circle there, sized proportionally to the remaining
boost time.

</details>

<details>
<summary>Hint 4 — Mixed power-up spawning</summary>

You can spawn either type randomly to keep the player guessing:

```python
import random
PowerUpClass = random.choice([ShieldPowerUp, SpeedPowerUp])
PowerUpClass(x, y)
```

This way a single spawn timer produces varied power-ups.

</details>

---

## Files to Modify

- `powerup.py` — add `SpeedPowerUp` class.
- `player.py` — add `speed_boost_timer`, `activate_speed_boost()`, apply
  boost in `update()`, add visual feedback in `draw()`.
- `main.py` — spawn `SpeedPowerUp`; handle collection; update HUD.
- `constants.py` — add speed-boost constants.

---

## Definition of Done

- [ ] Speed boost power-ups spawn on screen (alongside or instead of shield
  power-ups).
- [ ] Collecting a speed boost visibly accelerates the ship beyond its normal
  top speed.
- [ ] The boost expires after `SPEED_BOOST_DURATION` seconds and normal speed
  is restored.
- [ ] Collecting while already boosted resets the timer (no stacking).
- [ ] A visual indicator (HUD or in-world) shows that the boost is active.
- [ ] The indicator flashes or fades as the boost expires.
- [ ] Shield and speed boost can be simultaneously active without conflicts.
- [ ] The game runs without errors.
