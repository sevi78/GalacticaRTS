import math
from functools import lru_cache

import pygame
from pygame import Rect


def draw_arrows_on_line_from_start_to_end_(surf, color, start_pos, end_pos, width=1, dash_length=10, arrow_size=(4, 6)):
    clip_rect_ = surf.get_clip()
    border = 50
    clip_rect = Rect(
            clip_rect_[0] + border, clip_rect_[1] + border, clip_rect_[2] - border * 2, clip_rect_[3] - border * 2)

    x1, y1 = end_pos
    x2, y2 = start_pos
    dl = dash_length

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    dashes = int(distance / dl)
    if dashes == 0:
        return

    dx_dash = dx / dashes
    dy_dash = dy / dashes

    arrow_width, arrow_height = arrow_size

    for i in range(dashes):
        end = x1 + dx_dash * i, y1 + dy_dash * i
        start = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)
        pygame.draw.line(surf, color, start, end, width)

        # Calculate the angle of the dash
        angle = math.atan2(dy_dash, dx_dash)

        # Calculate the points of the arrowhead
        right = end[0] + arrow_height * math.cos(angle - math.pi / 6), end[
            1] + arrow_height * math.sin(angle - math.pi / 6)
        left = end[0] + arrow_height * math.cos(angle + math.pi / 6), end[
            1] + arrow_height * math.sin(angle + math.pi / 6)
        tip = end[0] + arrow_width * math.cos(angle), end[1] + arrow_width * math.sin(angle)

        # Draw the arrowhead
        pygame.draw.polygon(surf, color, [right, tip, left])
        # pygame.draw.lines(surf, color, True, [right, tip, left])


@lru_cache(maxsize=1000)
def calculate_arrow_points_on_line_from_start_to_end(start_pos, end_pos, dash_length=10, arrow_size=(4, 6)):
    x1, y1 = end_pos
    x2, y2 = start_pos
    dl = dash_length

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return []
    dashes = int(distance / dl)
    if dashes == 0:
        return []

    dx_dash = dx / dashes
    dy_dash = dy / dashes

    arrow_width, arrow_height = arrow_size

    points = []
    for i in range(dashes):
        end = x1 + dx_dash * i, y1 + dy_dash * i
        start = x1 + dx_dash * (i + 0.5), y1 + dy_dash * (i + 0.5)

        angle = math.atan2(dy_dash, dx_dash)
        right = end[0] + arrow_height * math.cos(angle - math.pi / 6), end[
            1] + arrow_height * math.sin(angle - math.pi / 6)
        left = end[0] + arrow_height * math.cos(angle + math.pi / 6), end[
            1] + arrow_height * math.sin(angle + math.pi / 6)
        tip = end[0] + arrow_width * math.cos(angle), end[1] + arrow_width * math.sin(angle)

        points.append((start, end, (right, tip, left)))

    return points


def draw_arrows_on_line_from_start_to_end(surf, color, start_pos, end_pos, width=1, dash_length=10, arrow_size=(4, 6)):
    clip_rect_ = surf.get_clip()
    border = 50
    clip_rect = Rect(
            clip_rect_[0] + border, clip_rect_[1] + border,
            clip_rect_[2] - border * 2, clip_rect_[3] - border * 2
            )

    points = calculate_arrow_points_on_line_from_start_to_end(start_pos, end_pos, dash_length, arrow_size)

    for start, end, arrow in points:
        if (clip_rect.left <= start[0] <= clip_rect.right and
                clip_rect.top <= start[1] <= clip_rect.bottom and
                clip_rect.left <= end[0] <= clip_rect.right and
                clip_rect.top <= end[1] <= clip_rect.bottom):

            pygame.draw.line(surf, color, start, end, width)

            right, tip, left = arrow
            if (clip_rect.left <= tip[0] <= clip_rect.right and
                    clip_rect.top <= tip[1] <= clip_rect.bottom):
                pygame.draw.polygon(surf, color, [right, tip, left])



# def draw_arrow_pointing_to_target_pos(screen, start_pos, target_pos, color, arrow_size):
#     """
#     This function draws an arrow that moves towards a target position.
#
#     Parameters:
#     screen (pygame.Surface): The surface to draw the arrow on.
#     start_pos (tuple): The starting position of the arrow.
#     target_pos (tuple): The target position of the arrow.
#     color (tuple): The color of the arrow.
#     arrow_size (int): The size of the arrow.
#     """
#
#     # Calculate the angle to the target position
#     dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
#     angle = math.atan2(dy, dx)
#
#     # Calculate the end position of the arrow
#     end_pos = (start_pos[0] + arrow_size * math.cos(angle), start_pos[1] + arrow_size * math.sin(angle))
#
#     # Draw the arrow
#     pygame.draw.line(screen, color, start_pos, end_pos, 2)
#     pygame.draw.polygon(screen, color, [end_pos, (
#         end_pos[0] - 10 * math.cos(angle - math.pi / 6), end_pos[1] - 10 * math.sin(angle - math.pi / 6)), (
#                                             end_pos[0] - 10 * math.cos(angle + math.pi / 6),
#                                             end_pos[1] - 10 * math.sin(angle + math.pi / 6))])


