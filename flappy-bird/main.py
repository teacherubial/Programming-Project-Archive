from __future__ import annotations

import json
import os
import random
import sys
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''  # disable that message at startup

import pygame as pg

TYPE_CHECKING = False  # avoid importing typing (small performance boost)

if TYPE_CHECKING:
    from pygame.rect import Rect
    from pygame.surface import Surface

# Colours
WHITE = (255, 255, 255)
# Screen size
SIZE = WIDTH, HEIGHT = (762, 896)
# Screen caption
CAPTION = 'Flappy bird'
# Frames per second
FPS = 60
# Frames between new pipes
PIPES_SPAWN = 180
# Pipe y offset range
PIPES_Y_RANGE = [*range(-160, 160)]
# Note that setting this any higher will probably
# break visuals and maybe the game


class Flappy(pg.sprite.Sprite):
    """Prepresents the birb"""

    # Type checker complains that these are None (cause of superclass)
    # So, we declare the type explicitly
    image: Surface
    rect: Rect

    def __init__(self) -> None:
        super().__init__()

        image = pg.image.load('images/flappy.png').convert_alpha()
        # Images is 3 images in one (I stole it from somewhere)
        # <flapping_down_image><gliding_image><flapping_up_image>
        # Here we split it and isolate each part of the image
        # Dimensions per image are 92x64
        self.flap_down_image = image.subsurface((0, 0, 92, 64))
        self.glide_image = image.subsurface((92, 0, 92, 64))
        self.flap_up_image = image.subsurface((184, 0, 92, 64))
        # self.image is the image that .draw() will be using
        # We will be mutating this value to imitate animated flapping
        self.image = self.glide_image
        # All images are the same size, this is safe
        self.rect = self.image.get_rect()
        # Center the bird
        self.rect.center = (WIDTH // 2, 200)
        # A mask lets us calculate hitbox collisions more accurately
        self.mask = pg.mask.from_surface(self.image)

        # self.velocity is the speed at which the bird falls or rises
        # If negative, the bird falls (as y decreases)
        # If positive, the bird rises (as y increases)
        self.velocity = -2

        # self.fall_acceleration is the rate at which self.velocity changes
        # This is simply to make the game feel less static and also
        # Piss the player off. Flappy bird is meant to be awkward
        self.fall_acceleration = 1

        # Whether this bird has flown off screen/bumped a pipe
        self.dead = False

        # Frames until self.image is cycled
        self.next_image_in = 10

    def draw(self, screen: Surface) -> None:
        """Draw this bird onto the game screen"""
        # Determine speed based on acceleration by velocity
        speed = self.fall_acceleration * self.velocity

        # Decrease velocity (as the bird is constantly falling)
        self.velocity -= 0.25

        if self.fall_acceleration < 1.05:
            # Increase falling acceleration if it is below 1.01
            self.fall_acceleration += 0.0008

        # Speed has to be opposite because of how this helper works
        self.rect.move_ip(0, -speed)

        if self.rect.bottom >= HEIGHT or self.rect.top <= -self.rect.height:
            # The bird went off screen, set .dead to True
            # Game.tick() knows how to handle this
            self.dead = True

        if self.next_image_in > 0:
            # Decrease image counter by 1
            self.next_image_in -= 1
        else:
            # We are updating the image for upcoming frame
            if self.next_image_in <= 0:
                # Reset counter
                self.next_image_in = 10

                if self.fall_acceleration >= 1.05:
                    # We are accelerating pretty fast here
                    # Flap the wings harder because bird panic
                    self.next_image_in = 3
                # Wing was all the way down, move wing up to middle
                if self.image == self.flap_down_image:
                    self.image = self.glide_image
                # Wing was gliding, move wing all the way up
                elif self.image == self.glide_image:
                    self.image = self.flap_up_image
                # Wing was all the way up, move wing back down
                elif self.image == self.flap_up_image:
                    self.image = self.flap_down_image

        screen.blit(self.image, self.rect)

    def flap(self) -> None:
        """Flap those puny wings once"""

        # .draw() is called soon, set .image to flapping down image
        self.image = self.flap_down_image
        # Makes the flapping down image last for 26 frames instead of
        # the default 8. I know, fancy graphics.
        self.next_image_in = 26
        # Set velocity to a positive value so the bird moves up
        self.velocity = 6.5
        # Reset acceleration
        self.fall_acceleration = 1


class Pipe(pg.sprite.Sprite):
    """Represents an upright or flipped pipe"""

    image: pg.surface.Surface
    rect: pg.rect.Rect

    def __init__(self, image: Surface, offset: int, flipped: bool = False) -> None:
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx = WIDTH + self.rect.width
        # Also create a mask here for perforamance reasons
        # as pg.sprite.collide_mask() creates one otherwise
        self.mask = pg.mask.from_surface(image)

        if flipped:  # This is an upside down pipe
            self.rect.top = -162 + offset
        else:  # This is an upright pipe
            self.rect.bottom = HEIGHT + 162 + offset

    def move(self) -> None:
        self.rect.move_ip(-2, 0)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)


