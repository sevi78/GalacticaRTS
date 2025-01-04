import math
import time

import pygame
from pygame import Rect, gfxdraw, draw, Surface

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, scale_image_cached, rotate_image_cached, get_gif_frames
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.view.game_objects.qt_stars import QTImage, QTFlickeringStar, QTPulsatingStar, QTGif, \
    QTMovingImage

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = pygame.color.THECOLORS["yellow"]
DRAW_ORBIT = False
DEBUG = True

font = pygame.font.SysFont(None, 18)


def draw_quadtree(quadtree, surface: Surface, pan_zoom_handler):
    screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
    boundary_screen = pan_zoom_handler.world_2_screen(quadtree.boundary.x, quadtree.boundary.y)
    boundary_screen_width = quadtree.boundary.width * pan_zoom_handler.get_zoom()
    boundary_screen_height = quadtree.boundary.height * pan_zoom_handler.get_zoom()
    boundary_screen_rect = Rect(
            boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

    if screen_rect.colliderect(boundary_screen_rect):
        draw.rect(surface, (5, 5, 155), boundary_screen_rect, 1)
        if quadtree.divided:
            draw_quadtree(quadtree.northEast, surface, pan_zoom_handler)
            draw_quadtree(quadtree.northWest, surface, pan_zoom_handler)
            draw_quadtree(quadtree.southEast, surface, pan_zoom_handler)
            draw_quadtree(quadtree.southWest, surface, pan_zoom_handler)


def draw_quadtree_boundary(quadtree, surface: Surface, pan_zoom_handler):
    screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
    boundary_screen = pan_zoom_handler.world_2_screen(quadtree.boundary.x, quadtree.boundary.y)
    boundary_screen_width = quadtree.boundary.width * pan_zoom_handler.get_zoom()
    boundary_screen_height = quadtree.boundary.height * pan_zoom_handler.get_zoom()
    boundary_screen_rect = Rect(
            boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

    if screen_rect.colliderect(boundary_screen_rect):
        draw.rect(surface, BLUE, boundary_screen_rect, 2)


def get_world_search_area():
    screen_rect = pygame.display.get_surface().get_rect()
    screen_search_area = screen_rect.inflate(-200, -200)  # Inflate by 200 pixels on each side
    world_x1, world_y1 = pan_zoom_handler.screen_2_world(screen_search_area.left, screen_search_area.top)
    world_x2, world_y2 = pan_zoom_handler.screen_2_world(screen_search_area.right, screen_search_area.bottom)
    return pygame.Rect(world_x1, world_y1, world_x2 - world_x1, world_y2 - world_y1)


def update_gif_index(obj, gif_frames):
    """
    updates gif index, sets new image frame
    """
    # update gif index and image
    current_time = time.time()
    if current_time > obj.gif_start + obj.gif_animation_time:
        # update gif index, set to zero after end of loop reached
        obj.gif_index = (obj.gif_index + 1) % len(gif_frames)
        obj.gif_start = current_time

        # kill sprite after gif loop
        if obj.gif_index == 0 and not obj.loop_gif:
            if obj.kill_after_gif_loop:
                obj.kill()
            return


def draw_objects(screen, qtree, screen_search_area):
    # draw the screen search area
    draw.rect(screen, YELLOW, screen_search_area, 2)

    # Convert screen coordinates to world coordinates
    world_search_area = get_world_search_area()

    # Query the quadtree for objects in the visible area
    found = qtree.query(world_search_area)
    for point in found:
        if isinstance(point, QTImage) or isinstance(point, QTMovingImage):
            draw_qt_image(screen, point)

        elif isinstance(point, QTFlickeringStar):
            draw_flickering_star(screen, point)

        elif isinstance(point, QTPulsatingStar):
            draw_pulsating_star(screen, point)


        elif isinstance(point, QTGif):
            draw_qt_gif(screen, point)



        # elif point.type == "qt_moving_image":
        #     draw_

        if point.selected:
            draw.rect(screen, RED, point.rect, 1)

        if DRAW_ORBIT:
            draw_orbit_circle(point)

        if DEBUG:
            text = font.render(point.type, 1, colors.frame_color)
            x, y = pan_zoom_handler.world_2_screen(point.x, point.y)
            screen.blit(text, (x, y))

            draw.rect(screen, GREEN, point.rect, 1)


def draw_qt_image(screen, point):
    image = get_image(point.image_name)

    # set alpha
    if point.image_alpha:
        image.set_alpha(point.image_alpha)

    # Determine size for scaling
    min_size = 3
    if point.rect.width < min_size or point.rect.height < min_size:
        size = (min_size, min_size)
    else:
        size = point.rect.size

    scaled_image = scale_image_cached(image, size)

    if point.rotation_angle == -1:
        # If no rotation, blit using original rect
        screen.blit(scaled_image, point.rect)
        return

    # Rotate the scaled image
    rotated_image = rotate_image_cached(scaled_image, point.rotation_angle)

    # Create a new rect for the rotated image
    rotated_rect = rotated_image.get_rect(**{point.align_image: pan_zoom_handler.world_2_screen(point.x, point.y)})

    # Blit the rotated image using its new rect
    screen.blit(rotated_image, rotated_rect)



# def draw_qt_moving_image(screen, point):
#     image = get_image(point.image_name)
#
#     # set alpha
#     if point.image_alpha:
#         image.set_alpha(point.image_alpha)
#
#     # Determine size for scaling
#     min_size = 3
#     if point.rect.width < min_size or point.rect.height < min_size:
#         size = (min_size, min_size)
#     else:
#         size = point.rect.size
#
#     scaled_image = scale_image_cached(image, size)
#
#     if point.rotation_angle == -1:
#         # If no rotation, blit using original rect
#         screen.blit(scaled_image, point.rect)
#         return
#
#     # Rotate the scaled image
#     rotated_image = rotate_image_cached(scaled_image, point.rotation_angle)
#
#     # Create a new rect for the rotated image
#     rotated_rect = rotated_image.get_rect(**{point.align_image: pan_zoom_handler.world_2_screen(point.x, point.y)})
#
#     # Blit the rotated image using its new rect
#     screen.blit(rotated_image, rotated_rect)



def draw_flickering_star(screen, point):
    color = point.colors[point.color_index]

    # Update the color index for the next iteration
    point.color_index = (point.color_index + 1) % len(point.colors)

    # Draw the flickering star using the current color
    # TODO: check if any other method  would be faster, also precalculate the line points
    pygame.draw.lines(
            screen,
            color,
            True,
            [(point.rect.x + 1, point.rect.y), (point.rect.x + 1, point.rect.y)])


def draw_pulsating_star(screen, point):
    # TODO: check if any other method  would be faster, specially the color calculation could be precalculated
    t = pygame.time.get_ticks() % (point.pulse_time * 1000) / (point.pulse_time * 1000)
    c = int(config.star_brightness / 2 * max(0.5, 1 + math.cos(2 * math.pi * t)))
    gfxdraw.filled_circle(
            screen,
            int(point.rect.x),
            int(point.rect.y),
            int(point.pulsating_star_size * pan_zoom_handler.zoom),
            (c, c, c))


def draw_qt_gif(screen, point):
    # get the gif frames
    gif_frames = get_gif_frames(point.gif_name)

    # update gif index
    update_gif_index(point, gif_frames)

    # get gif frame (= image)
    image = gif_frames[point.gif_index]

    # set alpha
    if point.image_alpha:
        image.set_alpha(point.image_alpha)

    # Determine size for scaling
    min_size = 3
    if point.rect.width < min_size or point.rect.height < min_size:
        size = (min_size, min_size)
    else:
        size = point.rect.size

    scaled_image = scale_image_cached(image, size)

    if point.rotation_angle == -1:
        # If no rotation, blit using original rect
        screen.blit(scaled_image, point.rect)
        return

    # Rotate the scaled image
    rotated_image = rotate_image_cached(scaled_image, point.rotation_angle)

    # Create a new rect for the rotated image
    rotated_rect = rotated_image.get_rect(**{point.align_image: pan_zoom_handler.world_2_screen(point.x, point.y)})

    # Blit the rotated image using its new rect
    screen.blit(rotated_image, rotated_rect)


def draw_orbit_circle(self):
    """
    draws the orbit
    """
    if not self.orbit_object:
        return

    color = colors.get_orbit_color(self.type)
    if self.orbit_object and config.show_orbit:
        pos = self.orbit_object.rect.center
        radius = math.dist(self.rect.center, pos)
        pygame.draw.circle(config.win, color, (pos[0], pos[1]), radius, 1)
