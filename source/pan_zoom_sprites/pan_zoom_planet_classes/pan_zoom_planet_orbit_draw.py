import math

import pygame

from source.configuration.game_config import config
from source.draw.circles import draw_dashed_circle
from source.gui.lod import level_of_detail
from source.handlers.color_handler import colors
from source.handlers.orbit_handler import get_orbit_pos
from source.handlers.pan_zoom_handler import pan_zoom_handler


def draw_orbit_simple(self):
    if not self.orbit_object:
        return

    if self.orbit_object and config.show_orbit:
        color = colors.get_orbit_color(self.type)
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * pan_zoom_handler.zoom
        draw_dashed_circle(config.win, color, pos, radius, 10, 1)


def draw_orbit_circle(self):
    """
    draws the orbit
    """
    if not self.orbit_object:
        return

    color = colors.get_orbit_color(self.type)
    if self.orbit_object and config.show_orbit:
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * pan_zoom_handler.get_zoom()
        pygame.draw.circle(config.win, color, (pos[0], pos[1]), radius, 1)


def draw_orbit(self):  # original
    """
    Draws the orbit with fancy circles
    """
    if not self.orbit_object or not self.orbit_radius:
        return

    color = colors.get_orbit_color(self.type)

    max_points = 25
    min_dist = 1
    max_dist = 1500
    size_factor = 12
    min_dist_to_draw = self.orbit_object.rect.width / 5

    if config.show_orbit:
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * pan_zoom_handler.get_zoom()
        width = 1  # initial width of the circle
        circumference = 2 * math.pi * radius
        num_points = math.ceil(circumference / max_points)
        points = []

        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)  # angle of the current point
            x = pos[0] + radius * math.cos(angle)  # x-coordinate of the current point
            y = pos[1] + radius * math.sin(angle)  # y-coordinate of the current point
            if level_of_detail.inside_screen((x, y)):
                if math.dist(self.rect.center, (x, y)) * pan_zoom_handler.get_zoom() > min_dist_to_draw / pan_zoom_handler.get_zoom():
                    points.append((int(x), int(y)))

        if len(points) > 1:
            for i in points:
                dist = math.dist(self.rect.center, (i[0], i[1]))
                if dist < min_dist:
                    dist = min_dist
                if dist > max_dist:
                    dist = max_dist

                size = self.orbit_object.rect.width / 2 * (size_factor / dist)
                if size > self.orbit_object.rect.width / 2:
                    size = self.orbit_object.rect.width / 2

                # color = dim_color(colors.ui_darker, dist, min_color_value)
                center = (i[0], i[1])
                pygame.draw.circle(config.win, color, center, size, width)


def draw_orbits(self):  # original
    if pan_zoom_handler.get_zoom() < 0.1:
        draw_orbit_circle(self)
    elif pan_zoom_handler.get_zoom() < 0.8 > 0.1:
        draw_orbit_simple(self)
    elif pan_zoom_handler.get_zoom() > 0.8:
        if level_of_detail.inside_screen(self.rect.center):
            draw_orbit(self)

#
# def draw_orbits(self):
#     draw_orbit_simple(self)
#     draw_orbit(self)
