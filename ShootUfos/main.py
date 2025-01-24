# Angelo Wang

import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 1000
TITLE = "Shoot UFOs"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/starship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Rect
        self.rect = self.image.get_rect()

        # Speed
        self.xvel = 0

    def update(self):
        # Move left/right
        self.rect.x += self.xvel

        # Don't let go out of screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.image.get_width():
            self.rect.x = WIDTH - self.image.get_width()

    # Player movement
    def go_left(self):
        self.xvel = -5

    def go_right(self):
        self.xvel = 5

    def stop(self):
        self.xvel = 0


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # parameters
        width = 5
        height = 10

        # image
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        # rect
        self.rect = self.image.get_rect()

        # Speed
        self.yvel = 0

    def update(self):
        self.rect.y += self.yvel

    def go_up(self):
        self.yvel = -20

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/ufo.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Rect
        self.rect = self.image.get_rect()

        # Velocity
        self.xvel = random.choice([-5, 5])

    def update(self):
        # Move left/right
        self.rect.x += self.xvel

        # Don't let go out of screen
        if self.rect.x < 0:
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()
        if self.rect.x > WIDTH - self.image.get_width():
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()
        if self.rect.y > HEIGHT/3 and self.rect.y < (HEIGHT/3) * 2:
            if self.xvel < 0:
                self.xvel = -10
            else:
                self.xvel = 10
        if self.rect.y > HEIGHT - HEIGHT/3:
            if self.xvel < 0:
                self.xvel = -15
            else:
                self.xvel = 15

class SuperEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/superenemy.png")
        self.image = pygame.transform.scale(self.image, (75, 75))

        # Rect
        self.rect = self.image.get_rect()

        # Velocity
        self.xvel = random.choice([-10, 10])

    def update(self):
        # Move left/right
        self.rect.x += self.xvel

        # Don't let go out of screen
        if self.rect.x < 0:
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()
        if self.rect.x > WIDTH - self.image.get_width():
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()
        if self.rect.y > HEIGHT/3 and self.rect.y < (HEIGHT/3) * 2:
            if self.xvel < 0:
                self.xvel = -15
            else:
                self.xvel = 15
        if self.rect.y > HEIGHT - HEIGHT/3:
            if self.xvel < 0:
                self.xvel = -20
            else:
                self.xvel = 20

