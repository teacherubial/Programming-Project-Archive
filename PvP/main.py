"""
z6.py
"""

# python z6.py

import pygame
import random
import time

# --- Varibles and Constants

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 26, 117)
RED = (255, 0, 0)
HP = (0, 255, 128)
BLUE = (0, 0, 255)
SCOREBOARD = (89, 0, 153)
PLAYER_BACKGROUND = (191, 191, 191)
p1_color = (0, 0, 255)
p2_color = (255, 0, 0)
DEAD = (129, 49, 50)

screen_width = 1280
screen_height = 720
side = 20
side2 = -20
player_life = 4     # the actual player life is 1 more than the number
knock_back_distance = 100
moving_platform_speed = 1
full_ammo = 7
TIME_TO_RELOAD = 2000

background_image = pygame.image.load("background.jpg")

reloading = False
reloading2 = False


# --- Classes

class Platform(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Platform, self).__init__()

        self.image = pygame.image.load("platform.png")
        self.rect = self.image.get_rect()

class SmallPlatform(Platform):
    def __init__(self):
        super(SmallPlatform, self).__init__()

        self.image = pygame.image.load("SmallPlatform.png")
        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    def __init__(self):
        super(MovingPlatform, self).__init__()

        self.image = pygame.image.load("MovingPlatform.png")
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x > 1200:
            self.rect.x = -400
        self.rect.x += moving_platform_speed

class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        super(Hearts, self).__init__()

        self.image = pygame.image.load("Heart.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += moving_platform_speed

'''
# Add later

class Gun(Hearts):
    def __init__(self):
        super(Gun, self).__init__()

        self.image = pygame.image.load("p1.png")
        self.rect = self.image.get_rect()
'''

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super(Player, self).__init__()

        self.image = pygame.image.load("p1.png")
        self.life = player_life
        self.jump_count = 0
        self.hp_player1 = 160
        self.ammo = 7

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Moving Platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, moving_platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) == 1:
            self.rect.x += moving_platform_speed

        # Jump
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) == 1:
            self.jump_count = 0

        # Damage taken
        self.hit_response()

        # boundary
        self.boundary()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything (x axis)
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything (y axis)
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
        # Stop our vertical movement
            self.change_y = 0

        # Powerups update

        # hearts
        block_hit_list = pygame.sprite.spritecollide(self, hearts_list, True)
        for block in block_hit_list:
            hearts_list.remove(heart)
            all_sprites_list.remove(heart)
            self.life += 1

    def hit_response(self):
        player_hit_list = pygame.sprite.spritecollide(self, bullet_list, True)
        for bullet in player_hit_list:
            bullet_list.remove(bullet2)
            all_sprites_list.remove(bullet2)
            self.hp_player1 -= 16
            # knock back
            if bullet2.side2 == 20:
                self.rect.x += knock_back_distance
            else:
                self.rect.x -= knock_back_distance

    def boundary(self):
        if self.rect.y >= 800 or self.rect.x >= 1400 or self.rect.x <= -200 or self.hp_player1 <= 0:
            self.rect.y = -600
            self.rect.x = random.randrange(100, 1000)
            self.life -= 1
            self.change_y = 0
            self.hp_player1 = 160
            self.ammo = full_ammo

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = .8

        else:
            self.change_y += .5

    def jump(self):
        """ Double Jump """

        if self.jump_count == 0:
            self.change_y = -11
            self.jump_count = 1

        '''
        # Triple Jump Feature

        elif self.jump_count == 1:
            self.change_y = -10
            self.jump_count = 2
        '''



    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Player2(Player):

    def __init__(self):
        super(Player2, self).__init__()

        self.image = pygame.image.load("p2.png")
        self.hp_player2 = 160

    def hit_response(self):
        player_hit_list = pygame.sprite.spritecollide(self, bullet_list, True)
        for bullet in player_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            self.hp_player2 -= 16
            if bullet.side == 20:
                self.rect.x += knock_back_distance
            else:
                self.rect.x -= knock_back_distance

    def boundary(self):
        if self.rect.y >= 800 or self.rect.x >= 1400 or self.rect.x <= -200 or self.hp_player2 <= 0:
            self.rect.y = -600
            self.rect.x = random.randrange(100, 1000)
            self.life -= 1
            self.change_y = 0
            self.hp_player2 = 160
            self.ammo = full_ammo

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Bullet, self).__init__()

        self.image = pygame.image.load("fireball.png")
        self.side = side
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += self.side

