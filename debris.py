import pygame
import random
from circleshape import CircleShape

class Debris(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 0)
        self.__lifetime = 5
        direction: pygame.Vector2 = pygame.Vector2(0, 1)
        speed = random.randint(40, 80)
        self.velocity = (direction * speed).rotate(random.randint(0, 359))
        self.__random_radius = random.randint(1, 3)

    def update(self, dt: float) -> None:
        self.__lifetime -= dt
        if self.__lifetime <= 0:
            self.kill()
        self.position += self.velocity * dt

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "gray", self.position, self.__random_radius)
