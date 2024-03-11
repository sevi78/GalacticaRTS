import math
import time

import pygame

from source.draw.moving_arrow import MovingArrow


class MovingArrow__:
    def __init__(self,
                 win,
                 color,
                 start_pos,
                 direction='right',
                 width=1,
                 arrow_size=5,
                 cycle_time=0.1,
                 steps=1,
                 reset_distance=100.0):

        self.downy = 0
        self.upy = 0
        self.upx = 0
        self.downx = 0
        self.win = win
        self.color = color

        self.start_pos_raw = start_pos
        self.start_pos = start_pos
        self.relative_x = 0
        self.relative_y = 0
        self.direction = direction
        self.width = width
        self.arrow_size = arrow_size
        self.start_time = time.time()
        self.cycle_time = cycle_time
        self.steps = steps
        self.reset_distance = reset_distance

    def set_position(self, pos):
        self.start_pos_raw = pos

    def move_arrow(self):
        self.relative_x, self.relative_y = self.start_pos
        # self.start_time = time.time()
        if self.direction == 'right':
            self.relative_x += self.steps
        elif self.direction == 'left':
            self.relative_x -= self.steps
        elif self.direction == 'down':
            self.relative_y += self.steps
        elif self.direction == 'up':
            self.relative_y -= self.steps
        # Calculate arrowhead points based on direction
        if self.direction in ['right', 'left']:
            self.upy = self.relative_y + self.arrow_size
            self.downy = self.relative_y - self.arrow_size
            if self.direction == 'right':
                self.upx = self.relative_x - self.arrow_size
                self.downx = self.relative_x - self.arrow_size
            else:  # left
                self.upx = self.relative_x + self.arrow_size
                self.downx = self.relative_x + self.arrow_size
        else:  # up or down
            self.upx = self.relative_x + self.arrow_size
            self.downx = self.relative_x - self.arrow_size
            if self.direction == 'down':
                self.upy = self.relative_y - self.arrow_size
                self.downy = self.relative_y - self.arrow_size
            else:  # up
                self.upy = self.relative_y + self.arrow_size
                self.downy = self.relative_y + self.arrow_size

        #self.start_pos = (self.relative_x, self.relative_y)
        return self.relative_x, self.relative_y

    def draw(self):
        # x, y = self.start_pos
        # if time.time() - self.start_time > self.cycle_time:
        x, y = self.move_arrow()

        # reset position
        if math.dist(self.start_pos_raw, self.start_pos) > self.reset_distance:
            self.start_pos = self.start_pos_raw

        # Draw the line and arrowhead
        pygame.draw.line(self.win, self.color, (x, y), (self.downx, self.downy), self.width)
        pygame.draw.line(self.win, self.color, (x, y), (self.upx, self.upy), self.width)


class AnimatedArrowedCross:
    def __init__(self, win, pos=(0, 0), size=100, center_distance=230):
        self.win = win
        self.position = pos
        self.size = size
        self.center_distance = center_distance
        self.arrows = []

        self.directions = {0: "left", 1: "up", 2: "right", 3: "down"}
        self.start_positions = None
        self.set_start_positions()

        for i in range(4):
            self.arrows.append(MovingArrow(
                self.win,
                (120, 120, 200),
                self.start_positions[self.directions[i]],
                self.directions[i],
                1,
                5,
                0.001,
                0.3,
                self.center_distance))

    def draw(self):
        for i in self.arrows:
            i.draw()

    def set_position(self, pos):
        self.position = pos
        for i in self.arrows:
            i.set_position(pos)

    def set_start_positions(self):
        self.start_positions = {"left": (self.position[0] - self.center_distance, self.position[1]),
                                "up": (self.position[0], self.position[1] - self.center_distance),
                                "right": (self.position[0] + self.center_distance, self.position[1]),
                                "down": (self.position[0], self.position[1] + self.center_distance)
                                }


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Moving Arrow")
    clock = pygame.time.Clock()
    animated_arrowed_cross = AnimatedArrowedCross(screen, (0, 0), 50, center_distance=30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEMOTION:
                # animated_arrowed_cross.start_pos = pygame.mouse.get_pos()
                # animated_arrowed_cross.start_pos_raw = pygame.mouse.get_pos()


                animated_arrowed_cross.set_position(pygame.mouse.get_pos())

        screen.fill((0, 0, 0))


        animated_arrowed_cross.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
