from circleshape import CircleShape
import pygame
from logger import log_event
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        new_dir = random.uniform(20, 50)

        new_dir_vel_1 = self.velocity.rotate(new_dir)
        new_dir_vel_2 = self.velocity.rotate(-new_dir)

        self.radius -= ASTEROID_MIN_RADIUS

        child1 = Asteroid(self.position.x, self.position.y, self.radius)
        child2 = Asteroid(self.position.x, self.position.y, self.radius)

        child1.velocity = new_dir_vel_1 * 1.2
        child2.velocity = new_dir_vel_2 * 1.2
