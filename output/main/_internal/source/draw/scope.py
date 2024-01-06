import pygame
from source.configuration import global_params
from source.handlers.color_handler import colors


def draw_scope(self):
    """
    draws line to mouse position and draws the scope
    """

    if global_params.hover_object != None:
        color = colors.hover_color
        # print("draw_scope", global_params.hover_object,global_params.hover_object.name )
    else:
        color = self.frame_color

    # draw line from selected object to mouse cursor
    if self.selected:
        pygame.draw.line(surface=self.win, start_pos=self.rect.center, end_pos=pygame.mouse.get_pos(), color=color)

        # scope
        pos = pygame.mouse.get_pos()
        size_x = 30
        size_y = 30
        arrow = pygame.draw.arc(self.win, color, (
            (pos[0] - size_x / 2, pos[1] - size_y / 2), (size_x, size_y)), 2, 10, 2)

        arrow = pygame.draw.arc(self.win, color, (
            (pos[0] - size_x, pos[1] - size_y), (size_x * 2, size_y * 2)), 2, 10, 2)

        # horizontal line
        factor = size_x / 12
        x = pos[0] - size_x * factor / 2
        y = pos[1]
        x1 = x + size_x * factor
        y1 = y
        pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=color)

        # vertical line
        x = pos[0]
        y = pos[1] - size_x * factor / 2
        x1 = x
        y1 = y + size_x * factor
        pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=color)