class Mothership(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/mothership.png")
        self.image = pygame.transform.scale(self.image, (300, 150))

        # Rect
        self.rect = self.image.get_rect()

        # Velocity
        self.xvel = random.choice([-2, 2])

        # Health
        self.health = 10
        self.last_laser_fired = pygame.time.get_ticks()

    def update(self):
        # Move left/right
        self.rect.x += self.xvel

        # Don't let go out of screen
        if self.rect.x < 0:
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()
        if self.rect.x > WIDTH - self.image.get_width():
            self.xvel *= -1
            self.rect.y = self.rect.y + self.image.get_height()

class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/laserball.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        # Rect
        self.rect = self.image.get_rect()

        # Velocity
        self.xvel = 5
        self.yvel = 5

        # Health
        self.health = 2

    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel

# class Shield(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#
#         self.image = pygame.image.load("./assets/shield.png")
#         self.image = pygame.transform.scale(self.image, (100, 50))
#
#         self.rect = self.image.get_rect()
#
#         self.health = 10
#
#     def update(self):
#         if self.health == 0:
#             self.kill()

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
    default_font = pygame.font.SysFont("Menlo", 20)
    laser_sound = pygame.mixer.Sound("./assets/laser.ogg")
    death_sound = pygame.mixer.Sound("./assets/dead.ogg")

    # Create starship
    starship = Player()

    # Create laser
    laser = Laser()

    # Create enemy
    enemy = Enemy()

    # Create shield

    # Set the coordinates of starship
    starship.rect.x = WIDTH/2 - starship.rect.width/2
    starship.rect.y = 900

    laser.rect.y = 925

    enemy.rect.x = random.randrange(0, WIDTH-enemy.image.get_width())
    enemy.rect.y = 0

    # all sprites group
    all_sprites_group = pygame.sprite.Group()
    laser_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()
    superenemy_sprites_group = pygame.sprite.Group()
    mothership_sprites_group = pygame.sprite.Group()
    enemylaser_sprites_group = pygame.sprite.Group()
    shield_sprites_group = pygame.sprite.Group()

    # add starship
    all_sprites_group.add(starship)
    all_sprites_group.add(laser)
    all_sprites_group.add(enemy)
    laser_sprites_group.add(laser)
    enemy_sprites_group.add(enemy)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    starship.go_left()
                if event.key == pygame.K_RIGHT:
                    starship.go_right()
                if event.key == pygame.K_SPACE:
                    laser.go_up()
                    laser = Laser()
                    all_sprites_group.add(laser)
                    laser_sprites_group.add(laser)
                    laser.rect.y = 925
                    laser_sound.play()
                    # if laser.rect.y < 925:
                    #     laser.rect.x = laser.rect.x
                    # else:
                    #     laser.rect.x = starship.rect.x + starship.rect.width / 2 - 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and starship.xvel < 0:
                    starship.stop()
                if event.key == pygame.K_RIGHT and starship.xvel > 0:
                    starship.stop()
        if laser.rect.y < 925:
            laser.rect.x = laser.rect.x
        else:
            laser.rect.x = starship.rect.x + starship.rect.width / 2 - 2

        # ----- LOGIC
        # Update
        all_sprites_group.update()

        # Collision
        killed_enemy = pygame.sprite.groupcollide(laser_sprites_group, enemy_sprites_group, True, True)
        killed_superenemy = pygame.sprite.groupcollide(laser_sprites_group, superenemy_sprites_group, True, True)

        # Kill mothership
        if pygame.sprite.groupcollide(laser_sprites_group, mothership_sprites_group, True, False):
            mothership.health -= 1
            if mothership.health == 0:
                mothership.kill()
                score += 5
                death_sound.play()

        # Kill laser
        if pygame.sprite.groupcollide(enemylaser_sprites_group, laser_sprites_group, True, True):
            enemylaser.health -= 1
            if enemylaser.health == 0:
                enemylaser.kill()
                death_sound.play()

        # Add score when enemy killed
        if len(killed_enemy) > 0:
            score += 1
            death_sound.play()

            for i in range(score):
                if len(enemy_sprites_group) > 10:
                    pass
                else:
                    enemy = Enemy()
                    enemy_sprites_group.add(enemy)
                    all_sprites_group.add(enemy)

        # Superenemy kill points
        if len(killed_superenemy) > 0:
            score += 2
            death_sound.play()

        # Spawn superenemy
        if score > 50:
            if len(superenemy_sprites_group) > 3:
                pass
            else:
                superenemy = SuperEnemy()
                all_sprites_group.add(superenemy)
                superenemy_sprites_group.add(superenemy)

        # Spawn mothership
        if score > 100:
            if len(mothership_sprites_group) == 1:
                if pygame.time.get_ticks() - mothership.last_laser_fired > 500:
                    enemylaser = EnemyLaser()
                    enemylaser.rect.x = mothership.rect.x + mothership.rect.width / 2.25
                    enemylaser.rect.y = mothership.rect.y + 100
                    all_sprites_group.add(enemylaser)
                    enemylaser_sprites_group.add(enemylaser)
                    enemylaser2 = EnemyLaser()
                    enemylaser2.rect.x = mothership.rect.x + mothership.rect.width / 2.25
                    enemylaser2.rect.y = mothership.rect.y + 100
                    all_sprites_group.add(enemylaser2)
                    enemylaser_sprites_group.add(enemylaser2)
                    enemylaser2.xvel *= -1
                    enemylaser3 = EnemyLaser()
                    enemylaser3.rect.x = mothership.rect.x + mothership.rect.width / 2.25
                    enemylaser3.rect.y = mothership.rect.y + 100
                    all_sprites_group.add(enemylaser3)
                    enemylaser_sprites_group.add(enemylaser3)
                    enemylaser3.xvel *= 0

                    mothership.last_laser_fired = pygame.time.get_ticks()
            else:
                mothership = Mothership()
                all_sprites_group.add(mothership)
                mothership_sprites_group.add(mothership)
            if laser.rect.y < 925:
                laser.rect.x = laser.rect.x
            else:
                laser.rect.x = starship.rect.x + starship.rect.width / 2 - 2

        # Die
        if pygame.sprite.spritecollide(starship, enemy_sprites_group, True) or pygame.sprite.spritecollide(starship, superenemy_sprites_group, True) or pygame.sprite.spritecollide(starship, mothership_sprites_group, True) or pygame.sprite.spritecollide(starship, enemylaser_sprites_group, True):
            done = True
            print(f"Final Score: {score}")

        # ----- RENDER
        screen.fill(BLACK)

        all_sprites_group.draw(screen)

        # Score
        score_display = default_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_display, (10, 10))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()