# Chapter 12 — Power-up: Shield

## Goal

Add a **shield power-up** that spawns on screen, can be collected by the
player, and temporarily makes the player invulnerable to asteroid hits.

---

## Background

Power-ups are a new category of game object: they sit in the world, waiting to
be picked up by the player. When the player's hitbox overlaps the power-up, it
activates its effect and disappears.

You will build a general pattern here that can be reused for the speed power-up
in Chapter 13.

---

## What to Build

### Part A — Shield Power-up Class

Create a new file `powerup.py` containing a `ShieldPowerUp` class:

1. Spawns at a random position on screen (but not too close to the screen
   edges).
2. Draws itself as a distinctive shape (e.g. a blue circle with an inner ring,
   or a blue hexagon).
3. Has a lifetime — despawns after `POWERUP_LIFETIME` seconds if not collected.
4. Slowly rotates or pulses to attract the player's attention.

### Part B — Spawning Power-ups

5. In `main.py` (or in a new manager), spawn a shield power-up at random
   intervals (e.g. every `POWERUP_SPAWN_INTERVAL` seconds).
6. Limit the number of power-ups on screen at one time (suggested maximum: 2).

### Part C — Collection & Effect

7. Each frame in `main.py`, check whether the player overlaps a shield
   power-up (use `player.collides_with(powerup)` — the circular hitbox is
   fine here).
8. On collection:
   - Kill the power-up sprite.
   - Activate the shield on the player for `SHIELD_DURATION` seconds.
9. While shielded, the player is **immune to asteroid collisions** — hits are
   absorbed without losing a life.

### Part D — Shield Visual

10. While the shield is active, draw a translucent blue circle around the ship.
11. Flash or shrink the circle as the shield is about to expire.

---

## New Constants to Add

```python
# constants.py
POWERUP_SPAWN_INTERVAL  = 15.0    # seconds between power-up spawns
POWERUP_LIFETIME        = 10.0    # seconds before a power-up despawns
POWERUP_RADIUS          = 15      # collision radius for pick-up
SHIELD_DURATION         = 5.0     # seconds the shield lasts after pick-up
MAX_POWERUPS_ON_SCREEN  = 2
```

---

## Constraints

- Power-ups must use the sprite group system (`updatable`, `drawable`).
- The shield timer lives on the `Player` object, not in `main.py`.
- While shielded, the player should still be able to take hits visually (the
  asteroid should still bounce), but no life should be lost.
- If the player picks up a shield while already shielded, the duration should
  **reset** (not stack infinitely).
- Do **not** make power-ups collide with asteroids — they should be transparent
  to asteroid physics.

---

## Hints

<details>
<summary>Hint 1 — Power-up base pattern</summary>

```python
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.lifetime = POWERUP_LIFETIME
        self.angle = 0.0

    def update(self, dt):
        self.lifetime -= dt
        self.angle += 90 * dt  # rotate 90 degrees per second
        if self.lifetime <= 0:
            self.kill()
```

Subclass this for `ShieldPowerUp` with a custom `draw()`.

</details>

<details>
<summary>Hint 2 — Drawing the shield on the player</summary>

In `Player.draw()`, after drawing the triangle, check if the shield is active:

```python
if self.shield_timer > 0:
    alpha = 128 if int(self.shield_timer * 4) % 2 == 0 else 64
    # pygame.draw.circle doesn't support alpha directly on the main surface.
    # Use a temporary surface:
    shield_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
    pygame.draw.circle(
        shield_surf, (0, 100, 255, alpha),
        (self.radius * 2, self.radius * 2),
        int(self.radius * 1.5), 3
    )
    screen.blit(shield_surf, (self.position.x - self.radius * 2,
                              self.position.y - self.radius * 2))
```

</details>

<details>
<summary>Hint 3 — Spawning at safe positions</summary>

Avoid spawning power-ups right on top of the player:

```python
import random
margin = 100
x = random.randint(margin, SCREEN_WIDTH - margin)
y = random.randint(margin, SCREEN_HEIGHT - margin)
```

You may also want to skip spawning if the random position is too close to the
player's current position.

</details>

<details>
<summary>Hint 4 — Checking collection in main.py</summary>

Add a `powerups` sprite group. Each frame:

```python
for powerup in list(powerups):
    if Skizzy.collides_with(powerup):   # Skizzy is the Player instance in main.py
        Skizzy.activate_shield()
        powerup.kill()
```

</details>

---

## Files to Create / Modify

- **`powerup.py`** (new) — `PowerUp` base class and `ShieldPowerUp`.
- `player.py` — add `shield_timer`, `activate_shield()`, and shield visual in
  `draw()`.
- `main.py` — add `powerups` group; wire containers; spawn at intervals; check
  collection; skip damage when shield active.
- `constants.py` — add power-up and shield constants.

---

## Definition of Done

- [ ] Shield power-ups spawn at random positions at regular intervals.
- [ ] A maximum of `MAX_POWERUPS_ON_SCREEN` power-ups exist at any time.
- [ ] Power-ups despawn automatically if not collected.
- [ ] Flying into a shield power-up activates the shield.
- [ ] While shielded, asteroid hits do not cost a life.
- [ ] A visible shield effect renders around the ship while active.
- [ ] The shield flashes when about to expire.
- [ ] Collecting a shield while already shielded resets the timer.
- [ ] The game runs without errors.
