import pygame

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler


def draw_zoomable_circle(surface, color, world_x, world_y, radius):
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    pygame.draw.circle(surface, color,(screen_x, screen_y), radius * pan_zoom_handler.zoom, 1)