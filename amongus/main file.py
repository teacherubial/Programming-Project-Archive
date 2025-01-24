# Charles Zhang

import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (94, 243, 140)
YELLOW = (255, 255, 0)
MIDDLE_BLUE_PURPLE = (125, 122, 188)
WIDTH = 816
HEIGHT = 616
TITLE = "test subject"

# extra variables
play = False
tutorial = False
not_quit = True


# ----- Classes ------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./Sprites/right_player1-1.png")
        self.rect = self.image.get_rect()

        # ___Speed of the player___
        self.vel_x = 0
        self.vel_y = 0

        # direction variables
        self.facing_right = True
        self.hp = 3

        # Added this cause plagiarism :D
        # Supposed to be list of things the sprites bump into
        self.level = None

    def update(self):
        """Player's movement"""
        self.calc_grav()

        # ___Hit Reg___
        # _Horizontal_
        self.rect.x += self.vel_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # _Vertical_
        self.rect.y += self.vel_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.vel_y = 0

        if self.rect.right >= WIDTH - 8:
            self.rect.right = WIDTH - 9
        elif self.rect.x < 8:
            self.rect.x = 9

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT - 9
        elif self.rect.y < 8:
            self.rect.y = 9

    def calc_grav(self):
        """The Earth is flat things just fall"""
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6
        self.facing_right = False

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6
        self.facing_right = True

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0

    def duck_right(self):
        # width = 40
        # height = 60
        # self.image = pygame.Surface([width, height])
        # ___Hitbox___
        # self.image.fill(RED)
        self.image = pygame.Surface([40, 30])
        self.image.fill(RED)
        current_cords = (self.rect.x, self.rect.y + 30)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = current_cords

    def stand_up(self):
        current_cords = (self.rect.x, self.rect.y - 30)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = current_cords

class Right_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Sprites/Right_Bullet.png")

        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.x_vel = 7

    def update(self):
        self.rect.x += self.x_vel


class Left_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Sprites/Left_Bullet.png")

        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.x_vel = -7

    def update(self):
        self.rect.x += self.x_vel


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen, ):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLACK)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


