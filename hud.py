import pygame
from constants import SCORE_POINTS, SCORE_BASE, SCREEN_WIDTH, SCREEN_HEIGHT
from asteroid import Asteroid
from player import Player

class HUD:
    def __init__(self):
        self.__score = 0.0
        self.__font = pygame.font.Font(None, 24)
        self.__weapon_text_sequence = ["Weapons: ", "(1)Pistol, ", "(2)MachineGun, ", "(3)Shotgun"]
        self.__weapon_text_width = self.__font.size("Weapons: (1)Pistol, (2)MachineGun, (3)Shotgun")[0]

    def draw(self, screen: pygame.Surface, player: Player) -> None:
        self.show_score(screen)
        self.show_lives(screen, player)
        self.show_weapons(screen, player)

    def update(self, dt: float) -> None:
        self.__score += dt;

    def add_score(self, asteroid: Asteroid) -> None:
        radius = asteroid.radius
        points = SCORE_POINTS.get(radius, SCORE_BASE)
        self.__score += points

    def show_score(self, screen: pygame.Surface) -> None:
        text_surface = self.__font.render(f"Score: {int(self.__score)}", True, "white");
        screen.blit(text_surface, (20, 20))

    def show_lives(self, screen: pygame.Surface, player: Player) -> None:
        text_surface = self.__font.render(f"Lives: {player.get_lives()}", True, "white")
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 30))

    def show_weapons(self, screen: pygame.Surface, player: Player) -> None:
        current_x = SCREEN_WIDTH - 30 - self.__weapon_text_width
        player_weapon = player.get_weapon().get_name()
        for text in self.__weapon_text_sequence:
            resolved_color = "green" if player_weapon in text else "white"
            text_surface = self.__font.render(text, True, resolved_color)
            screen.blit(text_surface, (current_x, SCREEN_HEIGHT - 30))
            current_x += text_surface.get_width()

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
