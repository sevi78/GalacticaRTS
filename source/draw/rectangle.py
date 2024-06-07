import pygame
import pygame.draw

from source.draw.arc_with_dashes import draw_arc_with_dashes
from source.draw.dashed_line import draw_dashed_line
from source.handlers.pan_zoom_handler import pan_zoom_handler


def draw_transparent_rounded_rect(surface, color, rect, radius, alpha):
    # Create a Surface with the correct dimensions and with per-pixel alpha enabled
    rect_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    # Draw a transparent rounded rectangle on the created Surface
    pygame.draw.rect(rect_surface, color + (alpha,), (0, 0, rect[2], rect[3]), border_radius=radius)
    # Blit the transparent rounded rectangle onto the target surface at the correct position
    surface.blit(rect_surface, rect[:2])

    return rect_surface


def draw_dashed_rounded_rectangle(surf, color, rect, width, border_radius, dash_length):
    x, y, w, h = rect
    # Draw the straight dashed edges
    draw_dashed_line(surf, color, (x + border_radius, y), (x + w - border_radius, y), width, dash_length)  # Top
    draw_dashed_line(surf, color, (x + border_radius, y + h), (
        x + w - border_radius, y + h), width, dash_length)  # Bottom
    draw_dashed_line(surf, color, (x, y + border_radius), (x, y + h - border_radius), width, dash_length)  # Left
    draw_dashed_line(surf, color, (x + w, y + border_radius), (
        x + w, y + h - border_radius), width, dash_length)  # Right

    # Draw the dashed rounded corners
    draw_arc_with_dashes(surf, color, (x, y), 180, 270, border_radius, dash_length, width)  # Top-left
    draw_arc_with_dashes(surf, color, (
        x + w - 2 * border_radius, y), 270, 360, border_radius, dash_length, width)  # Top-right
    draw_arc_with_dashes(surf, color, (
        x, y + h - 2 * border_radius), 90, 180, border_radius, dash_length, width)  # Bottom-left
    draw_arc_with_dashes(surf, color, (
        x + w - 2 * border_radius, y + h - 2 * border_radius), 0, 90, border_radius, dash_length, width)  # Bottom-right


def draw_zoomable_rect(surface, color, world_x, world_y, width, height, **kwargs):
    border_radius = kwargs.get("border_radius", 0)
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    rect = pygame.Rect(screen_x, screen_y, width * pan_zoom_handler.zoom, height * pan_zoom_handler.zoom)
    pygame.draw.rect(surface, color, rect, 1, border_radius)
