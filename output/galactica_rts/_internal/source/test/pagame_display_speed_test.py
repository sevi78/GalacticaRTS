import random

import pygame

from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class Object:
    def __init__(self, win, x, y, width, height, image):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.win.blit(self.image, self.rect)
        pygame.display.update(self.rect)
        # pygame.display.update()


class MainLoop:
    def __init__(self, win):
        self.font_size = 18
        self.font = pygame.font.SysFont(None, self.font_size)
        self.objects = []
        pygame.init()
        self.win = win
        self.running = True
        self.modes = ["flip", "update"]  # {"flip"}
        self.mode = "update"

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.mode = "flip"
                    if event.key == pygame.K_u:
                        self.mode = "update"
            self.draw()

    def add(self, obj):
        self.objects.append(obj)

    def draw_objects(self):
        for i in self.objects:
            i.draw()

    def draw(self):
        self.win.fill((0, 0, 0))
        self.draw_objects()
        self.draw_text()
        # if self.mode == "flip":
        #     pygame.display.flip()
        #
        # elif self.mode == "update":
        #     pygame.display.update()

    def draw_text(self):
        self.win.blit(self.font.render("FPS: ", True, colors.frame_color), (100, 100))
        pygame.display.update(pygame.Rect(100, 100, self.font_size, self.font_size))


def main():
    win = pygame.display.set_mode((1200, 800), pygame.DOUBLEBUF, pygame.RESIZABLE)
    mainloop = MainLoop(win)
    for i in range(10000):
        mainloop.add(Object(win, random.randint(0, 1000), random.randint(0, 1000), 20, 20, get_image("star2_100x100.png")))
    mainloop.run()


if __name__ == "__main__":
    main()
