# Vick Wang

# Imports
import os
import random
import pygame

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen size
WIDTH = 900
HEIGHT = 600
SCREENSIZE = (WIDTH, HEIGHT)

# Other constants
FPS = 60
SNAKE_SIZE = 30
SNAKE_SPEED = 5


# Sprite for the snake
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        # Init sprite
        pygame.sprite.Sprite.__init__(self)
        self.length = 1
        self.chunks = []
        self.x = 45
        self.y = 55
        self.x_speed = 0
        self.y_speed = 0
        self.food_x = random.randint(20, WIDTH // 2)
        self.food_y = random.randint(20, HEIGHT // 2)

    def move(self):
        # move snake position
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

        if abs(self.x - self.food_x) < 30 and abs(self.y - self.food_y) < 30:
            # Snake touched food so add score and make new food
            global score
            global highscore
            score += 10
            self.food_x = random.randint(20, WIDTH // 2)
            self.food_y = random.randint(20, HEIGHT // 2)
            self.length += 5
            if score > highscore:
                highscore = score

    def draw(self, screen):
        # make a snake blob
        chunk = (self.x, self.y)

        # add to snake blobs
        self.chunks.append((self.x, self.y))

        # remove old chunk
        if len(self.chunks) > self.length:
            del self.chunks[0]

        global game_stopped

        # snake run into itself
        if chunk in self.chunks[:-1]:
            game_stopped = True

        # snake touched screen border
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            game_stopped = True

        # draw snake blobs
        for x, y in self.chunks:
            pygame.draw.rect(screen, BLACK, [x, y, SNAKE_SIZE, SNAKE_SIZE])


# Runs game
def main():
    # Init pygame
    pygame.init()

    # Create display
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Snake Game")
    pygame.display.update()
    screen.fill((222, 49, 99))

    # Comic sans font
    font = pygame.font.SysFont("Comic Sans", 25)
    # Clock for controlling fps
    clock = pygame.time.Clock()

    # Draws text to the screen
    def show_text(text, color, x, y):
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    # Create sprite
    snake = Snake()

    global game_stopped
    global score
    global highscore

    score = 0
    game_started = False
    game_stopped = False

    # Create highscore.txt text file to store high score
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
            highscore = 0
    else:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())

    # Game loop
    while not game_stopped:
        # Introduce player
        if not game_started:
            show_text("Welcome to snakes", BLACK, WIDTH // 2, 250)
            show_text("Press space bar to play", BLACK, WIDTH // 2, 290)
            show_text("Dont hit yourself", BLACK, WIDTH // 2, 330)

            # Wait for player to press space to start game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_stopped = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_started = True
        else:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_stopped = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        snake.x_speed = SNAKE_SPEED
                        snake.y_speed = 0

                    elif event.key == pygame.K_LEFT:
                        snake.x_speed = -SNAKE_SPEED
                        snake.y_speed = 0

                    elif event.key == pygame.K_UP:
                        snake.y_speed = -SNAKE_SPEED
                        snake.x_speed = 0

                    elif event.key == pygame.K_DOWN:
                        snake.y_speed = SNAKE_SPEED
                        snake.x_speed = 0

            # Move the snake
            snake.move()

            # snake.move() increases score. check and update highscore
            if score > int(highscore):
                highscore = score

            # Make screen blank
            screen.fill(WHITE)

            # Draw food blob on screen
            pygame.draw.rect(
                screen,
                RED,
                (snake.food_x, snake.food_y, SNAKE_SIZE, SNAKE_SIZE),
            )

            # Draw the snake
            snake.draw(screen)

            # Print score
            show_text(
                f"Score: {score} Highscore: {highscore}",
                (128, 128, 128),
                5,
                5,
            )

        # Update display
        pygame.display.flip()
        # Manage fps
        clock.tick(FPS)

    # Save high score
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))

    # Exit python
    exit()


if __name__ == "__main__":
    main()
