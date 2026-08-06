import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_LIVES, PLAYER_INVULNERABILITY_SECONDS
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.__initial_x = x
        self.__initial_y = y
        self.rotation = 0
        self.__shoot_cooldown = 0
        self.__lives = PLAYER_LIVES
        self.__invulnerability_cooldown = 0

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
        self.__shoot_cooldown -= dt
        self.__shoot_cooldown = max(self.__shoot_cooldown, 0)
        self.__invulnerability_cooldown = max(self.__invulnerability_cooldown - dt, 0);

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.__shoot_cooldown > 0:
            return
        self.__shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def take_hit(self) -> int:
        self.__lives -= 1
        if self.__lives > 0:
            self.respawn()
        return self.__lives

    def respawn(self) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(self.__initial_x, self.__initial_y)
        self.rotation = 0
        self.__shoot_cooldown = PLAYER_INVULNERABILITY_SECONDS
        self.__invulnerability_cooldown = PLAYER_INVULNERABILITY_SECONDS

    def get_lives(self) -> int:
        return self.__lives

    def is_vulnerable(self) -> bool:
        return self.__invulnerability_cooldown == 0
