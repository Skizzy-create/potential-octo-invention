# Chapter 03 — Scoring System

## Goal

Right now you can blast asteroids all day with no record of your heroics. Add a
**scoring system** that awards points for destroying asteroids and displays the
current score on screen throughout the game.

---

## Background

When a shot hits an asteroid, `main.py` calls `asteroid.split()` and
`shot.kill()`. The split logic is in `asteroid.py`. There is currently no
concept of a score anywhere in the codebase.

Pygame can render text to the screen using `pygame.font.Font` (or
`pygame.font.SysFont`). Text is rendered to a `Surface`, then blitted onto the
main screen surface.

---

## What to Build

### Part A — Track the Score

1. Introduce a `score` variable in the game loop (`main.py`).
2. Each time an asteroid is destroyed (shot hits it), add points to `score`.
3. Larger asteroids should be worth **more** points than smaller ones.

### Part B — Display the Score

4. Render the current score as text in a corner of the screen each frame.
5. The font, size, colour, and position are up to you — make it readable.

---

## Scoring Suggestions

You decide the exact point values, but a reasonable scheme:

| Asteroid size | Points |
|---------------|--------|
| Large         | 20     |
| Medium        | 50     |
| Small         | 100    |

You can derive "size" from `asteroid.radius` compared to `ASTEROID_MIN_RADIUS`
in `constants.py`.

---

## Constraints

- The score must survive the entire game session — do not reset it between
  asteroid waves.
- The score display must **not** flicker (render it every frame, in the draw
  section of the loop).
- Do **not** hard-code pixel values for text positioning that only work at one
  screen resolution — use `SCREEN_WIDTH` / `SCREEN_HEIGHT` from `constants.py`.

---

## Hints

<details>
<summary>Hint 1 — Where to increment the score</summary>

In `main.py`, the shot-asteroid collision block looks like:

```python
for asteroid in asteroids:
    for shot in shots:
        if asteroid.collides_with(shot):
            asteroid.split()
            shot.kill()
```

This is the right place to add `score += <points>`. You need to know the
asteroid's radius before calling `split()` (which calls `self.kill()`).

</details>

<details>
<summary>Hint 2 — Initialising the font</summary>

Initialise once, before the game loop starts:

```python
font = pygame.font.SysFont(None, 48)   # None = default system font, size 48
```

Then each frame inside the draw section:

```python
text_surface = font.render(f"Score: {score}", True, "white")
screen.blit(text_surface, (20, 20))    # top-left corner
```

</details>

<details>
<summary>Hint 3 — Deriving point value from radius</summary>

`asteroid.radius` at the time of the hit tells you the asteroid's current size.
The smallest possible asteroid has radius `ASTEROID_MIN_RADIUS`. You can
calculate a tier like this:

```python
tier = round(asteroid.radius / ASTEROID_MIN_RADIUS)
```

Then map tier → points however you like.

</details>

---

## Files to Modify

- `main.py` — add `score` variable, increment on asteroid kill, render score
  text each frame.
- `constants.py` — optionally add named point-value constants
  (`SCORE_LARGE`, `SCORE_MEDIUM`, `SCORE_SMALL`) to keep magic numbers out of
  the game loop.

---

## Definition of Done

- [ ] A `score` variable starts at 0 and increases each time an asteroid is
  destroyed.
- [ ] Larger asteroids award more points than smaller ones.
- [ ] The current score is displayed on screen at all times.
- [ ] The text is readable (legible font size and colour).
- [ ] The display does not flicker.
- [ ] The game runs without errors.
