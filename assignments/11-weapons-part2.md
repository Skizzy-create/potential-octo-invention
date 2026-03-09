# Chapter 11 — Weapon Types, Part 2: Bombs

## Goal

Add **bombs** to the weapon roster. A bomb is dropped at the ship's current
position and detonates after a short fuse, creating a large explosion that
destroys any asteroids within its blast radius.

---

## Background

You built spread shot and rapid fire in Chapter 10. Bombs are a fundamentally
different weapon: they are stationary (or slow-moving), time-delayed, and
affect an area — not a single point.

This chapter requires:
- A new `Bomb` sprite class.
- A blast-radius collision check in `main.py`.
- Integration with the particle system from Chapter 07 (optional but highly
  recommended for visual feedback).

---

## What to Build

### Part A — Bomb Class

Create a new file `bomb.py` containing a `Bomb` class that:

1. Spawns at the player's current position with no initial velocity (or the
   player's current velocity if you implemented Chapter 02's acceleration).
2. Has a `fuse_timer` that counts down each frame.
3. Draws itself as a small pulsing circle (or any distinctive visual).
4. When `fuse_timer` reaches 0, **detonates**: destroys all asteroids within
   `BOMB_BLAST_RADIUS` of its centre, then calls `self.kill()`.

### Part B — Add Bomb to Weapon Cycle

5. Add `"bomb"` to the weapon list in `Player` (from Chapter 10).
6. Dropping a bomb calls a new `drop_bomb()` method (or reuses `shoot()`
   dispatch logic).
7. Give bombs a long cooldown — the player shouldn't be able to spam them.

### Part C — Blast Collision

8. In `main.py` (or inside `Bomb.detonate()`), iterate over all live asteroids
   and split any that are within `BOMB_BLAST_RADIUS` of the bomb's position.
9. Trigger an explosion particle effect at the bomb's position on detonation
   (see Chapter 07).

---

## New Constants to Add

```python
# constants.py
BOMB_BLAST_RADIUS    = 200     # pixels — area of effect
BOMB_FUSE_SECONDS    = 2.0     # seconds before detonation
BOMB_COOLDOWN_SECONDS = 5.0   # seconds before player can drop another
BOMB_RADIUS          = 8      # visual radius of the bomb sprite
```

---

## Constraints

- A bomb must not destroy asteroids the moment it is dropped — the fuse must
  expire first.
- The bomb's blast must split asteroids (call `asteroid.split()`), not just
  kill them outright — preserve the split mechanic.
- Bombs should be added to `updatable` and `drawable` sprite groups.
- The bomb must **not** be destroyed by shots — shots only affect asteroids.
- If the player is within the blast radius of their own bomb when it detonates,
  they should lose a life (this is dangerous gameplay and optional but
  recommended for fun).

---

## Hints

<details>
<summary>Hint 1 — Bomb class skeleton</summary>

```python
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.fuse_timer = BOMB_FUSE_SECONDS

    def update(self, dt):
        self.fuse_timer -= dt
        if self.fuse_timer <= 0:
            self.detonate()

    def detonate(self):
        # Blast logic goes here — see Hint 2
        self.kill()

    def draw(self, screen):
        # Draw a pulsing circle
        pulse = abs(math.sin(self.fuse_timer * math.pi * 4)) * 4
        pygame.draw.circle(screen, "red", (int(self.position.x),
                           int(self.position.y)), int(BOMB_RADIUS + pulse), 2)
```

</details>

<details>
<summary>Hint 2 — Blast logic and group access</summary>

`Bomb.detonate()` needs to iterate over live asteroids. You can pass the
`asteroids` sprite group into `Bomb.__init__` and store it, or handle the blast
check in `main.py` by listening for a bomb event.

The cleanest approach is to store a reference to the `asteroids` group:

```python
def __init__(self, x, y, asteroids_group):
    ...
    self._asteroids = asteroids_group

def detonate(self):
    for asteroid in list(self._asteroids):
        if asteroid.position.distance_to(self.position) < BOMB_BLAST_RADIUS:
            asteroid.split()
    self.kill()
```

</details>

<details>
<summary>Hint 3 — Pulsing visual</summary>

Use `math.sin` driven by `self.fuse_timer` to make the bomb pulse in size or
brightness. As the timer counts down the pulses speed up, giving a visual cue
that detonation is imminent.

</details>

<details>
<summary>Hint 4 — Integrating with Chapter 10's weapon cycle</summary>

The cleanest approach is to keep all firing logic inside `Player`. Add a
`drop_bomb()` method on `Player` that accepts the `asteroids` group (or stores
a reference to it set during group wiring in `main.py`):

```python
# In Player.shoot(), add a branch:
elif self.weapon == "bomb":
    Bomb(self.position.x, self.position.y, self._asteroids)
    self.coolDown = BOMB_COOLDOWN_SECONDS
```

Wire the reference once in `main.py`, before the game loop:

```python
Skizzy._asteroids = asteroids   # give the player access to the group
```

This keeps `main.py` free of per-weapon branching and the firing path remains
consistent through `Player.shoot()`.

</details>

---

## Files to Create / Modify

- **`bomb.py`** (new) — `Bomb` class.
- `player.py` — add `"bomb"` to weapon list, handle drop logic.
- `main.py` — wire `Bomb.containers`; pass asteroids group; optionally handle
  friendly-fire blast on player.
- `constants.py` — add bomb constants.

---

## Definition of Done

- [ ] Selecting the bomb weapon and pressing Space drops a bomb at the ship's
  position.
- [ ] The bomb has a visible fuse countdown (pulsing visual or shrinking
  circle).
- [ ] After `BOMB_FUSE_SECONDS`, the bomb detonates.
- [ ] All asteroids within `BOMB_BLAST_RADIUS` are split on detonation.
- [ ] An explosion effect plays at the detonation point (Chapter 07
  integration).
- [ ] Bombs have a long cooldown — they cannot be spammed.
- [ ] The game runs without errors.
