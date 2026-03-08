# Chapter 04 — Lives System, Part 1: Tracking & Display

## Goal

At the moment the game ends immediately when the player is hit once
(`sys.exit()` is called). A proper arcade game gives you multiple chances.
In this chapter you will add a **lives counter** that decrements on each hit
and display it on screen. Actual respawning is covered in Chapter 05.

---

## Background

The game-over logic in `main.py`:

```python
for asteroid in asteroids:
    if Skizzy.collides_with(asteroid):
        log_event("player_hit")
        print("Game over!")
        sys.exit()
```

You will replace the instant death with a "lose a life" event. When lives reach
zero the game ends; otherwise the player continues (we'll handle the
re-positioning in the next chapter).

---

## What to Build

### Part A — Lives Counter

1. Add a `lives` variable to the game loop, initialised to `PLAYER_LIVES`
   (a new constant).
2. When the player collides with an asteroid, decrement `lives` by 1 instead
   of calling `sys.exit()`.
3. Only call the "game over" logic when `lives` reaches 0.

### Part B — Lives Display

4. Display the remaining lives on screen (number, icons, or both — your
   choice).

---

## New Constant to Add

```python
# constants.py
PLAYER_LIVES = 3   # starting lives; tune to taste
```

---

## Constraints

- The player must have a brief **invincibility window** after being hit so they
  cannot lose multiple lives from a single asteroid pass-through. Track this
  with a cooldown timer on the player (similar to the shoot cooldown in
  `player.py`).
- When a life is lost but lives > 0, the game must **continue running** — do
  not call `sys.exit()`.
- When lives reach 0, print `"Game over!"` and end the game gracefully (you can
  still use `sys.exit()` here for now).

---

## Hints

<details>
<summary>Hint 1 — Invincibility cooldown on Player</summary>

In `player.py`, add an `invincible_timer` attribute (starts at 0). In
`player.update()`, decrement it each frame. In `main.py`, only count a
collision as a hit when `Skizzy.invincible_timer <= 0`, then set
`Skizzy.invincible_timer = PLAYER_INVINCIBLE_SECONDS` after a hit.

Add `PLAYER_INVINCIBLE_SECONDS` to `constants.py` (e.g. `2.0`).

</details>

<details>
<summary>Hint 2 — Displaying lives</summary>

The simplest display: render `f"Lives: {lives}"` with the same font you set up
in Chapter 03. Position it below the score.

A fancier option: draw small triangles (like the player sprite) for each
remaining life. `Player.triangle()` returns the three vertices — you could
create a helper to draw a small version at a fixed screen position.

</details>

<details>
<summary>Hint 3 — Game state flow</summary>

After decrementing lives, you need to decide what happens next. For now (before
Chapter 05), you can simply let the player keep flying at their current
position. The invincibility window will protect them from immediate further
hits. Respawning is the next chapter's problem.

</details>

---

## Files to Modify

- `constants.py` — add `PLAYER_LIVES` and `PLAYER_INVINCIBLE_SECONDS`.
- `player.py` — add `invincible_timer` attribute and update logic.
- `main.py` — replace `sys.exit()` on collision with lives-decrement logic;
  add lives display to the draw section.

---

## Definition of Done

- [ ] The player starts with `PLAYER_LIVES` lives (default 3).
- [ ] Colliding with an asteroid decrements lives by 1 (not immediately
  ending the game).
- [ ] An invincibility window prevents multiple lives being lost from a single
  collision.
- [ ] When lives reach 0 the game ends with "Game over!".
- [ ] The remaining lives count is always visible on screen.
- [ ] The game runs without errors.
