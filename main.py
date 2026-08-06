import sys
import pygame
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
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

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    AsteroidField()
    Shot.containers = (shots, drawable, updatable)

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
                        hud.add_score(asteroid)

        screen.fill("black")
        screen.blit(bg, (0, 0))

        for d in drawable:
            d.draw(screen)
        hud.draw(screen, player)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
