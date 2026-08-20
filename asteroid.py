import random
import pygame
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        points_num = random.randint(8, 12)
        angle_step = 360 / points_num
        self.__points: list[pygame.Vector2] = []

        for i in range(points_num):
            angle = i * angle_step
            point = pygame.Vector2(0, random.uniform(radius * 0.8, radius * 1.2)).rotate(angle)
            self.__points.append(point)

    def draw(self, screen: pygame.Surface) -> None:
        points = list(map(lambda p: p + self.position, self.__points))
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = -self.radius
        elif self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = -self.radius
        elif self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        ast1_velocity = self.velocity.rotate(angle)
        ast2_velocity = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast1 = Asteroid(self.position.x, self.position.y, new_radius)
        ast2 = Asteroid(self.position.x, self.position.y, new_radius)
        ast1.velocity = ast1_velocity * 1.2
        ast2.velocity = ast2_velocity * 1.2