class PipePair:
    """Represents a pair of pipes"""

    def __init__(self, game: Game) -> None:
        try:
            # Check if we have images cached
            image, flipped = PipePair.images
        except AttributeError:
            # Images haven't been loaded yet, load and parse them
            image = pg.image.load('images/pipe.png').convert_alpha()
            # Resize the image so it doesn't look stupid
            image = pg.transform.scale(
                image, (image.get_width() // 1.5, image.get_height() // 1.5)
            )
            # Get a 180-flipped version of the image
            flipped = pg.transform.flip(image, False, True)

            # Cache images for future PipePair objects
            PipePair.images = image, flipped

        # The y offset for drawing the pipes
        offset = random.choice(PIPES_Y_RANGE)

        # Represents the two pipes
        self.upright = Pipe(image, offset)  # This one is upright
        self.flipped = Pipe(flipped, offset, flipped=True)  # This one is upside down

        # Indicates whether flappy has passed this pipe
        self.passed = False
        # Indicates whether this pipe is sitting around unused
        self.unused = False
        self.game = game

    def draw(self, screen: pg.surface.Surface) -> None:
        """Draw this pipe pair onto the game screen"""

        # Unused pipe, return
        if self.unused:
            return

        # Move both pipes
        self.upright.move()
        self.flipped.move()

        # Check if flappy has passed this pipe
        if not self.passed:
            if self.upright.rect.right <= self.game.flappy.rect.left:
                # Flappy has passed this pipe, increment score and set
                # .passed to True to prevent this bit from running again
                self.passed = True
                self.game.incr_score()

        else:
            # Check whether we are off screen
            if self.upright.rect.right <= 0:
                # Set this to True
                self.unused = True

                # self.unused is my way of preventing a weird bug I noticed
                # where the rendered pipes would "flicker" when another pipe
                # was garbage collected and therefore deleted.
                # I'm still not sure what exactly was causing that behavior.
                # If self.unused is True, Game.create_pipe() uses this object
                # instead of creating new pipes by just re-initializing it.

                return

        # Draw both pipes
        self.upright.draw(screen)
        self.flipped.draw(screen)

    def collides(self, flappy: Flappy) -> bool:
        """Return whether flappy managed to bump into this pipe"""
        coll = pg.sprite.collide_mask
        # Calculate whether any hitbox collisions have occured
        return (coll(flappy, self.upright) or coll(flappy, self.flipped)) is not None


class Background:
    def __init__(self) -> None:
        self.image = (
            pg.image.load('images/background.png')
            .convert()
            .subsurface(0, 0, WIDTH, HEIGHT)
        )
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect2 = self.image.get_rect()
        self.rect2.x = WIDTH
        self.rect2.y = 0

    def draw(self, screen: Surface) -> None:
        self.rect.x -= 1
        self.rect2.x -= 1
        if self.rect.x <= -WIDTH:
            self.rect.x = WIDTH
        elif self.rect2.x <= -WIDTH:
            self.rect2.x = WIDTH
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect2)


