# main.py
# make an original game

import pygame
import random

# ----- CONSTANTS
WIDTH = 600
HEIGHT = 850
ENEMY_VEL = 20
LIVES = 1
TITLE = "mushroom smush"

# Create a background class
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/bg.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/toad.png")
        self.image = pygame.transform.scale(self.image, (54, 75))
        self.rect = self.image.get_rect()

        # Initialize velocity
        self.vel_x = 0

        # Spawn player at the bottom of the screen
        self.rect.bottom = HEIGHT - 75
        self.rect.right = WIDTH / 2

    # Update player
    def update(self):
        # Moves left and right
        self.rect.x += self.vel_x

    # Move left function
    def go_left(self):
        self.vel_x = -10
        self.image = pygame.image.load("./images/toad_flipped.png")
        self.image = pygame.transform.scale(self.image, (54, 75))

    # Move right function
    def go_right(self):
        self.vel_x = 10
        self.image = pygame.image.load("./images/toad.png")
        self.image = pygame.transform.scale(self.image, (54, 75))

    # Stop function
    def stop(self):
        self.vel_x = 0

# Create enemy class, scale enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/thwomp.png")
        self.image = pygame.transform.scale(self.image, (107, 120))
        self.rect = self.image.get_rect()

        # Set enemy velocity
        self.vel_y = ENEMY_VEL

        # Spawn a thwomp randomly at the top of the screen
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)

    def update(self):
        self.rect.y += self.vel_y

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    game_over = False

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    thwomp_spawn_time = 450
    last_thwomp_spawn = pygame.time.get_ticks()
    play_dead_sound = False

    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_score_x = 10
    text_score_y = 10

    def display_score(x, y):
        score = font.render("Score: " + str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    # Lives
    lives_value = 1
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_lives_x = 10
    text_lives_y = 40

    def display_lives(x, y):
        lives = font.render("Lives: " + str(lives_value), True, (0, 0, 0))
        screen.blit(lives, (x, y))

    # Sprite groups
    all_sprite_group = pygame.sprite.Group()
    background_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Player and enemy creation
    player = Player()
    all_sprite_group.add(player)

    # Background creation
    bg = Background()
    background_group.add(bg)

    # Background music
    pygame.mixer.music.load("./assets/bgm.mp3")
    pygame.mixer.music.play(-1)

    # Death music
    dead_sound = pygame.mixer.Sound("./assets/dead.mp3")

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Move player if user presses down on left/right arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_LEFT:
                    player.go_left()

            # Stop player if arrow key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

        # Restrict player to stay on screen
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.left < 0:
            player.rect.left = 0

        # ----- LOGIC
        all_sprite_group.update()

        if not game_over:
            # Thwomp spawn
            if pygame.time.get_ticks() > last_thwomp_spawn + thwomp_spawn_time:
                # Set the new time to this current time
                last_thwomp_spawn = pygame.time.get_ticks()
                # Spawn thwomp
                enemy = Enemy()
                all_sprite_group.add(enemy)
                enemy_group.add(enemy)

        # Player collides with a thwomp
        for enemy in enemy_group:
            # Kill if off screen
            if enemy.rect.bottom > HEIGHT:
                enemy.kill()
                # Add a point to score
                score_value += 1

        # Kill player if crushed by enemy
        enemies_hit = pygame.sprite.spritecollide(player, enemy_group, False)
        if len(enemies_hit) > 0:
            player.kill()
            lives_value -= 1

        # Game over
        if lives_value <= 0:
            game_over = True
            player.vel_x = 0
            # Play squish sound
            if not play_dead_sound:
                pygame.mixer.Sound.play(dead_sound)
                play_dead_sound = True
            # Stop enemy sounds
            for enemy in enemy_group:
                enemy.kill()

            # Stop background music
            pygame.mixer.music.stop()

        # ----- DRAW
        background_group.draw(screen)
        all_sprite_group.draw(screen)
        dirty_rectangles = all_sprite_group.draw(screen)

        # ----- UPDATE
        display_score(text_score_x, text_score_y)
        display_lives(text_lives_x, text_lives_y)
        pygame.display.update(dirty_rectangles)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()