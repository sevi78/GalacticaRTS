import pygame
from pygame import draw

from source.handlers.color_handler import colors
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler

from source.qt_universe.view.qt_view_config.qt_draw_config import GREEN

font = pygame.font.SysFont(None, 12)


def debug_object(screen,point) -> None:
    y = 10

    sorted_dict = {k: point.__dict__[k] for k in ['type'] if k in point.__dict__}
    sorted_dict.update({k: point.__dict__[k] for k in sorted(point.__dict__) if k != 'type'})

    for attr, value in sorted_dict.items():
        text = font.render(f"{attr}: {value}",  1, colors.frame_color)
        x_, y_ = pan_zoom_handler.world_2_screen(point.x, point.y)
        screen.blit(text, (x_ + point.rect.width/2, y_ + point.rect.height/2+ y))
        y += 14

    draw.rect(screen, GREEN, point.rect, 1)

# def draw_debug_text(screen, vars):
#     x,y = 10,10
#     color = (255, 255, 255)
#
#     for var in vars:
#         text_ = f"{var}: {vars[var]}"
#         text = font.render(text_, True, color)
#         screen.blit(text, (x,y))
#         y += 14
#     # text_ = f"Point Quadtree: {fps} fps"
#     # text = font.render(text_, True, color)
#     # screen.blit(text, (x,y))
#     # y += 14
#     #
#     # text_ = f"game_speed: {game_speed}"
#     # text = font.render(text_, True, color)
#     # screen.blit(text, (x, y))
#     # y += 14




def draw_debug_text(screen, kwargs):
      # You can adjust the font and size
    y_offset = 10
    for var_name, value in kwargs.items():
        if callable(value):
            value = value()  # Call the function if it's callable
        text = f"{var_name}: {value}"
        debug_surface = font.render(text, True, (255, 255, 255))  # White text
        screen.blit(debug_surface, (10, y_offset))
        y_offset += 14  # Adjust vertical spacing between lines