class RestartButton(pg.sprite.Sprite):
    image: Surface
    rect: Rect

    def __init__(self) -> None:
        self.image = pg.image.load('images/restart-btn.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)
        pg.display.flip()

    def clicked(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


class Game:
    """Represents the flappy bird game"""

    restart_btn: RestartButton | None

    def __init__(self) -> None:
        # Initialize pygame
        pg.display.init()
        pg.font.init()

        # Create screen
        self.screen = pg.display.set_mode(SIZE)

        # Game state
        try:
            f = open('data.json', 'r')
        except FileNotFoundError:
            self.high_score = 0
        else:
            data = json.load(f)
            self.high_score = data.get('high_score', 0)

        self.score = 0
        self.pipes = []
        self.next_pipe_spawn = PIPES_SPAWN
        self.restart_btn = None
        self.start = time.time()

        # Create sprites
        self.background = Background()
        self.flappy = Flappy()
        self.create_pipe()

        # Customize display
        icon = pg.transform.scale(self.flappy.image, (32, 32))
        pg.display.set_icon(icon)
        pg.display.set_caption(CAPTION)

        # Various utilities
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Comic Sans MS', 30)

    def create_pipe(self) -> None:
        """Create a ``PipePair`` and append to ``self.pipes``"""
        for pipe in self.pipes:
            # See PipePair.draw() for an explanation
            if pipe.unused:
                pipe.__init__(self)

                return pipe

        self.pipes.append(PipePair(self))

    def close(self) -> None:
        sys.exit()

    def tick(self) -> None:
        """Render a single frame and run the game for a single tick"""
        if self.flappy.dead and not self.restart_btn:
            self.show_endscreen()

        # Event handling
        for event in pg.event.get():
            # QUIT events will close the game
            if event.type == pg.QUIT:
                return self.close()

            if event.type == pg.KEYDOWN:
                # Pressing Q or Esc will close the game
                if event.key in {pg.K_q, pg.K_ESCAPE}:
                    return self.close()

                if self.flappy.dead:
                    if event.key in {pg.K_SPACE, pg.K_RETURN}:
                        return self.restart()

                else:
                    # Pressing SPACE will make flappy flap
                    if event.key == pg.K_SPACE:
                        self.flappy.flap()

            if self.flappy.dead and event.type == pg.MOUSEBUTTONDOWN:
                assert self.restart_btn is not None

                if self.restart_btn.clicked(event.pos):
                    return self.restart()

        if self.flappy.dead:
            return

        # Decrement spawn counter by 1 every frame
        if self.next_pipe_spawn > 0:
            self.next_pipe_spawn -= 1
        else:
            # Spawn a pipe and reset spawn counter
            self.next_pipe_spawn = PIPES_SPAWN
            self.create_pipe()

        # Preparing our new frame
        screen = self.screen

        # Draw the background
        self.background.draw(screen)

        # Draw sprites
        self.flappy.draw(screen)
        for pipe in self.pipes:
            pipe.draw(screen)

            # If pipe collides with fappy, kill the bird
            if not pipe.passed and pipe.collides(self.flappy):
                self.flappy.dead = True

        # Draw fps counter
        screen.blit(
            self.font.render(f'fps: {round(self.clock.get_fps())}', True, WHITE),
            (8, 8),
        )

        # Draw time counter
        screen.blit(
            self.font.render(f'time: {(time.time() - self.start):.2f}s', True, WHITE),
            (8, 30),
        )

        # Draw high score counter
        screen.blit(
            self.font.render(f'high score: {self.high_score}', True, WHITE),
            (8, 52),
        )

        # Draw score counter
        screen.blit(
            self.font.render(f'score: {self.score}', True, WHITE),
            (8, 74),
        )

        # Update the screen with our new frame
        pg.display.flip()

        # Maintain a rough framerate of "FPS"
        self.clock.tick(FPS)

    def show_endscreen(self) -> None:
        self.restart_btn = RestartButton()
        self.restart_btn.draw(self.screen)

    def incr_score(self) -> None:
        if self.high_score == self.score:
            self.high_score += 1
        self.score += 1

    def restart(self) -> None:
        high_score = self.high_score
        screen = self.screen

        self.__init__()

        self.high_score = high_score
        self.screen = screen

    def save(self) -> None:
        data = {'high_score': self.high_score}

        with open('data.json', 'w+') as f:
            json.dump(data, f)


def main():
    """Run flappy bird"""

    # Create the game
    game = Game()

    try:
        # Game loop
        while True:
            # .tick() will call exit on its own
            game.tick()

    # Graceful exit for EOF/Ctrl+C
    except KeyboardInterrupt:
        pass
    finally:
        game.save()


if __name__ == '__main__':
    main()
