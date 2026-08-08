import pygame
from constants import EXPLOSION_SPEED
from circleshape import CircleShape

class Explosion(CircleShape):
    def __init__(self, x: float, y: float, max_radius: int) -> None:
        super().__init__(x, y, 0)
        self.__max_radius = max_radius

    def update(self, dt: float) -> None:
        self.radius += EXPLOSION_SPEED * dt
        if self.radius >= self.__max_radius:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        line_width = int(self.__max_radius / 2 - self.radius / 2)
        pygame.draw.circle(screen, "orange", self.position, self.radius, max(line_width, 1))
