import pygame
from constants import SCORE_POINTS, SCORE_BASE
from asteroid import Asteroid

class Scoring:
    def __init__(self):
        self.score = 0.0
        self.__font = pygame.font.Font(None, 24)

    def draw(self, screen: pygame.Surface) -> None:
        text_surface = self.__font.render(f"Score: {int(self.score)}", True, "white");
        screen.blit(text_surface, (20, 20))

    def update(self, dt: float) -> None:
        self.score += dt;

    def add_score(self, asteroid: Asteroid) -> None:
        radius = asteroid.radius
        points = SCORE_POINTS.get(radius, SCORE_BASE)
        self.score += points

# import math
# import pygame
# from constants import SCORE_POINTS, SCORE_BASE
# from asteroid import Asteroid

# class Scoring(pygame.sprite.Sprite):
#     containers: tuple[pygame.sprite.Group, ...]

#     def __init__(self):
#         super().__init__(*self.containers)
#         self.score = 0
#         self.seconds_alive = 0
#         self.seconds_cooldown = 0
#         self.__font = pygame.font.Font(None, 24)

#     def draw(self, screen: pygame.Surface) -> None:
#         text_surface = self.__font.render(str(self.score), True, "white")
#         screen.blit(text_surface, (20, 20))

#     def update(self, dt: float) -> None:
#         self.seconds_alive += dt
#         self.seconds_cooldown -= dt
#         self.seconds_cooldown = max(self.seconds_cooldown, 0)
#         self.set_score()

#     def add_score(self, asteroid: Asteroid) -> None:
#         radius = asteroid.radius
#         points = SCORE_POINTS.get(radius, SCORE_BASE)
#         self.score += points

#     def set_score(self) -> None:
#         if self.seconds_cooldown > 0:
#             return
#         self.seconds_cooldown = 1
#         seconds_alive = math.floor(self.seconds_alive)
#         self.score += int(math.sqrt(seconds_alive))
