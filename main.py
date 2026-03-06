import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while 1 > 0:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # fill the screen with black colour.
        screen.fill("black")

        # pygame'self. display.flip() method is sued to refersh the screen,
        # this always has to be the last to be called.
        pygame.display.flip()


if __name__ == "__main__":
    main()
