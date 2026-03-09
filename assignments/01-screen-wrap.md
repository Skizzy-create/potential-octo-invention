# Chapter 01 — Screen Wrapping

## Goal

Right now, asteroids and shots fly off-screen and are gone forever. The classic
Asteroids arcade game wraps all objects around the screen — an asteroid that
exits the right edge reappears on the left, and so on. Your job is to add that
behaviour to **every** moving object in the game.

---

## Background

The screen dimensions are defined in `constants.py`:

```
SCREEN_WIDTH  = 2360
SCREEN_HEIGHT = 1240
```

Every game object that moves (player, asteroids, shots) inherits from
`CircleShape` in `circleshape.py`. Each has a `self.position` attribute — a
`pygame.Vector2`.

---

## What to Build

Add screen-wrapping logic so that any object whose centre crosses a screen edge
reappears on the opposite edge.

### Rules

- An object that moves past the **right** edge (`x > SCREEN_WIDTH`) should
  reappear at `x = 0`.
- An object that moves past the **left** edge (`x < 0`) should reappear at
  `x = SCREEN_WIDTH`.
- The same applies vertically (top ↔ bottom).
- The object's velocity must **not** change — it keeps moving in the same
  direction.
- The wrap should be seamless; the object should not "skip" a frame.

---

## Constraints

- Do **not** duplicate the wrapping logic in every class separately.
- You must find a single place to put the wrap logic so that all objects benefit
  from it without each class having to know about it.
- Shots should also wrap (even if that feels odd — it keeps things consistent;
  you can revisit this decision later).

---

## Hints

<details>
<summary>Hint 1 — Where to put the logic</summary>

`CircleShape` is the base class for `Player`, `Asteroid`, and `Shot`. Adding a
`wrap(self)` method there means every subclass inherits it for free.

</details>

<details>
<summary>Hint 2 — When to call it</summary>

The game loop in `main.py` calls `updatable.update(dt)` on every frame. Each
subclass already has an `update(self, dt)` method. The right time to call
`self.wrap()` is at the end of each `update` method, after the position has
changed.

Alternatively, you could call `wrap()` directly from `CircleShape.update()` —
but remember that subclasses override `update`, so think carefully about where
the call actually ends up.

</details>

<details>
<summary>Hint 3 — Modulo arithmetic</summary>

The modulo operator `%` is your friend here. For example:

```python
self.position.x = self.position.x % SCREEN_WIDTH
```

This naturally wraps any value into the range `[0, SCREEN_WIDTH)`.

</details>

---

## Files to Modify

- `circleshape.py` — add the `wrap()` helper method.
- `player.py`, `asteroid.py`, `shot.py` — call `wrap()` inside each `update`
  method (or arrange for `CircleShape.update` to do it, if you prefer that
  design).
- `constants.py` — you'll need to import `SCREEN_WIDTH` and `SCREEN_HEIGHT`
  in `circleshape.py`.

---

## Definition of Done

- [ ] The player ship wraps around all four edges without any visual jump.
- [ ] Asteroids wrap smoothly and continue at the same velocity after wrapping.
- [ ] Shots also wrap (even tiny ones).
- [ ] There is **no** duplicated wrapping code across classes — the logic lives
  in one place.
- [ ] The game runs without errors.
