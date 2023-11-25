import math

import pygame

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.physics.orbit import get_orbit_pos
from source.utils import global_params
from source.utils.colors import colors
from source.utils.positioning import get_distance

ORBIT_COLOR = colors.ui_dark

def draw_orbit_simple(self):
    """
    draws the orbit
    """
    if not self.orbit_object:
        return

    if self.orbit_object and global_params.show_orbit:
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * pan_zoom_handler.zoom
        width = 1  # initial width of the circle
        circumference = 2 * math.pi * radius

        num_points = math.ceil(circumference / 15)
        points = []
        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)  # angle of the current point
            x = pos[0] + radius * math.cos(angle)  # x-coordinate of the current point
            y = pos[1] + radius * math.sin(angle)  # y-coordinate of the current point
            if inside_screen((x, y), border=0):
                points.append((int(x), int(y)))

        if len(points) > 1:
            for i in points:
                pygame.draw.rect(global_params.win, ORBIT_COLOR, (i[0], i[1], width, width))


def draw_orbit_circle(self):
    """
    draws the orbit
    """
    if not self.orbit_object:
        return

    if self.orbit_object and global_params.show_orbit:
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * self.get_zoom()
        pygame.draw.circle(global_params.win, colors.ui_darker, (pos[0], pos[1]), radius, 1)


def draw_orbit(self):
    """
    Draws the orbit
    """
    if not self.orbit_object or not self.orbit_radius:
        return

    max_points = 25
    min_dist = 1
    max_dist = 1500
    size_factor = 12
    min_dist_to_draw = self.orbit_object.rect.width / 5

    if global_params.show_orbit:
        pos = get_orbit_pos(self)
        radius = self.orbit_radius * self.get_zoom()
        width = 1  # initial width of the circle
        circumference = 2 * math.pi * radius
        num_points = math.ceil(circumference / max_points)
        points = []

        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)  # angle of the current point
            x = pos[0] + radius * math.cos(angle)  # x-coordinate of the current point
            y = pos[1] + radius * math.sin(angle)  # y-coordinate of the current point
            if inside_screen((x, y), border=0):
                if get_distance(self.center, (x, y)) * self.get_zoom() > min_dist_to_draw / self.get_zoom():
                    points.append((int(x), int(y)))

        if len(points) > 1:
            for i in points:
                dist = get_distance(self.center, (i[0], i[1]))
                if dist < min_dist:
                    dist = min_dist
                if dist > max_dist:
                    dist = max_dist

                size = self.orbit_object.rect.width / 2 * (size_factor / dist)
                if size > self.orbit_object.rect.width / 2:
                    size = self.orbit_object.rect.width / 2

                #color = dim_color(colors.ui_darker, dist, min_color_value)
                center = (i[0], i[1])
                pygame.draw.circle(global_params.win, ORBIT_COLOR, center, size, width)


def draw_orbits(self):
    if self.get_zoom() < 0.1:
        draw_orbit_circle(self)
    elif self.get_zoom() < 0.8 > 0.1:
        draw_orbit_simple(self)
    elif self.get_zoom() > 0.8:
        draw_orbit(self)

    # draw_orbit_angle(self)
