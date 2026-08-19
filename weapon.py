import pygame
import random
from constants import PISTOL_COOLDOWN_SECONDS, MACHINE_GUN_COOLDOWN_SECONDS, SHOTGUN_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED, SHOT_RADIUS
from shot import Shot

class Weapon(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self, name: str = "Weapon"):
        super().__init__(self.containers)
        self._shoot_cooldown = 0
        self._name = name

    def update(self, dt: float) -> None:
        self._shoot_cooldown -= dt
        self._shoot_cooldown = max(self._shoot_cooldown, 0)

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        raise NotImplementedError

    def freeze(self, time: float) -> None:
        self._shoot_cooldown = time

    def get_name(self) -> str:
        return self._name

class Pistol(Weapon):
    def __init__(self):
        super().__init__("Pistol")

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        if self._shoot_cooldown > 0:
            return
        self._shoot_cooldown = PISTOL_COOLDOWN_SECONDS
        Shot(position.x, position.y, rotation, PLAYER_SHOOT_SPEED)

class MachineGun(Weapon):
    def __init__(self):
        super().__init__("MachineGun")

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        if self._shoot_cooldown > 0:
            return
        self._shoot_cooldown = MACHINE_GUN_COOLDOWN_SECONDS
        Shot(position.x, position.y, rotation, PLAYER_SHOOT_SPEED)

class Shotgun(Weapon):
    def __init__(self):
        super().__init__("Shotgun")
        self.__degree_spread = 60

    def fire(self, position: pygame.Vector2, rotation: float) -> None:
        if self._shoot_cooldown > 0:
            return
        self._shoot_cooldown = SHOTGUN_COOLDOWN_SECONDS
        pellet_num = random.randint(5, 7)
        start_offset = self.__degree_spread / 2 * -1
        angle_step = self.__degree_spread / (pellet_num - 1)
        for i in range(0, pellet_num):
            pellet_rotation = (start_offset + angle_step * i) + rotation
            rand_speed = random.randint(PLAYER_SHOOT_SPEED - 50, PLAYER_SHOOT_SPEED + 50)
            rand_radius = random.randint(SHOT_RADIUS - 2, SHOT_RADIUS + 3)
            Shot(position.x, position.y, pellet_rotation, rand_speed, rand_radius)
