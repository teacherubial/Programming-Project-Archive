# Peter Li - peteryuli1204@gmail.com

import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 800
RADIUS = 75
TIME_TO_FIND = 8000
TIME_TO_CATCH = 10000
TITLE = "Pyter Game"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("assets/circle.png")
        self.image = pygame.transform.scale(self.image, (2 * RADIUS - 40, 2 * RADIUS - 40))

        # Collision
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Move the player."""
        self.rect.center = pygame.mouse.get_pos()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./assets/demon.png")
        self.image = pygame.transform.scale(self.image, (96, 70))

        # Collision
        self.rect = self.image.get_rect()
        self.rect.center = random_coords()
        self.mask = pygame.mask.from_surface(self.image)

        # Velocity
        self.xvel = 0.0
        self.yvel = 0.0

    def update(self):
        """Move the enemy."""
        self.rect.x += self.xvel
        self.rect.y += self.yvel

    def kill(self) -> None:
        """Kill the enemy."""
        pygame.sprite.Sprite.kill(self)


def random_coords() -> tuple:
    """Returns a random x, y coordinate between 80 to WIDTH minus 80 and 80 to HEIGHT minus 80"""
    return random.randrange(80, WIDTH - 80), random.randrange(80, HEIGHT - 80)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_visible(False)

    background = pygame.image.load("./assets/floor_tiles.png").convert()

    jump_scare = pygame.image.load("./assets/demon.png")
    jump_scare = pygame.transform.scale(jump_scare, (800, 800))

    # ----- LOCAL VARIABLES
    # Pygame conditions
    done = False
    clock = pygame.time.Clock()

    # Game conditions
    found = False
    game_over = False
    jump_scare_played = False
    score = 0

    # Sprites
    all_sprites_group = pygame.sprite.Group()
    player_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()

    player = Player()
    player_sprites_group.add(player)
    all_sprites_group.add(player)

    enemy = Enemy()
    enemy_sprites_group.add(enemy)
    all_sprites_group.add(enemy)

    # Time tracking variables
    time_spawned = 0
    time_found = 0

    # Enemy velocity
    velocity_x = 2.0
    velocity_y = 3.0

    # Sounds
    enemy_sound = pygame.mixer.Sound("./assets/enemy-laugh.ogg")
    kill_sound = pygame.mixer.Sound("./assets/kill-sound.ogg")
    death_sound = pygame.mixer.Sound("./assets/death-sound.ogg")

    # Font
    font = pygame.font.SysFont("Georgia", 80)

    # ----- MAIN LOOP

    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # When clicked check if enemy was clicked
                for e in enemy_sprites_group:
                    if e.rect.collidepoint(pygame.mouse.get_pos()):
                        # Kill enemy and create a new enemy
                        e.kill()
                        enemy = Enemy()
                        all_sprites_group.add(enemy)
                        enemy_sprites_group.add(enemy)

                        # Change conditions
                        found = False
                        score += 1
                        enemy_sound.stop()
                        kill_sound.play()
                        time_spawned = pygame.time.get_ticks()

                        # Increase the speed of the enemy
                        velocity_x += 1
                        velocity_y += 1

        if not game_over:
            # ----- LOGIC
            # Update sprites
            all_sprites_group.update()

            # Check if found yet to only allow collision once
            if not found:
                enemy_collide = pygame.sprite.spritecollide(player, enemy_sprites_group, False, pygame.sprite.collide_mask)

                # Game over if the player does not find the enemy in time
                if pygame.time.get_ticks() - time_spawned > TIME_TO_FIND:
                    game_over = True

            # Make enemy move and laugh if collided with
            if len(enemy_collide) > 0:
                # Make it so the colliding won't register again until the enemy is clicked
                found = True

                # Play enemy found sound
                enemy_sound.play()

                # Set the enemy's movement speed and random direction
                enemy.xvel += (velocity_x * random.choice([-1, 1]))
                enemy.yvel += (velocity_y * random.choice([-1, 1]))

                # Clear the list so that this if statement will only run for one loop
                enemy_collide.clear()

                # Set time found
                time_found = pygame.time.get_ticks()

            # Make enemy bounce off walls
            if (enemy.rect.x + 48) > WIDTH or enemy.rect.x < 0:
                enemy.xvel *= -1

            if (enemy.rect.y + 35) > HEIGHT or enemy.rect.y < 0:
                enemy.yvel *= -1

            # Game over if the player does not catch the enemy in time
            if pygame.time.get_ticks() - time_found > TIME_TO_CATCH:
                game_over = True

        # ----- RENDER
            # Light circle
            cover_surf = pygame.Surface((RADIUS * 2, RADIUS * 2))
            cover_surf.fill(0)
            cover_surf.set_colorkey((255, 255, 255))
            pygame.draw.circle(cover_surf, (255, 255, 255), (RADIUS, RADIUS), RADIUS)

            clip_center = pygame.mouse.get_pos()
            screen.fill(0)
            clip_rect = pygame.Rect(clip_center[0] - RADIUS, clip_center[1] - RADIUS, RADIUS * 2, RADIUS * 2)
            screen.set_clip(clip_rect)

            # Game and sprites
            screen.blit(background, (0, 0))
            enemy_sprites_group.draw(screen)
            screen.blit(cover_surf, clip_rect)

        else:
            # ----- LOGIC
            if not jump_scare_played:
                death_sound.play()
                jump_scare_played = True

            # ----- RENDER
            # Image
            rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            screen.set_clip(rect)
            screen.fill(BLACK)
            screen.blit(jump_scare, (0, 0))

            # Words
            score_surf = font.render(f"Final Score: {score}", True, WHITE)
            score_rect = score_surf.get_rect()
            score_rect.midtop = (WIDTH/2, 700)
            screen.blit(score_surf, score_rect)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(75)

    pygame.quit()


if __name__ == "__main__":
    main()
