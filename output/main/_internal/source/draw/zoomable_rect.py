import pygame.draw
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler


def draw_zoomable_rect(surface, color, world_x, world_y, width, height, **kwargs):
    border_radius = kwargs.get("border_radius", 0)
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    rect = pygame.Rect(screen_x, screen_y, width * pan_zoom_handler.zoom, height * pan_zoom_handler.zoom)
    pygame.draw.rect(surface, color, rect, 1, border_radius)
