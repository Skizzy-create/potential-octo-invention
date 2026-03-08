# Chapter 05 — Lives System, Part 2: Respawning

## Goal

You've got lives tracking from Chapter 04. Now make losing a life actually
**respawn** the player at the centre of the screen after a short delay, rather
than letting them keep flying from their current (possibly dangerous) position.

---

## Background

After a hit the player should:
1. Disappear from the screen for a brief respawn delay.
2. Reappear at the screen centre with zero velocity.
3. Be invincible for a short window after reappearing (already partially in
   place from Chapter 04).

The player object is `Skizzy` in `main.py`. It is always alive (never
`kill()`-ed) in the current code. You will need to decide: should you
temporarily remove it from the drawable/updatable groups, or add a visible
flag?

---

## What to Build

### Part A — Respawn State

1. When the player is hit (and lives > 0), put the player into a "dead"
   state for `PLAYER_RESPAWN_DELAY` seconds.
2. During this time the player should **not** be drawn or able to move.
3. Asteroids should not be able to collide with the player while they are
   "dead".

### Part B — Reappearance

4. After the delay, reset the player's position to the screen centre.
5. Set the player's velocity to zero.
6. Begin the invincibility window (from Chapter 04) so the player has time to
   get their bearings.

### Part C — Visual Feedback (optional but recommended)

7. During the invincibility window after respawn, make the player sprite
   **flash** (alternate visible/invisible every few frames) so it is obvious
   to the player that they are temporarily protected.

---

## New Constant to Add

```python
# constants.py
PLAYER_RESPAWN_DELAY = 2.0      # seconds dead before reappearing
```

---

## Constraints

- The player's lives count must not change during the respawn delay — the
  player already lost the life when they were hit.
- If the player has 0 lives and is hit, do not trigger respawn — end the game.
- The game world (asteroids, asteroid spawning) must **continue** during the
  respawn delay — the screen should not freeze.
- Do **not** call `player.kill()` — that removes the sprite from all groups
  permanently. Use a state flag or timer instead.

---

## Hints

<details>
<summary>Hint 1 — State flag approach</summary>

Add `self.is_dead = False` and `self.respawn_timer = 0.0` to `Player.__init__`.

In `Player.update()`:
- If `self.is_dead`, count down `self.respawn_timer`. When it hits 0, respawn.
- If not dead, run normal input handling.

Expose a method `player.die()` that sets `is_dead = True`, resets the timer,
and zeroes velocity. Call it from `main.py` when a collision is detected.

</details>

<details>
<summary>Hint 2 — Hiding the player while dead</summary>

Option A: Skip drawing if dead. In `Player.draw()`, return early if
`self.is_dead`.

Option B: Temporarily remove the player from the `drawable` group and re-add
on respawn. This is cleaner but requires keeping a reference to the group.

Option A is simpler to start with.

</details>

<details>
<summary>Hint 3 — Resetting position on respawn</summary>

You'll need access to the screen centre coordinates. You can import
`SCREEN_WIDTH` and `SCREEN_HEIGHT` from `constants.py` inside `player.py`, or
pass the respawn position as an argument to a `respawn()` method.

```python
def respawn(self, x, y):
    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(0, 0)
    self.is_dead = False
    self.invincible_timer = PLAYER_INVINCIBLE_SECONDS
```

</details>

<details>
<summary>Hint 4 — Flashing during invincibility</summary>

In `Player.draw()`, skip drawing on alternating frames when `invincible_timer >
0`:

```python
if self.invincible_timer > 0:
    # flash: draw only on even multiples of 0.1 s
    if int(self.invincible_timer * 10) % 2 == 0:
        return
```

</details>

---

## Files to Modify

- `constants.py` — add `PLAYER_RESPAWN_DELAY`.
- `player.py` — add `is_dead`, `respawn_timer`, `die()`, and `respawn()`
  logic; modify `draw()` and `update()`.
- `main.py` — call `Skizzy.die()` instead of `sys.exit()` when lives > 0;
  call `Skizzy.respawn()` at the right moment (can be triggered from inside
  `Player.update()` or from `main.py`).

---

## Definition of Done

- [ ] When hit with lives remaining, the player disappears for
  `PLAYER_RESPAWN_DELAY` seconds.
- [ ] The player reappears at the screen centre with zero velocity.
- [ ] Asteroids cannot hit the player while they are "dead".
- [ ] The invincibility window activates on respawn.
- [ ] The game world continues normally during the respawn delay.
- [ ] (Optional) The player sprite flashes during the invincibility window.
- [ ] The game runs without errors.
