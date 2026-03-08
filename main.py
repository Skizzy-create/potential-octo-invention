import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from physics import resolve_circle_collision
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # init
    pygame.init()

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # wire containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # create player + asteroids field
    Skizzy = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # a new pygame Clock
    new_Clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while 1 > 0:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # fill the screen with black colour.
        screen.fill("black")

        # new way
        updatable.update(dt)

        # handle asteroid <-> asteroid collisions
        asteroid_list = list(asteroids)  # snapshot to avoid concurrency problems
        n = len(asteroid_list)
        for i in range(n):
            a = asteroid_list[i]
            for j in range(i + 1, n):
                b = asteroid_list[j]
                # use the existing method to check overlap
                if a.collides_with(b):
                    # restitution can be tuned; slightly inelastic avoids runaway speeds
                    resolve_circle_collision(a, b, restitution=0.9)

        for asteroid in asteroids:
            if Skizzy.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        # draw all objects in drawable Group
        for thing in drawable:
            thing.draw(screen)

        # drawing the player
        # Skizzy.draw(screen)

        # return's the time that has passed before the last tick,
        # and .tick() pauses the loop of 1/ 60th of a second
        # to make the game efficelty run at 60 FPS
        # /1000 makes it miliseconds( return value)
        dt = new_Clock.tick(60) / 1000

        # Skizzy.update(dt)

        # pygame'self. display.flip() method is sued to refersh the screen,
        # this always has to be the last to be called.
        pygame.display.flip()


if __name__ == "__main__":
    main()
