# Asteroids — Boot.dev-Style Assignment Track

Welcome to the assignment track for **potential-octo-invention** — the classic
Asteroids clone you've already built. This folder turns every item on the README
TODO list into a self-guided, Boot.dev-style chapter.

Each chapter tells you **what to build**, not how. You'll get goals, constraints,
hints, and a clear definition of done. Read each file in order, implement the
feature yourself, then move on.

---

## Chapter Order & Recommended Progression

| # | File | Topic | Difficulty |
|---|------|--------|------------|
| 01 | [01-screen-wrap.md](01-screen-wrap.md) | Screen Wrapping | ⭐ Beginner |
| 02 | [02-acceleration.md](02-acceleration.md) | Player Acceleration | ⭐ Beginner |
| 03 | [03-scoring.md](03-scoring.md) | Scoring System | ⭐⭐ Intermediate |
| 04 | [04-lives-part1.md](04-lives-part1.md) | Lives — Tracking & Display | ⭐⭐ Intermediate |
| 05 | [05-lives-part2.md](05-lives-part2.md) | Lives — Respawning | ⭐⭐ Intermediate |
| 06 | [06-background-image.md](06-background-image.md) | Background Image | ⭐ Beginner |
| 07 | [07-explosion-effect.md](07-explosion-effect.md) | Explosion Effect | ⭐⭐ Intermediate |
| 08 | [08-lumpy-asteroids.md](08-lumpy-asteroids.md) | Lumpy Asteroid Shapes | ⭐⭐⭐ Advanced |
| 09 | [09-triangle-hitbox.md](09-triangle-hitbox.md) | Triangular Ship Hitbox | ⭐⭐⭐ Advanced |
| 10 | [10-weapons-part1.md](10-weapons-part1.md) | Weapon Types — Spread & Rapid Fire | ⭐⭐ Intermediate |
| 11 | [11-weapons-part2.md](11-weapons-part2.md) | Weapon Types — Bombs | ⭐⭐⭐ Advanced |
| 12 | [12-powerups-shield.md](12-powerups-shield.md) | Power-up — Shield | ⭐⭐⭐ Advanced |
| 13 | [13-powerups-speed.md](13-powerups-speed.md) | Power-up — Speed Boost | ⭐⭐ Intermediate |

---

## How to Use This Track

1. **Read the chapter goal** before touching any code.
2. **Plan your approach** — sketch out what classes or functions you'll need.
3. **Implement it yourself.** Chapters contain hints, not solutions.
4. **Check the Definition of Done** at the bottom of each chapter to know when
   you're finished.
5. Move to the next chapter.

---

## Codebase Reference

Here are the key files you'll be working with:

| File | Purpose |
|------|---------|
| `main.py` | Game loop, group wiring, collision handling |
| `player.py` | `Player` class — movement, shooting, drawing |
| `asteroid.py` | `Asteroid` class — movement, splitting, drawing |
| `asteroidfield.py` | `AsteroidField` — spawns asteroids from screen edges |
| `shot.py` | `Shot` class — projectile behavior |
| `circleshape.py` | Base class for all circular game objects |
| `constants.py` | All tunable numeric constants |
| `physics.py` | Circle-circle collision resolution |
| `logger.py` | Game-state and event logging |

---

## Prerequisites

- You can run the game with `uv run python main.py` (or `python main.py` if
  pygame is already installed).
- You understand how pygame's `sprite.Group` works.
- You're comfortable reading and modifying object-oriented Python.

---

> Good luck, pilot. The cosmos won't blast itself.
