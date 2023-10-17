import math
import os

import pygame
from PIL import Image
from pygame import Vector2

from source.multimedia_library.images import gifs_path
from source.multimedia_library.sounds import sounds
from source.utils.positioning import rot_center

gif_path = os.path.join("assets", "gifs")


class GifHandler(pygame.sprite.Sprite):
    def __init__(self, parent, gif, **kwargs):
        super().__init__()
        self.target_position_x = 0
        self.target_position_y = 0
        self.target_position = Vector2(0, 0)
        self.parent = parent
        self.rotate = kwargs.get("rotate", False)
        self.gif = gif
        self.loop = kwargs.get("loop", False)
        self.sound = kwargs.get("sound", None)
        self.relative_gif_size = kwargs.get("relative_gif_size", None)

        self.frames = self.load_gif_frames(self.gif)
        self.index = 0
        self.counter = 0
        self.image_raw = self.frames[self.index]
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

        if self.relative_gif_size:
            self.max_size = max(self.parent.rect.width, self.parent.rect.height) * self.relative_gif_size

    def set_gif(self, gif, **kwargs):
        self.gif = gif
        self.loop = kwargs.get("loop", False)
        self.sound = kwargs.get("sound", None)
        self.relative_gif_size = kwargs.get("relative_gif_size", None)

        self.frames = self.load_gif_frames(self.gif)
        self.index = 1
        self.counter = 1
        self.image_raw = self.frames[self.index]
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

        if self.relative_gif_size:
            self.max_size = max(self.parent.rect.width, self.parent.rect.height) * self.relative_gif_size

    def load_gif_frames(self, gif_name):
        """ Load explosion GIF and extract frames"""
        frames = []
        path = os.path.join(gifs_path, gif_name)
        gif = Image.open(path)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            frames.append(frame_surface)
        return frames

    def update(self):
        self.counter += 1
        if self.counter % 5 == 0:
            self.index += 1
            if self.index == 1:
                if self.sound:
                    sounds.play_sound(getattr(sounds, self.sound))

            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0

            else:
                self.image_raw = self.frames[self.index]
                self.image = self.frames[self.index]

        self.set_size()
        self.set_gif_position()

        if self.rotate:
            self.set_target_position(self.parent.target_position)
            self.rotate_image_to_target()

    def set_size(self):
        # Calculate the maximum size based on the relative GIF size
        if self.relative_gif_size:
            self.max_size = max(self.parent.rect.width, self.parent.rect.height) * self.relative_gif_size

            # Set the image rect according to its parent, including the size
            self.rect.width = self.max_size
            self.rect.height = self.max_size
            self.image = pygame.transform.scale(self.image_raw, (self.max_size, self.max_size))

        else:
            self.image = pygame.transform.scale(self.image_raw, (self.parent.rect.width, self.parent.rect.height))
            self.rect = self.image.get_rect()

    def rotate_image_to_target(self):
        if not self.parent.target:
            return

        rel_x, rel_y = self.parent.target.rect.center[0] - self.rect.x, self.parent.target.rect.center[1] - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        new_image, new_rect = rot_center(self.image, angle, self.rect.x, self.rect.y)

        self.image = new_image
        self.rect = new_rect

    def set_gif_position(self):
        if self.relative_gif_size:
            self.rect.x = self.parent.rect.x - (self.max_size - self.parent.rect.width) / 2
            self.rect.y = self.parent.rect.y - (self.max_size - self.parent.rect.height) / 2
        else:
            self.rect.x = self.parent.rect.x
            self.rect.y = self.parent.rect.y

    def draw(self):
        try:
            self.update()

            # only because frame 0 doesn't alpha properly, we set get index 1
            if not self.loop:
                if self.index > 0:
                    self.parent.win.blit(self.image, self.rect)
            else:
                self.parent.win.blit(self.image, self.rect)
        except AttributeError as e:
            print("gif_handler error", e)

    def set_target_position(self, position):
        self.target_position = position
