# Matthew Wong

# Pygame Project


import pygame
import random
from pygame import mixer


# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1920
HEIGHT = 1080
SPEED = 4
font_name = pygame.font.match_font('menlo')
TITLE = "<Pygame Project 2022>"
pygame.mixer.init()

# Game sounds
peanut_sound = pygame.mixer.Sound("./Sounds/Anya say peanut.ogg")
damage_sound = pygame.mixer.Sound("./Sounds/Anya-Shocked-Sound.ogg")
heart_sound = pygame.mixer.Sound("./Sounds/Anya Waku Waku.ogg")
dad_sound = pygame.mixer.Sound("./Sounds/Anya Chi Chi.ogg")

# Background Music
mixer.init()
mixer.music.load("./Sounds/SPY x FAMILY Main Theme - EPIC VERSION (1).ogg")
mixer.music.play()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Background

background_image = pygame.image.load("./Assets/City Background.jpg")
background_image = pygame.transform.scale(background_image, (1920, 1080))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Anya_Forger_Anime_2.png")
        self.image = pygame.transform.scale(self.image, (100, 250))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2 - 97.5
        self.rect.y = HEIGHT - self.rect.height - 10

        # Speed
        self.vel_x = 0
        self.player_speed = 4.5

    def update(self):
        self.rect.x += self.vel_x * self.player_speed

class Peanut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Peanut.png")
        self.image = pygame.transform.scale(self.image, (80, 120))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(25, WIDTH - self.rect.width - 25)
        self.rect.y = 0

        # Speed
        self.vel_y = 8

    def update(self):
        self.rect.y += self.vel_y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Villain.png")
        self.image = pygame.transform.scale(self.image, (150 , 180))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # Speed
        self.vel_y = 10

    def update(self):
        self.rect.y += self.vel_y

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Heart Powerup.png")
        self.image = pygame.transform.scale(self.image, (80, 100))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(25, WIDTH - self.rect.width - 25)
        self.rect.y = 0

        # Speed
        self.vel_y = 9

    def update(self):
        self.rect.y += self.vel_y

