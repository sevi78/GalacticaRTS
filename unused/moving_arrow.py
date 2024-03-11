import math
import time
import pygame


class MovingArrow:
    def __init__(self,
                 win,
                 color,
                 start_pos,
                 direction='right',
                 width=1,
                 arrow_size=5,
                 cycle_time=0.01,
                 speed=1,
                 reset_distance=100.0):

        self.downy = 0
        self.upy = 0
        self.upx = 0
        self.downx = 0
        self.win = win
        self.color = color
        self.start_pos = start_pos
        self.start_pos_raw = start_pos
        self.direction = direction
        self.width = width
        self.arrow_size = arrow_size
        self.start_time = time.time()
        self.cycle_time = cycle_time
        self.steps = 0
        self.speed = speed
        self.reset_distance = reset_distance

    def set_position(self, pos):
        self.start_pos_raw = pos

    def move_arrow(self):
        x, y = self.start_pos_raw
        self.steps += 1

        self.start_time = time.time()
        if self.direction == 'right':
            x += self.speed * self.steps
        elif self.direction == 'left':
            x -= self.speed * self.steps
        elif self.direction == 'down':
            y += self.speed * self.steps
        elif self.direction == 'up':
            y -= self.speed * self.steps

        # Calculate arrowhead points based on direction
        if self.direction in ['right', 'left']:
            self.upy = y + self.arrow_size
            self.downy = y - self.arrow_size
            if self.direction == 'right':
                self.upx = x - self.arrow_size
                self.downx = x - self.arrow_size
            else:  # left
                self.upx = x + self.arrow_size
                self.downx = x + self.arrow_size
        else:  # up or down
            self.upx = x + self.arrow_size
            self.downx = x - self.arrow_size
            if self.direction == 'down':
                self.upy = y - self.arrow_size
                self.downy = y - self.arrow_size
            else:  # up
                self.upy = y + self.arrow_size
                self.downy = y + self.arrow_size
        self.start_pos = (x, y)
        return x, y

    def draw(self):
        x, y = self.start_pos
        if time.time() - self.start_time > self.cycle_time:
            x, y = self.move_arrow()

        # reset position
        if math.dist(self.start_pos_raw, self.start_pos) > self.reset_distance:
            self.start_pos = self.start_pos_raw
            self.steps = 0

        if math.dist(self.start_pos, pygame.mouse.get_pos()) > self.reset_distance:
            self.start_pos = self.start_pos_raw
            self.steps = 0

        # Draw the line and arrowhead
        pygame.draw.line(self.win, self.color, (x, y), (self.downx, self.downy), self.width)
        pygame.draw.line(self.win, self.color, (x, y), (self.upx, self.upy), self.width)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Moving Arrow")
    clock = pygame.time.Clock()
    arrow = MovingArrow(
        screen,
        (120, 120, 200),
        (100, 100),
        'down',
        1,
        15,
        0.001,
        1,
        100.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEMOTION:
                arrow.start_pos_raw = event.pos

        screen.fill((0, 0, 0))

        arrow.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
