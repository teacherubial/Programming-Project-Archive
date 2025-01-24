import pygame
import random
import time

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Joypack Jetride"
GRAVITY = 0.4
THRUST = 0.9

score = 0

class Player(pygame.sprite.Sprite):
    """This class is the jetpack man that the player controls"""

    # Methods
    def __init__(self):
        """Constructor"""
        super().__init__()

        # Create the image
        self.image = pygame.image.load("./assets/running_man.png")
        self.image = pygame.transform.scale(self.image, (60, 110)) # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        # Position/Speed vectors (x and dx are constant 0)
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.dy = 0
        self.acceleration = 0     # 2 possible values: Thrust on and thrust off

    def update(self):
        """Move the player"""
        # Move up/down
        self.rect.y += self.dy

        # Update sprite based on player's vertical movement/status
        if self.rect.bottom == HEIGHT:                                     # Player is on ground
            if score % 2 == 0:
                self.image = pygame.image.load("./assets/running_man.png")
            else:
                self.image = pygame.image.load("./assets/running_man2.png")
            self.image = pygame.transform.scale(self.image, (60, 110))     # Scale

        elif self.rect.bottom < HEIGHT and self.acceleration != THRUST:
            self.image = pygame.image.load("./assets/falling_man.png")     # Player is falling down
            self.image = pygame.transform.scale(self.image, (60, 110))     # Scale

        # Gravity
        self.calc_grav()


    def calc_grav(self):
        """Calculate gravity and update the speed vector"""
        # Add the gravity unit to the dy
        self.acceleration = GRAVITY
        self.dy += self.acceleration

        # Check if player on ground
        if self.rect.y >= HEIGHT - self.rect.height and self.dy >= 0:
            self.dy = 0
            self.rect.y = HEIGHT - self.rect.height

        # Check if player on ceiling
        if self.rect.y <= 0:
            self.dy = 1
            self.rect.y = 0

    def fly(self):
        """Called when the user hits the space bar. The player moves up at constant acceleration"""
        self.acceleration = THRUST
        self.dy -= self.acceleration

        # Change the sprite to a jetpack flying man
        self.image = pygame.image.load("./assets/flying_man.png")
        self.image = pygame.transform.scale(self.image, (60, 110))  # Scale


class Obstacle(pygame.sprite.Sprite):
    """Class is obstacles that a player faces on the screen"""
    def __init__(self):
        """
        :param height: height of the knife in px
        """
        super().__init__()

        # Create the image
        self.image = pygame.image.load("./assets/knife.png")
        self.image = pygame.transform.scale(self.image, (12, 100))  # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        # Set the coords off the screen
        self.rect.center = self.random_coords()
        self.rect.x = random.randrange(WIDTH, WIDTH*2)

        # Set the initial xvelocity
        self.dx = -5

    def update(self):
        """Change the x coordinate by its dx"""
        self.rect.x += self.dx

        # Recycle the obstacle by setting its position back off the screen
        if self.rect.x <= 0:
            self.rect.center = self.random_coords()

        if score % 100 == 0 and score != 0:
            self.speed_up()

    def random_coords(self):
        """Returns a random set of coordinates off the screen to the right"""
        return [
            random.randrange(WIDTH + 10, WIDTH + 300),
            random.randrange(0 + self.rect.height / 2, HEIGHT - self.rect.height / 2)
        ]

    def speed_up(self):
        """Speed up the obstacles when the function is called"""
        self.dx -= 0.2

class Background(pygame.sprite.Sprite):
    """The scrolling background"""

    # Methods
    def __init__(self, x):
        """Constructor"""
        super().__init__()

        # Create the image
        self.image = pygame.image.load("./assets/backdrop.png")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT)) # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.dx = -4


    def update(self):
        self.rect.x += self.dx
        if self.rect.x <= self.image.get_width() * -1:
            self.rect.x = self.image.get_width()

def game_loop():
    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # Create sprite groups
    player_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    background1 = Background(0)
    background2 = Background(WIDTH)
    background_group = pygame.sprite.Group()
    background_group.add(background1)
    background_group.add(background2)

    # Create player and add to group
    player = Player()
    player_group.add(player)

    # Create obstacles and add to group
    for i in range(4):
        obstacle = Obstacle()
        obstacle_group.add(obstacle)



    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    space_bar_pressed = False
    time_until_score = 0
    global score
    GAME_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 20)
    game_music = pygame.mixer.Sound("./assets/game_music.wav")

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Check for user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_bar_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_bar_pressed = False

        # Make the player fly if the space key is pressed
        if space_bar_pressed:
            player.fly()

        # ----- LOGIC
        player_group.update()
        obstacle_group.update()
        background_group.update()

        # Play the game music
        pygame.mixer.Sound.play(game_music)

        # If a player group collides with an obstacle group end the game
        collided_player = pygame.sprite.spritecollide(player, obstacle_group, dokill=True)
        if len(collided_player) > 0:
            player.image = pygame.image.load("./assets/dying_man.png")
            player.image = pygame.transform.scale(player.image, (60, 110))  # Scale

            done = True

        # Update the score every time_until_score iterations of the while loop
        if time_until_score == 6:
            score += 1
            time_until_score = 0

            # Every time the score reaches a certain amount, speed up the obstacles
            if score % 100 == 0:
                obstacle_group.update()
        time_until_score += 1

        # ----- RENDER
        screen.fill(BLACK)
        background_group.draw(screen)
        player_group.draw(screen)
        obstacle_group.draw(screen)



        # Display the score on the top left of the screen
        score_surf = GAME_FONT.render(f"SCORE:{score}", True, WHITE)
        screen.blit(score_surf, (0, 0))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)


def end_game_loop() -> bool:
    """Returns True if user wants to play again"""
    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    GAME_OVER_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 50)
    SCORE_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 30)
    clock = pygame.time.Clock()
    global score
    game_end_music = pygame.mixer.Sound("./assets/game_end_music.wav")

    # ----- MAIN LOOP
    while not done:
        # ----- EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                # Check for user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        # ----- LOGIC
        pygame.mixer.Sound.play(game_end_music)


        # ------ RENDER
        # Display game over text
        game_over_surf = GAME_OVER_FONT.render("GAME OVER", True, WHITE)
        screen.blit(game_over_surf, (WIDTH / 2 - 200, HEIGHT / 2))

        # Display the user's score
        score_surf = SCORE_FONT.render(f"YOUR SCORE:{score}", True, WHITE)
        screen.blit(score_surf, (WIDTH/2 - 200, HEIGHT / 2 - 100))

        # Display user instructions
        instructions_surf = SCORE_FONT.render("Press SPACE to play again", True, WHITE)
        screen.blit(instructions_surf, (50, HEIGHT / 2 + 100))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)



def main():
    pygame.init()
    game_loop()
    pygame.mixer.stop()
    time.sleep(0.5)

    while end_game_loop():     # While end_game_loop returns True run game_loop
        # Reset the score
        global score
        score = 0

        pygame.mixer.stop()

        game_loop()

        pygame.mixer.stop()
        time.sleep(0.5)

    pygame.quit()

if __name__ == "__main__":
    main()