class Loid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Loid.png")
        self.image = pygame.transform.scale(self.image, (300, 300))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(25, WIDTH - self.rect.width - 25)
        self.rect.y = 0

        # Speed
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    peanut_spawn = random.randrange(3000, 6000)
    heart_spawn = random.randrange(8000, 10000)
    loid_spawn = random.randrange (20000, 25000)
    enemy_spawn = 1000
    peanut_latest_spawn = pygame.time.get_ticks()
    enemy_latest_spawn = pygame.time.get_ticks()
    heart_latest_spawn = pygame.time.get_ticks()
    loid_latest_spawn = pygame.time.get_ticks()
    score = 0
    life = 0
    game_over = True

    # Intro / Game Over Screen
    def show_go_screen():
        screen.blit(background_image, (0, 0))
        draw_text(screen, "Anya's Peanut Addiction", 80, WIDTH / 2, HEIGHT / 4 + 120)
        draw_text(screen, "Controls: Use A and D to move!", 32, WIDTH / 2, HEIGHT / 2 + 50)
        draw_text(screen, "Press ENTER to Begin", 24, WIDTH / 2, HEIGHT * (3 / 4) + 120)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("./Sounds/SPY x FAMILY Main Theme - EPIC VERSION (1).ogg")
                        pygame.mixer.music.play(-1)

    # ------ SPRITE GROUPS
    all_sprites_group = pygame.sprite.RenderUpdates()
    peanut_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    heart_group = pygame.sprite.Group()
    loid_group = pygame.sprite.Group()


    # Player
    player = Player()
    all_sprites_group.add(player)

    # ----- MAIN LOOP
    while not done:

        if game_over:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./Sounds/SPY x FAMILY Main Theme - EPIC VERSION (1).ogg")
            pygame.mixer.music.play(-1)
            # show game over screen
            show_go_screen()
            # reset game
            enemy_spawn = 1000
            life = 1000
            invincibility = False
            score = 0
            player.vel_x = 0
            player.rect.x = WIDTH / 2 - 97.5
            player.rect.y = HEIGHT - player.rect.height - 10
            for enemy in enemy_group:
                enemy.kill()
            for peanut in peanut_group:
                peanut.kill()
            for heart in heart_group:
                heart.kill()
            for loid in loid_group:
                loid.kill()
            game_over = False

        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # ---- CONTROLS
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        player.vel_x = SPEED
                    elif event.key == pygame.K_a:
                        player.vel_x = -SPEED

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.vel_x < 0:
                        player.vel_x = 0
                    if event.key == pygame.K_d and player.vel_x > 0:
                        player.vel_x = 0

        # Makes sure player is not out of screen (x-axis)
        if player.rect.right > WIDTH:
           player.rect.right = WIDTH
        if player.rect.left < 0:
           player.rect.left = 0

        # ----- LOGIC
        all_sprites_group.update()

        if not game_over:

            # Peanut Spawn
            if pygame.time.get_ticks() > peanut_latest_spawn + peanut_spawn:
                # set the new time to this current time
                peanut_latest_spawn = pygame.time.get_ticks()
                # Spawn Peanut
                peanut = Peanut()
                all_sprites_group.add(peanut)
                peanut_group.add(peanut)

            # Enemy Spawn
            if pygame.time.get_ticks() > enemy_latest_spawn + enemy_spawn:
                enemy_latest_spawn = pygame.time.get_ticks()
                # Spawn enemy
                enemy = Enemy()
                all_sprites_group.add(enemy)
                enemy_group.add(enemy)

            # Heart Spawn
            if pygame.time.get_ticks() > heart_latest_spawn + heart_spawn:
                heart_latest_spawn = pygame.time.get_ticks()
                # Spawn heart
                heart = Heart()
                all_sprites_group.add(heart)
                heart_group.add(heart)

            # Loid Spawn
            if pygame.time.get_ticks() > loid_latest_spawn + loid_spawn:
                loid_latest_spawn = pygame.time.get_ticks()
                # Spawn heart
                loid = Loid()
                all_sprites_group.add(loid)
                loid_group.add(loid)

            # If a peanut hits the ground
            for peanut in peanut_group:
                if peanut.rect.y >= HEIGHT - peanut.rect.height - 7:
                    peanut.kill()

                # Player collision
                peanuts_collected = pygame.sprite.spritecollide(player, peanut_group, True)
                if len(peanuts_collected) > 0:
                    peanut.kill()
                    peanut_sound.play()
                    score += 1

            # If an enemy hits the player
            enemy_collide = pygame.sprite.spritecollide(player, enemy_group, dokill= False)
            for enemy in enemy_group:
                if len(enemy_collide) > 0:
                    # enemy.kill()
                    damage_sound.play()
                    life -= 1

            # If a heart hits the player

            for heart in heart_group:
                if heart.rect.y >= HEIGHT - heart.rect.height - 7:
                    heart.kill()

                heart_collected = pygame.sprite.spritecollide(player, heart_group, True)
                if len(heart_collected) > 0:
                    heart.kill()
                    heart_sound.play()
                    life += 200

            # If Loid hits the player

            for loid in loid_group:
                if loid.rect.y >= HEIGHT - loid.rect.height - 7:
                    loid.kill()
                    dad_sound.play()
                # Loid killing enemies
                loid_collide = pygame.sprite.spritecollide(loid, enemy_group, dokill= True)
                if len(loid_collide) > 0:
                    enemy.kill()

            # Speed Game Up at Certain Scores
            if score >= 2:
                enemy_latest_spawn -= 10

            if score >= 5:
                enemy_latest_spawn -= 20

            if score >= 10:
                enemy_latest_spawn -= 40


            # Game Over
            if life <= 0:
                game_over = True

        # ----- RENDER
        screen.blit(background_image, (0, 0))
        draw = all_sprites_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.update(draw)
        draw_text(screen, ("Score: " + str(score)), 36, 100, 10)
        draw_text(screen, ("Life: " + str(life//100)), 36, 1500, 10)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()