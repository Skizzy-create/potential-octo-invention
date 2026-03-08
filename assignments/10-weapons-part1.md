# Chapter 10 — Weapon Types, Part 1: Spread Shot & Rapid Fire

## Goal

The ship currently fires a single shot at a fixed rate. Expand the weapon
system to support at least **two additional weapon types** that the player can
switch between, making combat more strategic and fun.

In this chapter you will implement:
- **Spread Shot** — fires three shots in a fan pattern simultaneously.
- **Rapid Fire** — fires a single shot but with a much shorter cooldown.

Bombs are covered in Chapter 11.

---

## Background

Shooting happens in `Player.shoot()` in `player.py`. It fires one `Shot` at
`PLAYER_SHOOT_SPEED` in the direction the ship faces, then sets a cooldown.

The cooldown and shot speed live in `constants.py`:
```
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.1
```

You will need a way to track which weapon is currently active and cycle through
weapons with a key press.

---

## What to Build

### Part A — Weapon State

1. Add a `self.weapon` attribute to `Player.__init__` — start with a string
   or enum representing the current weapon (e.g. `"normal"`, `"spread"`,
   `"rapid"`).
2. Add a key binding to cycle weapons (suggested: **Q** or **Tab**).
3. Prevent rapid weapon switching by adding a weapon-switch cooldown.

### Part B — Spread Shot

4. When `weapon == "spread"`, fire **three shots** from a single `shoot()` call:
   - Centre shot: straight ahead.
   - Left shot: rotated `-SPREAD_ANGLE` degrees from centre.
   - Right shot: rotated `+SPREAD_ANGLE` degrees from centre.
5. The spread shot should have a longer cooldown than the normal shot.

### Part C — Rapid Fire

6. When `weapon == "rapid"`, fire a single shot with a **shorter cooldown**
   (`RAPID_COOLDOWN_SECONDS`).

### Part D — HUD Display

7. Display the current weapon name on screen so the player always knows what
   they have equipped.

---

## New Constants to Add

```python
# constants.py
SPREAD_ANGLE            = 20     # degrees between spread shots
SPREAD_COOLDOWN_SECONDS = 0.4    # longer than normal
RAPID_COOLDOWN_SECONDS  = 0.05   # shorter than normal
WEAPON_SWITCH_COOLDOWN  = 0.3    # seconds between weapon switches
```

---

## Constraints

- `Shot` objects created for all weapon types must use the existing `Shot`
  class — do not create separate shot classes yet.
- The normal shot must remain unchanged — this is the default weapon.
- Weapon state lives on the `Player` object, not in `main.py`.
- All shots must be added to the `shots` and `updatable`/`drawable` groups
  (already handled by `Shot.containers`).

---

## Hints

<details>
<summary>Hint 1 — Cycling weapons</summary>

```python
WEAPONS = ["normal", "spread", "rapid"]

# In update():
if keys[pygame.K_q] and self.weapon_switch_cooldown <= 0:
    idx = WEAPONS.index(self.weapon)
    self.weapon = WEAPONS[(idx + 1) % len(WEAPONS)]
    self.weapon_switch_cooldown = WEAPON_SWITCH_COOLDOWN
```

</details>

<details>
<summary>Hint 2 — Firing a spread</summary>

```python
def _fire_shot(self, angle_offset=0):
    shot = Shot(self.position.x, self.position.y)
    velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle_offset)
    velocity *= PLAYER_SHOOT_SPEED
    shot.velocity = velocity

def shoot(self):
    if self.coolDown > 0:
        return
    if self.weapon == "spread":
        self._fire_shot(0)
        self._fire_shot(-SPREAD_ANGLE)
        self._fire_shot(SPREAD_ANGLE)
        self.coolDown = SPREAD_COOLDOWN_SECONDS
    elif self.weapon == "rapid":
        self._fire_shot(0)
        self.coolDown = RAPID_COOLDOWN_SECONDS
    else:
        self._fire_shot(0)
        self.coolDown = PLAYER_SHOOT_COOLDOWN_SECONDS
```

</details>

<details>
<summary>Hint 3 — Displaying the weapon on-screen</summary>

In `main.py`, after drawing the score and lives, render the weapon name:

```python
weapon_surf = font.render(f"Weapon: {Skizzy.weapon}", True, "cyan")
screen.blit(weapon_surf, (20, 80))
```

</details>

---

## Files to Modify

- `constants.py` — add weapon constants.
- `player.py` — add weapon state, cycling logic, and updated `shoot()`.
- `main.py` — add weapon name to HUD.

---

## Definition of Done

- [ ] The player can cycle between at least three weapon types (normal, spread,
  rapid) using a key press.
- [ ] Spread shot fires three shots in a fan pattern.
- [ ] Rapid fire has a noticeably shorter cooldown than normal.
- [ ] Normal shot is unchanged.
- [ ] The current weapon is displayed on-screen.
- [ ] All shots still collide with asteroids correctly.
- [ ] The game runs without errors.
