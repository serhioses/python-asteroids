import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x: float, y: float, rotation: float, speed: int, radius: int = SHOT_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 1).rotate(rotation) * speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
