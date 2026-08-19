import pygame
import random
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from weapon import Weapon, Pistol
from shot import Shot
from explosion import Explosion
from debris import Debris
from particle import Particle
from hud import HUD

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    shots: pygame.sprite.Group = pygame.sprite.Group()

    Weapon.containers = updatable
    weapon = Pistol()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, weapon)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    AsteroidField()
    Shot.containers = (shots, drawable, updatable)
    Explosion.containers = (drawable, updatable)
    Debris.containers = (drawable, updatable)
    Particle.containers = (drawable, updatable)

    # Scoring.containers = (drawable, updatable)
    hud = HUD()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_original = pygame.image.load("./images/bg.jpg").convert()
    bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.set_alpha(100)

    dt = 0.0
    clock = pygame.time.Clock()
    running = True

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.set_weapon(1)
                elif event.key == pygame.K_2:
                    player.set_weapon(2)
                elif event.key == pygame.K_3:
                    player.set_weapon(3)

        if running:
            updatable.update(dt)
            hud.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player) and player.is_vulnerable():
                    log_event("player_hit")
                    remaining_lives = player.take_hit()
                    if remaining_lives <= 0:
                        player.kill()
                        print("Game over!")
                        running = False
                        break
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        # Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        for i in range(0, random.randint(20, 30)):
                            # Debris(asteroid.position.x, asteroid.position.y)
                            Particle(asteroid.position.x, asteroid.position.y)
                        hud.add_score(asteroid)
                        break

        screen.fill("black")
        screen.blit(bg, (0, 0))

        for d in drawable:
            d.draw(screen)
        hud.draw(screen, player)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
