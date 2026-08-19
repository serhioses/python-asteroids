import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_LIVES, PLAYER_INVULNERABILITY_SECONDS, PLAYER_ACCELERATION, PLAYER_MAX_SPEED
from circleshape import CircleShape
from shot import Shot
from weapon import Weapon, Pistol, MachineGun, Shotgun

class Player(CircleShape):
    def __init__(self, x: float, y: float, weapon: Weapon) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.__initial_x = x
        self.__initial_y = y
        self.rotation = 0
        self.__lives = PLAYER_LIVES
        self.__invulnerability_cooldown = 0
        self.__speed = 0
        self.__weapon = weapon

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        should_skip_frame = int(self.__invulnerability_cooldown * 6) % 2 == 0
        if not self.is_vulnerable() and should_skip_frame:
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)   
        pygame.draw.circle(screen, "red", self.position, PLAYER_RADIUS, LINE_WIDTH)
            

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.__invulnerability_cooldown = max(self.__invulnerability_cooldown - dt, 0);

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.__speed = 0

    def move(self, dt: float, direction: int) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.__speed += PLAYER_ACCELERATION * dt
            
        if self.__speed > PLAYER_MAX_SPEED:
            self.__speed = PLAYER_MAX_SPEED
        rotated_with_speed_vector = rotated_vector * self.__speed * dt * direction
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        self.__weapon.fire(self.position, self.rotation)

    def take_hit(self) -> int:
        self.__lives -= 1
        if self.__lives > 0:
            self.respawn()
        return self.__lives

    def respawn(self) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(self.__initial_x, self.__initial_y)
        self.rotation = 0
        self.__weapon.freeze(PLAYER_INVULNERABILITY_SECONDS)
        self.__invulnerability_cooldown = PLAYER_INVULNERABILITY_SECONDS
        self.__speed = 0

    def get_lives(self) -> int:
        return self.__lives

    def is_vulnerable(self) -> bool:
        return self.__invulnerability_cooldown == 0

    def get_weapon(self) -> Weapon:
        return self.__weapon

    def set_weapon(self, n: int) -> None:
        new_weapon: Weapon | None = None
        if n == 1:
            new_weapon = Pistol()
        elif n == 2:
            new_weapon = MachineGun()
        elif n == 3:
            new_weapon = Shotgun()
        if new_weapon and not isinstance(self.__weapon, new_weapon.__class__):
            old_weapon = self.__weapon
            self.__weapon = new_weapon
            old_weapon.kill()
