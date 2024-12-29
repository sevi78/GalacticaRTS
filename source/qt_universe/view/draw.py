import math

import pygame
from pygame import Rect, gfxdraw, draw

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image
from source.pan_zoom_quadtree.view.draw import draw_rect_border, YELLOW, RED
from source.handlers.color_handler import colors


def draw_points_inside_screen_rect_with_lod(screen, qtree, screen_search_area):
    draw_rect_border(screen, screen_search_area, YELLOW)

    world_x1, world_y1 = pan_zoom_handler.screen_2_world(screen_search_area.left, screen_search_area.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(screen_search_area.right, screen_search_area.bottom)
    world_search_area = Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)

    found = qtree.query(world_search_area)
    for point in found:
        if point.lod == 0:
            gfxdraw.pixel(screen, int(point.rect.centerx), int(point.rect.centery), point.color)
        elif point.lod == 1:
            draw.circle(screen, point.color, point.rect.center, int(point.rect.width / 2))
            gfxdraw.pixel(screen, int(point.rect.centerx), int(point.rect.centery), RED)
        else:
            image = get_image(point.image_name)
            scaled_image = pygame.transform.scale(image, point.rect.size)
            screen.blit(scaled_image, point.rect)
            gfxdraw.pixel(screen, int(point.rect.centerx), int(point.rect.centery), RED)

        # draw.rect(screen, point.color, point.rect, 1)

        if point.selected:
            draw_rect_border(screen, point.rect, RED)

        draw_orbit_circle(point)


def draw_orbit_circle(self):
    """
    draws the orbit
    """
    if not self.orbit_object:
        return


    color = colors.get_orbit_color(self.type)
    if self.orbit_object and config.show_orbit:
        pos = self.orbit_object.rect.center
        radius =math.dist(self.rect.center, pos)
        pygame.draw.circle(config.win, color, (pos[0], pos[1]), radius, 1)

