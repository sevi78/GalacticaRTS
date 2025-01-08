import math
import time

import pygame
from pygame import Surface, Rect, draw, gfxdraw

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, scale_image_cached, rotate_image_cached, get_gif_frames
# from source.pygame_shaders import pygame_shaders

from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.view.game_objects.qt_game_objects import QTImage, QTMovingImage
from source.qt_universe.view.qt_view_config.qt_draw_config import DARK_BLUE

#
# # define the target surface, the surface where the shader will be drawn onto
# target_surface = pygame.Surface((1920,1080))
# target_surface.fill((0, 0, 0))
#
# # define the shader
# ring_shader = pygame_shaders.Shader("vertex.txt", "ring_atmosphere.glsl", target_surface)  # <- give it to our shader
# ring_shader.send("iResolution", target_surface.get_size())
#
# def draw_shader(screen, image_rect):
#     # render the shader
#     ring_shader.send("iPos", image_rect.center)
#     ring_shader.send("iRadius", image_rect.width)
#     ring_shader.send("iColor", (0.3, 0.1, 0.2, 0.0))
#     ring_shader.send("iBlur", 80)
#     rendered_shader = ring_shader.render()
#
#     # then render the shader onto the display
#     screen.blit(rendered_shader, (0, 0), special_flags=pygame.BLEND_MAX)

def draw_quadtree(quadtree, surface: Surface, pan_zoom_handler) -> None:
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


def draw_quadtree_boundary(quadtree, surface: Surface, pan_zoom_handler) -> None:
    screen_rect = Rect(0, 0, surface.get_width(), surface.get_height())
    boundary_screen = pan_zoom_handler.world_2_screen(quadtree.boundary.x, quadtree.boundary.y)
    boundary_screen_width = quadtree.boundary.width * pan_zoom_handler.get_zoom()
    boundary_screen_height = quadtree.boundary.height * pan_zoom_handler.get_zoom()
    boundary_screen_rect = Rect(
            boundary_screen[0], boundary_screen[1], boundary_screen_width, boundary_screen_height)

    if screen_rect.colliderect(boundary_screen_rect):
        draw.rect(surface, DARK_BLUE, boundary_screen_rect, 1)


def update_gif_index(obj, gif_frames) -> None:
    """
    updates gif index, checks if gif loop should be killed
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


def draw_flickering_star(screen, point):
    color_ = point.colors[point.color_index]

    # Calculate the brightness factor
    brightness_factor = pan_zoom_handler.get_zoom() / pan_zoom_handler.zoom_max * 900
    brightness_factor = max(0, min(1, brightness_factor))  # Ensure it's between 0 and 1

    # Apply the brightness factor to the color, maxing out at 255
    color = [min(255, int(c * brightness_factor)) for c in color_]

    # Check if all color values are less than 1 (for extreme dimming cases)
    all_dim = all(c < 2 for c in color)

    if all_dim:
        point.visible = False
        return
    else:
        point.visible = True
        # Update the color index for the next iteration
        point.color_index = (point.color_index + 1) % len(point.colors)

        # Draw the flickering star using the current color
        pygame.draw.lines(
                screen,
                color,
                True,
                [(point.rect.x + 1, point.rect.y), (point.rect.x + 1, point.rect.y)]
                )


def draw_pulsating_star(screen, point) -> None:
    # if point.lod == 0:
    #     return
    # TODO: check if any other method  would be faster, specially the color calculation could be precalculated
    t = pygame.time.get_ticks() % (point.pulse_time * 1000) / (point.pulse_time * 1000)
    c = int(config.star_brightness / 2 * max(0.5, 1 + math.cos(2 * math.pi * t)))
    gfxdraw.filled_circle(
            screen,
            int(point.rect.x),
            int(point.rect.y),
            int(point.pulsating_star_size * pan_zoom_handler.zoom),
            (c, c, c))


def draw_qt_image_(screen, point: QTImage or QTMovingImage) -> None:
    """
    draws a qt image of type:
    - QTImage
    - QTMovingImage
    - GameObject

    """

    # Determine size for scaling
    min_size = 3
    if point.rect.width < min_size or point.rect.height < min_size:
        size = (min_size, min_size)
    else:
        size = point.rect.size

    # Get the image
    image = get_image(point.image_name)

    # set alpha
    if point.image_alpha:
        image.set_alpha(point.image_alpha)

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

def draw_qt_image(screen, point: QTImage or QTMovingImage) -> None:
    """
    draws a qt image of type:
    - QTImage
    - QTMovingImage
    - GameObject

    """

    # Determine size for scaling
    min_size = 3
    if point.rect.width < min_size or point.rect.height < min_size:
        size = (min_size, min_size)
    else:
        size = point.rect.size

    # Get the image
    image = get_image(point.image_name)

    # set alpha
    if point.image_alpha:
        image.set_alpha(point.image_alpha)

    scaled_image = scale_image_cached(image, size)

    if point.rotation_angle == -1:
        # If no rotation, blit using original rect
        screen.blit(scaled_image, point.rect)
        # draw_shader(screen, point.rect)


    # Rotate the scaled image
    rotated_image = rotate_image_cached(scaled_image, point.rotation_angle)

    # Create a new rect for the rotated image
    rotated_rect = rotated_image.get_rect(**{point.align_image: pan_zoom_handler.world_2_screen(point.x, point.y)})

    # Blit the rotated image using its new rect
    screen.blit(rotated_image, rotated_rect)
    # draw_shader(screen, rotated_rect)





def draw_qt_gif(screen, point) -> None:
    # if point.lod == 0 and not point.type == "sun":
    #     return

    # min_size = 3
    # if point.rect.width < min_size or point.rect.height < min_size:
    #     draw.circle(screen, point.color, point.rect.center, int(point.rect.height / 2))
    #     return

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

    if point.type == "sun":
        resize_factor = 0.75
        sub_image_size = (size[0] * resize_factor, size[1] * resize_factor)
        scaled_sub_image = scale_image_cached(get_image("sonnecomic_110x110.png"), sub_image_size)
        scaled_sub_image_rect = scaled_sub_image.get_rect(**{point.align_image: pan_zoom_handler.world_2_screen(point.x, point.y)})
        screen.blit(scaled_sub_image, scaled_sub_image_rect)

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


def draw_orbit_circle(surface, obj) -> None:
    # if obj.lod == 0:
    #     return
    """
    draws the orbit
    """
    if not obj.orbit_object:
        return

    color = colors.get_orbit_color(obj.type)
    if obj.orbit_object:  # and config.show_orbit:
        pos = obj.orbit_object.rect.center
        radius = math.dist(obj.rect.center, pos)
        pygame.draw.circle(surface, color, (pos[0], pos[1]), radius, 1)
        # print (obj.lod)