class Field_01(Level):
    """ Definition for field 1. """

    def __init__(self, player):
        """ Create field 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform 616 - 816 player 40 - 60
        level = [
            # ____border____
            # __sides__
            [8, 616, 0, 0],
            [8, 616, 808, 0],
            # __ top and bottom__
            [816, 8, 0, 0],
            [816, 8, 0, HEIGHT - 8],
            # __map platforms__
            [100, 8, 8, 88],
            [100, 8, 708, 88],
            [200, 8, WIDTH / 2 - 100, 158],
            [100, 8, 108, 228],
            [100, 8, WIDTH - 208, 228],
            [100, 8, 8, 328],
            [100, 8, WIDTH - 108, 328],
            [100, 8, WIDTH / 2 - 200, 412],
            [100, 8, WIDTH / 2 + 100, 412],
            [100, 8, 8, HEIGHT - 120],
            [100, 8, WIDTH - 108, HEIGHT - 120],
            [50, 50, WIDTH / 2 - 25, HEIGHT - 88],
            [200, 180, WIDTH / 2 - 100, HEIGHT - 348]
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


class Tutorial(Level):
    """ Definition for tutorial. """

    def __init__(self, player):
        """ Create tutorial. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform 616 - 816 player 40 - 60
        level = [
            # ____border____
            # __sides__
            [8, 616, 0, 0],
            [8, 616, 808, 0],
            # __ top and bottom__
            [816, 8, 0, 0],
            [816, 8, 0, HEIGHT - 8],
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu(game):
    pygame.init()
    FONT = pygame.font.SysFont('arial', 24, False, False)

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    game.play = False
    game.tutorial = False

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game.play = True
                    done = True
                if event.key == pygame.K_t:
                    game.tutorial = True
                    done = True
                if event.key == pygame.K_ESCAPE:
                    done = True
                    game.not_quit = False

        # ----- LOGIC

        # ----- DRAW
        screen.fill(MIDDLE_BLUE_PURPLE)
        draw_text("main menu", FONT, BLACK, screen, WIDTH / 2 - 200, 20)
        draw_text("Press \"s\" to start the game", FONT, BLACK, screen, WIDTH / 2 - 200, 60)
        draw_text("press\"t\" to learn the controls", FONT, BLACK, screen, WIDTH / 2 - 200, 100)
        draw_text("press\"esc\" to quit the game", FONT, BLACK, screen, WIDTH / 2 - 200, 140)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


def tutorial():
    pygame.init()
    FONT = pygame.font.SysFont('arial', 24, False, False)

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ----- SPRITE GROUPS
    all_sprites = pygame.sprite.Group()
    bullet_sprites_pl1 = pygame.sprite.Group()
    bullet_sprites_pl2 = pygame.sprite.Group()
    player_1_sprites = pygame.sprite.Group()
    player_2_sprites = pygame.sprite.Group()

    player_1 = Player()
    player_2 = Player()
    player_1_sprites.add(player_1)
    player_2_sprites.add(player_2)

    player_1.image = pygame.image.load("Sprites/left_player1-1.png")
    player_1.facing_right = False
    player_2.image = pygame.image.load("Sprites/right_player2-1.png")

    # -----  FIELD LIST (add more here)
    field_list = []
    field_list.append(Tutorial(player_1))
    field_list.append(Tutorial(player_2))

    # ----- for field selection
    field_selected_num = 0
    field_selected = field_list[field_selected_num]
    player_1.level = field_selected
    player_2.level = field_selected

    all_sprites.add(player_1)
    all_sprites.add(player_2)

    # ----- Player's starting spawn point
    player_1.rect.x = 767
    player_1.rect.y = HEIGHT - player_1.rect.height - 10
    player_2.rect.x = 9
    player_2.rect.y = HEIGHT - player_2.rect.height - 10

    # ----- TUTORIAL LOOP _____________________________________________________
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    done = True
            # _____Player 1 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_1.go_left()
                    player_1.image = pygame.image.load("Sprites/left_player1-1.png")
                if event.key == pygame.K_RIGHT:
                    player_1.go_right()
                    player_1.image = pygame.image.load("Sprites/right_player1-1.png")
                if event.key == pygame.K_UP:
                    player_1.jump()
                if event.key == pygame.K_DOWN:
                    player_1.duck_right()
                if event.key == pygame.K_SLASH:
                    if player_1.facing_right:
                        bullet = Right_Bullet(player_1.rect.center[0] + 15, player_1.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl1.add(bullet)
                    elif not player_1.facing_right:
                        bullet = Left_Bullet(player_1.rect.center[0] - 15, player_1.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl1.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_1.vel_x < 0:
                    player_1.stop()
                if event.key == pygame.K_RIGHT and player_1.vel_x > 0:
                    player_1.stop()
                if event.key == pygame.K_DOWN:
                    if player_1.facing_right:
                        player_1.image = pygame.image.load("Sprites/left_player1-1.png")
                    elif not player_1.facing_right:
                        player_1.image = pygame.image.load("Sprites/left_player1-1.png")
                    player_1.stand_up

            # _____Player 2 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_2.go_left()
                    player_2.image = pygame.image.load("Sprites/left_player2-1.png")
                if event.key == pygame.K_d:
                    player_2.go_right()
                    player_2.image = pygame.image.load("Sprites/right_player2-1.png")
                if event.key == pygame.K_w:
                    player_2.jump()
                if event.key == pygame.K_q:
                    if player_2.facing_right:
                        bullet = Right_Bullet(player_2.rect.center[0] + 15, player_2.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl2.add(bullet)

                    elif not player_2.facing_right:
                        bullet = Left_Bullet(player_2.rect.center[0] - 15, player_2.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl2.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player_2.vel_x < 0:
                    player_2.stop()
                if event.key == pygame.K_d and player_2.vel_x > 0:
                    player_2.stop()

        # ----- LOGIC
        all_sprites.update()
        field_selected.update()

        # Check if bullet hits any platform then kill
        for bullet in bullet_sprites_pl1:
            bullet_hit_group = pygame.sprite.spritecollide(bullet, field_selected.platform_list, False)
            if len(bullet_hit_group) > 0:
                bullet.kill()

        for bullet in bullet_sprites_pl2:
            bullet_hit_group = pygame.sprite.spritecollide(bullet, field_selected.platform_list, False)
            if len(bullet_hit_group) > 0:
                bullet.kill()
        # Check if player 1 is hit by player 2 bullet

        for bullet in bullet_sprites_pl1:
            bullet_kill1_group = pygame.sprite.spritecollide(bullet, player_2_sprites, False)
            if len(bullet_kill1_group) > 0:
                if player_2.hp > 0:
                    player_2.vel_x = 0
                    player_2.vel_y = 0
                    player_2.rect.x = random.choice([9, 767])
                    player_2.rect.y = random.choice([542, 314, 484, 80])
                if player_2.hp < 1:
                    done = True
                    print("player1 Wins!")
                bullet.kill()

        for bullet in bullet_sprites_pl2:
            bullet_kill2_group = pygame.sprite.spritecollide(bullet, player_1_sprites, False)
            if len(bullet_kill2_group) > 0:
                if player_1.hp > 0:
                    player_1.vel_x = 0
                    player_1.vel_y = 0
                    player_1.rect.x = random.choice([9, 767])
                    player_1.rect.y = random.choice([542, 314, 484, 80])
                if player_1.hp < 1:
                    done = True
                    print("player2 Wins!")
                bullet.kill()

        # Checks if bullet hits bullet
        for bullet in bullet_sprites_pl1:
            bullet_bullet1_group = pygame.sprite.spritecollide(bullet, bullet_sprites_pl2, True)
            if len(bullet_bullet1_group) > 0:
                bullet.kill()
        for bullet in bullet_sprites_pl2:
            bullet_bullet2_group = pygame.sprite.spritecollide(bullet, bullet_sprites_pl1, True)
            if len(bullet_bullet2_group) > 0:
                bullet.kill()

        # ----- DRAW
        screen.fill(BLACK)
        field_selected.draw(screen)
        all_sprites.draw(screen)
        draw_text("Tutorial", FONT, WHITE, screen, WIDTH / 2 - 200, 20)
        draw_text("WAD for player 2 movement", FONT, WHITE, screen, WIDTH / 2 - 200, 60)
        draw_text("q to shoot for player 2", FONT, WHITE, screen, WIDTH / 2 - 200, 100)
        draw_text("arrow keys for player 1 movement", FONT, WHITE, screen, WIDTH / 2 - 200, 140)
        draw_text("/ to shoot for player 1", FONT, WHITE, screen, WIDTH / 2 - 200, 180)
        draw_text("press \"b\" to go back", FONT, WHITE, screen, WIDTH / 2 - 200, 220)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


def main(game):
    pygame.init()
    FONT = pygame.font.SysFont('arial', 24, False, False)

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    game.player1_win = False
    game.player2_win = False

    # ----- SPRITE GROUPS
    all_sprites = pygame.sprite.Group()
    bullet_sprites_pl1 = pygame.sprite.Group()
    bullet_sprites_pl2 = pygame.sprite.Group()
    player_1_sprites = pygame.sprite.Group()
    player_2_sprites = pygame.sprite.Group()

    player_1 = Player()
    player_2 = Player()
    player_1_sprites.add(player_1)
    player_2_sprites.add(player_2)

    player_1.image = pygame.image.load("Sprites/left_player1-1.png")
    player_1.facing_right = False
    player_2.image = pygame.image.load("Sprites/right_player2-1.png")

    # -----  FIELD LIST (add more here)
    field_list = []
    field_list.append(Field_01(player_1))
    field_list.append(Field_01(player_2))

    # ----- for field selection
    field_selected_num = 0
    field_selected = field_list[field_selected_num]
    player_1.level = field_selected
    player_2.level = field_selected

    all_sprites.add(player_1)
    all_sprites.add(player_2)

    # ----- Player's starting spawn point
    player_1.rect.x = 767
    player_1.rect.y = HEIGHT - player_1.rect.height - 10
    player_2.rect.x = 9
    player_2.rect.y = HEIGHT - player_2.rect.height - 10

    # ----- MAIN LOOP _____________________________________________________
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # _____Player 1 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_1.go_left()
                    player_1.image = pygame.image.load("Sprites/left_player1-1.png")
                if event.key == pygame.K_RIGHT:
                    player_1.go_right()
                    player_1.image = pygame.image.load("Sprites/right_player1-1.png")
                if event.key == pygame.K_UP:
                    player_1.jump()
                if event.key == pygame.K_SLASH:
                    if player_1.facing_right:
                        bullet = Right_Bullet(player_1.rect.center[0] + 15, player_1.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl1.add(bullet)
                    elif not player_1.facing_right:
                        bullet = Left_Bullet(player_1.rect.center[0] - 15, player_1.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl1.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_1.vel_x < 0:
                    player_1.stop()
                if event.key == pygame.K_RIGHT and player_1.vel_x > 0:
                    player_1.stop()

            # _____Player 2 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_2.go_left()
                    player_2.image = pygame.image.load("Sprites/left_player2-1.png")
                if event.key == pygame.K_d:
                    player_2.go_right()
                    player_2.image = pygame.image.load("Sprites/right_player2-1.png")
                if event.key == pygame.K_w:
                    player_2.jump()
                if event.key == pygame.K_q:
                    if player_2.facing_right:
                        bullet = Right_Bullet(player_2.rect.center[0] + 15, player_2.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl2.add(bullet)

                    elif not player_2.facing_right:
                        bullet = Left_Bullet(player_2.rect.center[0] - 15, player_2.rect.center[1] - 10)
                        all_sprites.add(bullet)
                        bullet_sprites_pl2.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player_2.vel_x < 0:
                    player_2.stop()
                if event.key == pygame.K_d and player_2.vel_x > 0:
                    player_2.stop()

        # ----- LOGIC
        all_sprites.update()
        field_selected.update()

        # Check if bullet hits any platform then kill
        for bullet in bullet_sprites_pl1:
            bullet_hit_group = pygame.sprite.spritecollide(bullet, field_selected.platform_list, False)
            if len(bullet_hit_group) > 0:
                bullet.kill()

        for bullet in bullet_sprites_pl2:
            bullet_hit_group = pygame.sprite.spritecollide(bullet, field_selected.platform_list, False)
            if len(bullet_hit_group) > 0:
                bullet.kill()
        # Check if player 1 is hit by player 2 bullet

        for bullet in bullet_sprites_pl1:
            bullet_kill1_group = pygame.sprite.spritecollide(bullet, player_2_sprites, False)
            if len(bullet_kill1_group) > 0:
                if player_2.hp > 0:
                    player_2.hp -= 1
                    player_1.hp += 1
                    player_2.vel_x = 0
                    player_2.vel_y = 0
                    player_2.rect.x = random.choice([9, 767])
                    player_2.rect.y = random.choice([542, 314, 484, 80])
                if player_2.hp < 1:
                    game.player1_win = True
                    done = True
                    print("player1 Wins!")
                bullet.kill()

        for bullet in bullet_sprites_pl2:
            bullet_kill2_group = pygame.sprite.spritecollide(bullet, player_1_sprites, False)
            if len(bullet_kill2_group) > 0:
                if player_1.hp > 0:
                    player_1.hp -= 1
                    player_2.hp += 1
                    player_1.vel_x = 0
                    player_1.vel_y = 0
                    player_1.rect.x = random.choice([9, 767])
                    player_1.rect.y = random.choice([542, 314, 484, 80])
                if player_1.hp < 1:
                    game.player2_win = True
                    done = True
                    print("player2 Wins!")
                bullet.kill()

        # Checks if bullet hits bullet
        for bullet in bullet_sprites_pl1:
            bullet_bullet1_group = pygame.sprite.spritecollide(bullet, bullet_sprites_pl2, True)
            if len(bullet_bullet1_group) > 0:
                bullet.kill()
        for bullet in bullet_sprites_pl2:
            bullet_bullet2_group = pygame.sprite.spritecollide(bullet, bullet_sprites_pl1, True)
            if len(bullet_bullet2_group) > 0:
                bullet.kill()

        # ----- DRAW
        screen.fill(BLACK)
        field_selected.draw(screen)
        all_sprites.draw(screen)
        draw_text(str(player_2.hp), FONT, WHITE, screen, 9, 20)
        draw_text(str(player_1.hp), FONT, WHITE, screen, WIDTH - 20, 20)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


def player1_win():
    pygame.init()
    FONT = pygame.font.SysFont('arial', 24, False, False)

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    done = True

        # ----- LOGIC

        # ----- DRAW
        screen.fill(MIDDLE_BLUE_PURPLE)
        draw_text("Player 1 wins :D", FONT, BLACK, screen, WIDTH / 2 - 200, 20)
        draw_text("press \"b\" to go back to menu", FONT, BLACK, screen, WIDTH / 2 - 200, 60)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def player2_win():
    pygame.init()
    FONT = pygame.font.SysFont('arial', 24, False, False)

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    done = True

        # ----- LOGIC

        # ----- DRAW
        screen.fill(MIDDLE_BLUE_PURPLE)
        draw_text("Player 2 wins :D", FONT, BLACK, screen, WIDTH / 2 - 200, 20)
        draw_text("press \"b\" to go back to menu", FONT, BLACK, screen, WIDTH / 2 - 200, 60)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)


class menu:
    def __init__(self):
        self.tutorial = False
        self.play = False
        self.not_quit = True
        self.player2_win = False
        self.player1_win = False


if __name__ == "__main__":
    game = menu()

    while game.not_quit:
        main_menu(game)
        if game.play:
            main(game)
            if game.player1_win:
                player1_win()
            if game.player2_win:
                player2_win()
        elif game.tutorial:
            tutorial()

    pygame.quit()
