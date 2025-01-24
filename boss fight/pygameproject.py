import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Boss Fight 2022"
HEART = pygame.transform.scale(pygame.image.load("./assets/heart_sprite.png"), (40, 40))
DEFEAT = pygame.transform.scale(pygame.image.load("./assets/defeat_screen.jpg"), (WIDTH, HEIGHT))
VICTORY = pygame.transform.scale(pygame.image.load("./assets/victory_screen.jpg"), (WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/space_player.png")
        # Resize
        self.image = pygame.transform.scale(
            self.image,
            (75, 75),
        )

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = [(WIDTH/2), (HEIGHT/2 + 100)]

        # Movement
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Move the player sprite based on arrow key input
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    # Player-controlled movement(taken from platformexample.py and modified for up and down):
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
    def go_up(self):
        """ Called when user hits up arrow"""
        self.change_y = -5
    def go_down(self):
        """ Called when user hits down arrow"""
        self.change_y = 5
    def stop_x(self):
        """ Called when the user lets off the keyboard in left or right directions. """
        self.change_x = 0
    def stop_y(self):
        """ Called when the user lets off the keyboard in left or right directions. """
        self.change_y = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, center: list):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/bullet_sprite.png")
        # Rotate the image by 90 degrees
        self.image = pygame.transform.rotate(self.image, 270)
        # Resize
        self.image = pygame.transform.scale(
            self.image,
            (25, 25),
        )

        self.rect = self.image.get_rect()
        self.rect.x = center[0]
        self.rect.y = center[1]

        self.radius = self.rect.width // 2

    def update(self):
        """ The basic path of the bullet """
        self.yvel = -5
        self.rect.y += self.yvel

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/boss_sprite_cropped.png")
        # Resize
        self.image = pygame.transform.scale(
            self.image,
            (200, 200),
        )

        # Rect
        self.rect = self.image.get_rect()
        self.rect.center = [(WIDTH / 2), (HEIGHT / 2 - 150)]

        self.radius = self.rect.width // 2 - 10

        # Movement
        self.change_x = 2
        self.change_y = 2

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y



class Sword_vertical(pygame.sprite.Sprite):
    def __init__(self, center: list):
        super().__init__()

        # Image
        self.image = pygame.image.load("assets/phase_one_sword.png")
        # Rotate
        self.image = pygame.transform.rotate(self.image, 180)
        # Resize
        self.image = pygame.transform.scale(
            self.image,
            (70, 70),
        )

        # Rect
        self.rect = self.image.get_rect()
        self.rect.x = center[0]
        self.rect.y = center[1]

        # Movement
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.y += self.change_y
        self.change_y += 0.1

        if self.rect.y > HEIGHT:
            self.rect.center = random_coords()
            self.change_y = 0

class Health_boss(pygame.sprite.Sprite):
    def __init__(self, width: int):
        super().__init__()

        # Image
        self.image = pygame.Surface([750, 30])
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 20
        self.boss_health_left = 750

    def update(self):
        """ make a health bar with a width representative of the boss's remaining health"""
        self.image.fill([128, 128, 128])
        pygame.draw.rect(self.image, [149, 53, 83], [0, 0, self.boss_health_left, self.rect.height])


def random_coords():
    x, y, = (
        random.randrange(0, WIDTH),
        random.randrange(-150, 50)
    )
    return x, y


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    gun_sound = pygame.mixer.Sound("./assets/lasersound.mp3")

    # Create a sprite group for the player
    player = Player()
    boss = Boss()

    # number of swords spawned
    num_swords = 7

    # starting number of lives
    lives = 3

    # Add the sprite group to all_sprite_groups
    all_sprites_group = pygame.sprite.Group()
    all_sprites_group.add(player)
    all_sprites_group.add(boss)
    bullet_sprites_group = pygame.sprite.Group()
    boss_sprites_group = pygame.sprite.Group()
    boss_sprites_group.add(boss)
    sword_sprites_group = pygame.sprite.Group()
    for i in range(num_swords):
        sword = Sword_vertical(random_coords())
        all_sprites_group.add(sword)
        sword_sprites_group.add(sword)
    health_boss = Health_boss(100)
    all_sprites_group.add(health_boss)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Shoot a bullet when the space key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet([player.rect.x, player.rect.y])
                    all_sprites_group.add(bullet)
                    bullet_sprites_group.add(bullet)
                    gun_sound.play()

            # Control movement based on arrow key input(taken from platformexample.py)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop_x()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop_x()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop_y()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop_y()



        # ----- LOGIC
        all_sprites_group.update()

        # Deal with bullets colliding with the boss sprite
        # BULLETS collides with any sprite from BOSS_SPRITE_GROUP
        for bullet in bullet_sprites_group:
            # Handle all bullet collision inside this for loop
            collided_bullet = pygame.sprite.spritecollide(boss, bullet_sprites_group, True, pygame.sprite.collide_circle)

            if len(collided_bullet) > 0:
                # some collision has happened
                health_boss.boss_health_left -= 10

        # ENEMY collides with PLAYER
        collided_player = pygame.sprite.spritecollide(player, sword_sprites_group, True, pygame.sprite.collide_rect_ratio(0.7))

        # take away one life from the player if they are hit by an enemy attack
        if len(collided_player) > 0:
            lives -= 1

        # don't let the boss move off the screen
        if boss.rect.x >= WIDTH - 200 or boss.rect.x <= 0:
            boss.change_x *= -1
        if boss.rect.y >= ((HEIGHT / 2) - 150) or boss.rect.y <= 0:
            boss.change_y *= -1

        # ----- RENDER
        screen.fill(BLACK)
        all_sprites_group.draw(screen)

        # decorate the boss's health bar

        # put hearts on the screen representing the amount of lives the player has
        if lives == 5:
            screen.blit(HEART, (WIDTH - 205, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 165, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 125, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 85, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 45, HEIGHT - 45))

        if lives == 4:
            screen.blit(HEART, (WIDTH - 165, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 125, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 85, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 45, HEIGHT - 45))

        if lives == 3:
            screen.blit(HEART, (WIDTH - 125, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 85, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 45, HEIGHT - 45))

        elif lives == 2:
            screen.blit(HEART, (WIDTH - 85, HEIGHT - 45))
            screen.blit(HEART, (WIDTH - 45, HEIGHT - 45))

        elif lives == 1:
            screen.blit(HEART, (WIDTH - 45, HEIGHT - 45))

        # blit a defeat screen if the player runs out of lives
        elif lives <= 0:
            screen.blit(DEFEAT, (0, 0))

        # blit a victory screen if the boss runs out of health
        if health_boss.boss_health_left <= 0:
            screen.blit(VICTORY, (0, 0))


        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()