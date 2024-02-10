import pygame

from source.configuration import global_params
from source.draw.dashed_line import draw_dashed_line
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.position_handler import get_distance
from source.multimedia_library.images import get_image
from source.text.text_formatter import format_number

SCOPE_SIZE = 30
SCOPE_TEXT_SIZE = 12


class Scope:
    def __init__(self, win: pygame.surface.Surface):
        self.win = win
        self.font_size = SCOPE_TEXT_SIZE
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.text = ""
        self.base_color = colors.frame_color
        self.hover_color = colors.hover_color
        self.warn_color = pygame.color.THECOLORS.get("red")
        self.warn_image = get_image("warning.png")

    def draw_text(self, x, y, color, text: str):
        text = self.font.render(text, 1, color)
        self.win.blit(text, (x, y))

    def draw_warning_image(self, x, y):
        self.win.blit(self.warn_image, (x, y))

    def draw_scope(self, start_pos: tuple, range_: float, info: dict):
        """
        draws line to mouse position and draws the scope
        """
        # if not obj.selected:
        #     return

        # handle different colors depending on distance and hover object
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance = get_distance(start_pos, (mouse_x, mouse_y)) / pan_zoom_handler.zoom

        # if hover over a possible target -> green
        if global_params.hover_object:
            color = self.hover_color
        # if hover anywhere else -> blue
        else:
            color = self.base_color

        # if distance outside range_
        if distance > range_:
            color = self.warn_color
            self.draw_warning_image(mouse_x, mouse_y - SCOPE_SIZE*2 )

        # draw line from selected object to mouse cursor
        # pygame.draw.line(surface=self.win, start_pos=start_pos, end_pos=(mouse_x, mouse_y), color=color)
        draw_dashed_line(self.win, color, start_pos, (mouse_x, mouse_y), width=1, dash_length=10)

        # scope
        size_x = SCOPE_SIZE
        size_y = SCOPE_SIZE

        # draw arrows
        pygame.draw.arc(self.win, color, ((mouse_x - size_x / 2, mouse_y - size_y / 2), (size_x, size_y)), 2, 10, 2)
        pygame.draw.arc(self.win, color, ((mouse_x - size_x, mouse_y - size_y), (size_x * 2, size_y * 2)), 2, 10, 2)

        # horizontal line
        factor = size_x / 12
        x = mouse_x - size_x * factor / 2
        y = mouse_y
        x1 = x + size_x * factor
        y1 = y
        pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(x1, y1), color=color)

        # vertical line
        x = mouse_x
        y = mouse_y - size_x * factor / 2
        x1 = x
        y1 = y + size_x * factor
        pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(x1, y1), color=color)

        # text
        y = 0
        self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - SCOPE_SIZE - self.font_size - 2, color, f"distance: {format_number(distance * 1000, 1)}")
        for key, value in info.items():
            self.draw_text(mouse_x + SCOPE_SIZE, mouse_y - y - SCOPE_SIZE, color, f"{key}: {value}")
            y += SCOPE_SIZE

        # self.draw_text(mouse_x, mouse_y - SCOPE_SIZE - self.font_size, f"energy use: {distance}")


def draw_scope(self):  # original
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


scope = Scope(global_params.win)
