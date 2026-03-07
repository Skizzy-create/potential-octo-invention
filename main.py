import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # init
    Skizzy = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pygame.init()

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

        # drawing the player
        Skizzy.draw(screen)

        # return's the time that has passed before the last tick,
        # and .tick() pauses the loop of 1/ 60th of a second
        # to make the game efficelty run at 60 FPS
        # /1000 makes it miliseconds( return value)
        dt = new_Clock.tick(60) / 1000

        # pygame'self. display.flip() method is sued to refersh the screen,
        # this always has to be the last to be called.
        pygame.display.flip()


if __name__ == "__main__":
    main()