def draw_arrow_orientated(win, pos, orientation, color, size, width=1):
    # Calculate arrowhead points based on orientation
    x, y = pos
    if orientation in ['right', 'left']:
        upy = y + size
        downy = y - size
        if orientation == 'right':
            upx = x - size
            downx = x - size
        else:  # left
            upx = x + size
            downx = x + size
    else:  # up or down
        upx = x + size
        downx = x - size
        if orientation == 'down':
            upy = y - size
            downy = y - size
        else:  # up
            upy = y + size
            downy = y + size

    pygame.draw.line(win, color, (x, y), (upx, upy), width)
    pygame.draw.line(win, color, (x, y), (downx, downy), width)


def draw_arrowed_cross(win, pos, color, size, width=1, center_distance=20.0):
    # top
    top_pos = (pos[0], pos[1] - center_distance)

    # bottom
    bottom_pos = (pos[0], pos[1] + center_distance)

    # left
    left_pos = (pos[0] - center_distance, pos[1])

    # right
    right_pos = (pos[0] + center_distance, pos[1])

    draw_arrow_orientated(win, top_pos, 'down', color, size, width)
    draw_arrow_orientated(win, bottom_pos, 'up', color, size, width)

    draw_arrow_orientated(win, left_pos, 'right', color, size, width)
    draw_arrow_orientated(win, right_pos, 'left', color, size, width)


class ArrowCrossAnimated:
    def __init__(
            self, win, color, pos=(100, 100), size=60, center_distance=30, arrow_size=15, width=1, steps=0.5,
            direction=-1
            ):
        # args
        self.win = win
        self.color = color
        self.pos = pos
        self.size = size
        self.size_raw = size
        self.center_distance_raw = center_distance
        self.center_distance = center_distance
        self.arrow_size = arrow_size
        self.width = width

        # calculated
        self.max_moving_index = None
        self.min_moving_index = None
        self.moving_distance = self.size - self.center_distance
        self.steps = steps
        self.direction = direction
        self.moving_index = self.center_distance / self.steps * self.direction
        self.draw_range = self.size - self.center_distance_raw

    def update(self, pos):
        # set pos
        self.pos = pos

        # calc positions
        self.size = self.size_raw
        self.min_moving_index = self.center_distance_raw / self.steps * self.direction
        self.max_moving_index = self.size / self.steps
        self.center_distance = self.moving_index * self.steps * self.direction

        # add index
        self.moving_index -= self.steps * self.direction

        # if too near
        if self.center_distance < self.center_distance_raw:
            self.moving_index = -self.max_moving_index

        # if too far
        if self.center_distance > self.size:
            self.moving_index = self.min_moving_index

    def draw(self):
        draw_arrowed_cross(self.win, self.pos, self.color, self.arrow_size, self.width, self.center_distance)


class ArrowCrossAnimatedArray(ArrowCrossAnimated):
    def __init__(
            self, win, color, pos=(100, 100), size=60, center_distance=30, arrow_size=15, width=1, array=3,
            array_distance=10, steps=0.5, direction=-1
            ):
        ArrowCrossAnimated.__init__(self, win, color, pos, size, center_distance, arrow_size, width, steps, direction)
        self.array = array
        self.array_distance = array_distance

    def set_center_distance(self, value):
        self.center_distance_raw = value
        self.size_raw = self.center_distance_raw + self.draw_range

    def draw(self):
        for i in range(self.array):
            draw_arrowed_cross(self.win, self.pos, self.color, self.arrow_size, self.width, self.center_distance + (
                    i * self.array_distance))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Arrow Animation')

    color = (55, 130, 157)

    array = ArrowCrossAnimatedArray(
            screen,
            color,
            (400, 300),
            60,
            10,
            8,
            1,
            3,
            5,
            0.5,
            -1)

    # arrowed_cross = ArrowCrossAnimated(
    #     screen,
    #     color,
    #     (400, 300),
    #     100,
    #     20,
    #     10,
    #     10,
    #     )

    index_scale = 30
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Draw the arrow
        # draw_arrow_pointing_to_target_pos(screen, (400, 400), (800, 800), (0, 123, 0), 10)
        # draw_arrow_orientated(screen, (400, 400), 'right', (0, 123, 0), 10, 5)
        # draw_arrowed_cross(screen, (400, 400), (0, 123, 0), 10, 1, 30)
        # arrowed_cross.pos = pygame.mouse.get_pos()
        # arrowed_cross.update(pygame.mouse.get_pos())
        # arrowed_cross.draw()
        array.set_center_distance(150)
        array.update(pygame.mouse.get_pos())
        array.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
