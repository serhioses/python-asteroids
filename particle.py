import random
import pygame
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        self.__initial_radius = random.randint(2, 4)
        super().__init__(x, y, self.__initial_radius)
        self.__lifetime = 1
        self.__life_pct = 1
        direction: pygame.Vector2 = pygame.Vector2(0, 1)
        speed = random.randint(200, 250)
        self.velocity = (direction * speed).rotate(random.randint(0, 359))

    def update(self, dt: float) -> None:
        self.__lifetime -= dt
        if self.__lifetime <= 0:
            self.kill()
        self.__life_pct = self.__lifetime / 1
        self.radius = self.__initial_radius * self.__life_pct
        self.velocity *= (0.05 ** dt)
        self.position += self.velocity * dt

    def draw(self, screen: pygame.Surface) -> None:
        if self.__life_pct > 0.6:
            color = "yellow"
        elif self.__life_pct > 0.3:
            color = "orange"
        else:
            color = "red"
        pygame.draw.circle(screen, color, self.position, self.radius)