class Bullet2(Bullet):
    def __init__(self):
        super(Bullet2, self).__init__()
        self.side2 = side2
        self.rect = self.image.get_rect()
    def update(self):
        """ Move the bullet. """
        self.rect.x += self.side2

# --- Functions

def socreboard():

    # board
    pygame.draw.rect(screen, SCOREBOARD, [300, 630, 270, 70], 0)
    pygame.draw.rect(screen, SCOREBOARD, [700, 630, 270, 70], 0)

    # Player image
    pygame.draw.rect(screen, PLAYER_BACKGROUND, [705, 635, 50, 60], 0)
    p1image = pygame.image.load("p1.png")
    p1imagerect = p1image.get_rect()
    p1imagerect.x = 710
    p1imagerect.y = 635
    screen.blit(p1image, p1imagerect)

    pygame.draw.rect(screen, PLAYER_BACKGROUND, [305, 635, 50, 60], 0)
    p1image = pygame.image.load("p2.png")
    p1imagerect = p1image.get_rect()
    p1imagerect.x = 310
    p1imagerect.y = 635
    screen.blit(p1image, p1imagerect)

    # Life bar
    pygame.draw.rect(screen, RED, [360, 670, 160, 20], 0)
    pygame.draw.rect(screen, RED, [760, 670, 160, 20], 0)

    # HP
    pygame.draw.rect(screen, HP, [360, 668, player2.hp_player2, 23], 0)
    pygame.draw.rect(screen, HP, [760, 668, player.hp_player1, 23], 0)

    # print life and magazine
    score_font = pygame.font.SysFont("comicsansms", 25)

    life_text = score_font.render("Life: " + str(int(player.life) + 1), 1, WHITE)
    screen.blit(life_text, (760, 630))

    life_text2 = score_font.render("Life: " + str(int(player2.life) + 1), 1, WHITE)
    screen.blit(life_text2, (360, 630))

    ammo_font = pygame.font.SysFont("comicsansms", 20)

    if reloading:
        mag_text = ammo_font.render("Reloading...", 1, WHITE)
    else:
        mag_text = ammo_font.render("Ammo: " + str(player.ammo) + "/7", 1, WHITE)
    screen.blit(mag_text, (855, 640))

    if reloading2:
        mag_text2 = ammo_font.render("Reloading...", 1, WHITE)
    else:
        mag_text2 = ammo_font.render("Ammo: " + str(player2.ammo) + "/7", 1, WHITE)
    screen.blit(mag_text2, (455, 640))



# Initialize Pygame
pygame.init()

# Set the height and width of the screen

screen = pygame.display.set_mode([screen_width, screen_height])

# --- Sprite lists

# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each platform in the game
platform_list = pygame.sprite.Group()

# List of each moving platform in the game
moving_platform_list = pygame.sprite.Group()

# List of each powerups in the game
hearts_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites

# This represents a block
platform1 = Platform()
platform2 = SmallPlatform()
platform3 = SmallPlatform()
platform4 = SmallPlatform()
platform5 = SmallPlatform()
platform6 = SmallPlatform()
moving_platform = MovingPlatform()

# All platforms
platform1.rect.x = 195
platform1.rect.y = 550

platform2.rect.x = 50
platform2.rect.y = 370

platform3.rect.x = 500
platform3.rect.y = 370

platform4.rect.x = 925
platform4.rect.y = 370

platform5.rect.x = 285
platform5.rect.y = 200

platform6.rect.x = 715
platform6.rect.y = 200

moving_platform.rect.x = -20
moving_platform.rect.y = 80

# Add the block to the list of objects
platform_list.add(platform1)
all_sprites_list.add(platform1)

platform_list.add(platform2)
all_sprites_list.add(platform2)

platform_list.add(platform3)
all_sprites_list.add(platform3)

platform_list.add(platform4)
all_sprites_list.add(platform4)

platform_list.add(platform5)
all_sprites_list.add(platform5)

platform_list.add(platform6)
all_sprites_list.add(platform6)

platform_list.add(moving_platform)
moving_platform_list.add(moving_platform)
all_sprites_list.add(moving_platform)

# Create player blocks
player = Player()
all_sprites_list.add(player)
player.rect.x = 940
player.rect.y = 280

player2 = Player2()
all_sprites_list.add(player2)
player2.rect.x = 200
player2.rect.y = 280

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------

