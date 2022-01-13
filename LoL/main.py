import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
GREEN = (96, 171, 154)
WIDTH = 1920
HEIGHT = 1080
PLAYER_SPEED = 3
PLAYER_DASH_SPEED = 7

TITLE = "<Draven>"

font_name = pygame.font.match_font('arial')



def score_board(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/background.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/draven.png")
        self.rect = self.image.get_rect()

        # Sets sprite location
        self.rect.centerx = (WIDTH // 10)
        self.rect.centery = (HEIGHT // 2)

        self.vel_x = 0
        self.vel_y = 0

        self.player_speed = 3

    def update(self):
        self.rect.x += self.vel_x * self.player_speed
        self.rect.y += self.vel_y * self.player_speed

    # Controls for up and down
    def go_up(self):
        self.vel_y = -4

    def go_down(self):
        self.vel_y = 4

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0


class Axe(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.image = pygame.image.load("./images/axe.png")
        self.image = pygame.transform.scale(self.image, (100, 140))

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = coords

        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord, vel_x, vel_y):
        super().__init__()

        self.image = pygame.image.load("./images/minion.png")
        self.image = pygame.transform.scale(self.image, (105, 86))

        self.rect = self.image.get_rect()

        self.vel_x = vel_x
        self.vel_y = vel_y

        self.rect.centerx = (x_coord)
        self.rect.centery = (y_coord)


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

class Teemo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/teemo.png")
        self.image = pygame.transform.scale(self.image, (137, 192))
        self.rect = self.image.get_rect()


        self.rect.centerx = WIDTH + 200
        self.rect.centery = HEIGHT // 2



        self.vel_x = 0
        self.vel_y = 0

        self.reached_middle = False

    def update(self):

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.centerx == WIDTH - 200 and not self.reached_middle:
            self.stop()
            self.vel_y = 4
            self.reached_middle = True
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.vel_y *= -1

    def stop(self):
        self.vel_x = 0



class Mushroom(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        self.image = pygame.image.load("./images/mushroom.png")
        self.image = pygame.transform.scale(self.image, (75, 72))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = coords

        self.rect.centerx = WIDTH - 200


        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x




def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    score = 0
    health = 1000
    bool = True
    teemo_spawned = False
    axe_counter = []

    # ---- SPAWN TIMES
    mushroom_spawn_time = 1000
    last_time_mushroom_spawned = pygame.time.get_ticks()

    minion_spawn_time = 500
    last_time_minion_spawned = pygame.time.get_ticks()

    # ---- SPRITE GROUPS

    all_sprites_group = pygame.sprite.RenderUpdates()
    background_group = pygame.sprite.Group()
    axe_sprites = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    mushroom_group = pygame.sprite.Group()

    # Player creation
    player = Player()
    all_sprites_group.add(player)

    # Teemo creation
    teemo = Teemo()
    all_sprites_group.add(teemo)

    # Background creation
    background = Background()
    background_group.add(background)

    # ----- MAIN LOOP


    pygame.mixer.music.load("./assets/backgroundmusic.mp3")
    pygame.mixer.music.play(-1)

    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # ---- CONTROLS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.vel_x = PLAYER_SPEED
                    player.image = pygame.image.load("./images/draven.png")
                    bool = True
                if event.key == pygame.K_LEFT:
                    player.vel_x = -PLAYER_SPEED
                    player.image = pygame.image.load("./images/dravenflipped.png")
                    bool = False
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()

                # ----Abilities

               # Axe (Q)
                if event.key == pygame.K_q and bool and len(axe_sprites) < 5:
                    axe = Axe(player.rect.midbottom)
                    all_sprites_group.add(axe)
                    axe_sprites.add(axe)
                    axe.vel_x = 10
                if event.key == pygame.K_q and not bool and len(axe_sprites) < 5:
                    axe = Axe(player.rect.midbottom)
                    all_sprites_group.add(axe)
                    axe_sprites.add(axe)
                    axe.vel_x = -10

                # Dash (w)
                if event.key == pygame.K_w:
                    player.player_speed = PLAYER_DASH_SPEED


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.vel_y < 0:
                    player.stop()
                if event.key == pygame.K_DOWN and player.vel_y > 0:
                    player.stop()
                if event.key == pygame.K_w and player.player_speed == PLAYER_DASH_SPEED:
                    player.player_speed = PLAYER_SPEED

        # Makes sure player is not out of screen (x-axis)
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.left < 0:
            player.rect.left = 0

        # Makes sure player is not out of screen (y-axis)
        if player.rect.bottom > HEIGHT:
            player.rect.bottom = HEIGHT
        if player.rect.top < 0:
            player.rect.top = 0

        # ----- LOGIC
        all_sprites_group.update()


        # Ends game if health is less than 0
        if health <= 0:
            done = True

        if health > 0 and not teemo_spawned:
            if pygame.time.get_ticks() > last_time_minion_spawned + minion_spawn_time:
                last_time_minion_spawned = pygame.time.get_ticks()

                enemy = Enemy(WIDTH, random.randrange(50, HEIGHT), random.randrange(-2, -1), 0)
                all_sprites_group.add(enemy)
                enemy_group.add(enemy)



        # Mushroom spawner
        if health >= 0 and teemo_spawned:
            if pygame.time.get_ticks() >  last_time_mushroom_spawned + mushroom_spawn_time:
                last_time_mushroom_spawned = pygame.time.get_ticks()

                mushroom = Mushroom(teemo.rect.midbottom)
                mushroom.vel_x  = -5
                all_sprites_group.add(mushroom)
                mushroom_group.add(mushroom)

            for mushroom in mushroom_group:
                if mushroom.rect.right < 0:
                    mushroom.kill()

                mushrooms_hit_player = pygame.sprite.spritecollide(player, mushroom_group, True)
                if len(mushrooms_hit_player) > 0:
                    health -= 50
                    mushroom.kill()



        # Check if axe collided with minions and mushroom
        for axe in axe_sprites:

            if axe.rect.right > WIDTH or axe.rect.right <0:
                axe.kill()

            enemy_hit_group = pygame.sprite.spritecollide(axe, enemy_group, True)
            if len(enemy_hit_group) > 0:
                axe.kill()
            for i in enemy_hit_group:
                score += 50

        for mushroom in mushroom_group:
            mushroom_hit_axe = pygame.sprite.spritecollide(mushroom, axe_sprites, True)
            if len(mushroom_hit_axe) > 0:
                mushroom.kill()
                axe.kill()
                score += 50

        # Check if player collided with enemy
        for enemy in enemy_group:

            enemy_hit_player_group = pygame.sprite.spritecollide(player, enemy_group, True)
            # Counts score
            for i in enemy_hit_player_group:
                score += 10
                health -= 50
                print(health)

            # Spawns stronger Enemy once score is reached
            if score >= 500 and not teemo_spawned:
                teemo.vel_x = -5
                teemo_spawned = True


        # ----- DRAW
        background_group.draw(screen)
        all_sprites_group.draw(screen)

        score_board(screen, f"Score: {score}", 50, WIDTH - 100, 10)
        score_board(screen, f"Health: {health}", 50, WIDTH - 400, 10)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()