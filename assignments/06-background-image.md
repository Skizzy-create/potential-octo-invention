# Chapter 06 — Background Image

## Goal

The black void looks fine, but a starfield background image would give the game
atmosphere and make it feel more like outer space. In this chapter you will load
an image and render it as the game's background each frame.

---

## Background

pygame's `screen.fill("black")` is called at the start of every frame in
`main.py` to clear the previous frame. Replacing (or augmenting) this with an
image blit gives you a persistent background.

The background must be drawn **before** all game objects so that it sits behind
everything else.

---

## What to Build

1. Add a background image file to the repository (see asset options below).
2. Load the image once before the game loop starts.
3. Scale it to fit the screen dimensions if necessary.
4. Blit it to the screen at the start of every frame (in place of, or right
   after, `screen.fill("black")`).

---

## Asset Options

Choose any approach that works for you:

| Option | Details |
|--------|---------|
| **Download a free starfield PNG** | Search for "free space starfield texture CC0". Many are available on OpenGameArt.org. Place it in an `assets/` folder. |
| **Generate one in Python** | Use pygame to draw random white dots onto a surface once before the loop, save that surface as your background. No external file needed. |
| **Use a solid colour + stars** | Keep `screen.fill((5, 5, 20))` for a dark blue tint, then draw scattered white `pygame.draw.circle` dots on top (radius 1). Simple and effective. |

The generated approach is recommended if you don't want to manage binary assets
in git.

---

## Constraints

- The background must be drawn every frame, before all game objects.
- If you use an image file, it **must** be scaled to `(SCREEN_WIDTH,
  SCREEN_HEIGHT)` — do not hard-code dimensions.
- If the image file cannot be found, the game should fall back gracefully (e.g.
  fill with black) rather than crashing.
- Do not store large binary files (>1 MB) in the repo — prefer generated or
  tiny images.

---

## Hints

<details>
<summary>Hint 1 — Loading and scaling an image</summary>

```python
import os

bg_path = os.path.join("assets", "starfield.png")
if os.path.exists(bg_path):
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    background = None
```

In the loop:

```python
if background:
    screen.blit(background, (0, 0))
else:
    screen.fill("black")
```

</details>

<details>
<summary>Hint 2 — Generating stars in Python</summary>

Create a surface once before the loop:

```python
import random

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((5, 5, 20))   # deep space blue-black
for _ in range(300):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    pygame.draw.circle(background, "white", (x, y), 1)
```

Then each frame: `screen.blit(background, (0, 0))`.

</details>

<details>
<summary>Hint 3 — Parallax (bonus)</summary>

For a fancier effect, create two star layers that scroll at different speeds,
wrapping horizontally. This creates a depth illusion without any 3D math. Store
an offset per layer and increment it each frame by `layer_speed * dt`.

</details>

---

## Files to Modify

- `main.py` — add background loading/generation before the loop; blit each
  frame.
- *(Optional)* `assets/` — add a background image file if using the image
  approach.
- *(Optional)* `constants.py` — add `BACKGROUND_PATH` or `STAR_COUNT` if you
  want to keep config separate.

---

## Definition of Done

- [ ] The game has a visible background (starfield, image, or coloured canvas
  with stars).
- [ ] The background renders behind all game objects every frame.
- [ ] No game objects are obscured by the background.
- [ ] The game does not crash if an optional image file is missing.
- [ ] The game runs without errors.
