import os
import pygame

from source.multimedia_library.images import get_gif_frames

pygame.init()

SIZE = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):
        """
        Animated sprite object.

        Args:
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        size = (32, 32)  # This should match the size of the images.

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.index = 1
        self.image = images[self.index]  # 'image' is the current image of the animation.

        self.animation_time = 0.5
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

        self.update_mode = 0
        self.kill_after_gif_loop = False

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images) if not (self.index + 1) % len(self.images) == 0 else 1
            if self.kill_after_gif_loop:
                if self.index == len(self.images)-1:
                    self.kill()
                    return

            self.image = self.images[self.index]
            print (f"update_time_dependent: self.index: {self.index}, len(self.images): {len(self.images)}")

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images) if not (self.index + 1) % len(self.images) == 0 else 1
            if self.kill_after_gif_loop:
                if self.index == len(self.images)-1:
                    self.kill()
                    return
            self.image = self.images[self.index]
            print(f"update_frame_dependent: self.index: {self.index}, len(self.images): {len(self.images)}")

    def update_manually(self):
        self.image = self.images[self.index]

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        if self.update_mode == 0:
            self.update_frame_dependent()
        elif self.update_mode == 1:
            self.update_time_dependent(dt)
        else:
            self.update_manually()


def main():
    images = get_gif_frames("explosion2.gif")  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(100, 100), images=images)
    all_sprites = pygame.sprite.Group(player)  # Creates a sprite group and adds 'player' to it.

    running = True
    while running:

        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.index -= 1
                elif event.key == pygame.K_LEFT:
                    player.index += 1

                elif event.key == pygame.K_UP:
                    player.update_mode += 1
                elif event.key == pygame.K_DOWN:
                    player.update_mode -= 1

                elif event.key == pygame.K_SPACE:
                    player.kill_after_gif_loop = True

                print (f"player.index: {player.index}")


        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