while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
                side = -20
            if event.key == pygame.K_RIGHT:
                player.go_right()
                side = 20
            if event.key == pygame.K_UP:
                player.jump()
            if not reloading and event.key == pygame.K_SLASH and player.ammo > 0:
                player.ammo -= 1
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                # Set the bullet so it is where the player is
                if side == 20:
                    bullet.rect.x = player.rect.x + 50
                else:
                    bullet.rect.x = player.rect.x - 20

                bullet.rect.y = player.rect.y + 10
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

            if event.key == pygame.K_a:
                player2.go_left()
                side2 = -20
            if event.key == pygame.K_d:
                player2.go_right()
                side2 = 20
            if event.key == pygame.K_w:
                player2.jump()

            if not reloading2 and event.key == pygame.K_g and player2.ammo > 0:
                player2.ammo -= 1
                # Fire a bullet if the user clicks the mouse button
                bullet2 = Bullet2()
                # Set the bullet so it is where the player is
                if side2 == 20:
                    bullet2.rect.x = player2.rect.x + 50
                else:
                    bullet2.rect.x = player2.rect.x - 20
                bullet2.rect.y = player2.rect.y + 10
                # Add the bullet to the lists
                all_sprites_list.add(bullet2)
                bullet_list.add(bullet2)

            '''
            # End game option

            if player2.life < 0 or player.life < 0 and event.key == pygame.K_SPACE:
                player.life = player_life
                player2.life = player_life
                all_sprites_list.add(player)
                all_sprites_list.add(player2)
            '''

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()
            if event.key == pygame.K_a and player2.change_x < 0:
                player2.stop()
            if event.key == pygame.K_d and player2.change_x > 0:
                player2.stop()

    # --- Game logic

    # reload logic
    if player.ammo <= 0:
        lastReloadTime = pygame.time.get_ticks()
        reloading = True
        player.ammo = full_ammo
    if reloading and pygame.time.get_ticks() - lastReloadTime > TIME_TO_RELOAD:
        reloading = False

    if player2.ammo <= 0:
        lastReloadTime2 = pygame.time.get_ticks()
        reloading2 = True
        player2.ammo = full_ammo
    if reloading2 and pygame.time.get_ticks() - lastReloadTime2 > TIME_TO_RELOAD:
        reloading2 = False

    # randomly spawn power ups
    if moving_platform.rect.x == -200:
        rand_num = random.randrange(0, 2)
        if rand_num == 0:
            heart = Hearts()
            heart.rect.x = moving_platform.rect.x + 70
            heart.rect.y = moving_platform.rect.y - 50
            hearts_list.add(heart)
            all_sprites_list.add(heart)
        else:
            '''
            gun = Gun()
            gun.rect.x = moving_platform.rect.x + 70
            gun.rect.y = moving_platform.rect.y - 50
            hearts_list.add(gun)
            all_sprites_list.add(gun)
            '''
            pass
    # Call the update() method on all the sprites
    all_sprites_list.update()


    # Calculate mechanics for each bullet
    for bullets in bullet_list:

        # See if it hit a block
        platform_hit_list = pygame.sprite.spritecollide(bullets, platform_list, False)
        #For each block hit, remove the bullet
        for platform in platform_hit_list:
            bullet_list.remove(bullets)
            all_sprites_list.remove(bullets)

        # Remove the bullet if it flies up off the screen
        if bullets.rect.x < -10 or bullets.rect.x > screen_width:
            bullet_list.remove(bullets)
            all_sprites_list.remove(bullets)

    # Clear the screen
    screen.fill(WHITE)
    screen.blit(background_image, [0, 0])
    # Draw all the spites
    socreboard()
    all_sprites_list.draw(screen)

    # end game text
    end_game_font = pygame.font.SysFont("comicsansms", 150)
    dead_font = pygame.font.SysFont("comicsansms", 30)

    # End game
    if player2.life < 0:
        all_sprites_list.remove(player2)
        pygame.draw.rect(screen, DEAD, [300, 630, 270, 70], 0)
        player.life = 98
        death_text2 = end_game_font.render("Player 1 Wins", 1, MAGENTA)
        screen.blit(death_text2, (170, 270))

        dead2 = dead_font.render("Dead", 1, RED)
        screen.blit(dead2, (390, 640))
    elif player.life < 0:
        all_sprites_list.remove(player)
        pygame.draw.rect(screen, DEAD, [700, 630, 270, 70], 0)
        player2.life = 98
        death_text2 = end_game_font.render("Player 2 Wins", 1, MAGENTA)
        screen.blit(death_text2, (170, 270))

        dead = dead_font.render("Dead", 1, RED)
        screen.blit(dead, (790, 640))
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
