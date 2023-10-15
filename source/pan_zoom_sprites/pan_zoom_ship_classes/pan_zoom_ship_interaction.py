import random

import pygame

from source.multimedia_library.sounds import sounds
from source.utils import global_params
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups


class PanZoomShipInteraction:
    def __init__(self):
        # functionality
        self.orbiting = False
        self._selected = False
        self.target = None

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def orbit_object(self):
        return self._orbit_object

    @orbit_object.setter
    def orbit_object(self, value):
        self._orbit_object = value
        if value:
            self.target = None
            self.orbiting = True
            self.orbit_direction = random.choice([-1, 1])
        else:
            self.orbiting = False
            self.orbit_angle = None

    @property
    def enemy(self):
        return self._enemy

    @enemy.setter
    def enemy(self, value):
        self._enemy = value
        if not value:
            self.orbit_angle = None
            self.orbit_object = None
            self.target_reached = False

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)
            global_params.app.ship = self

    def get_hit_object(self):
        for obj in sprite_groups.planets:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in sprite_groups.ships:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in sprite_groups.ufos:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in sprite_groups.collectable_items:
            if obj.rect.collidepoint(pygame.mouse.get_pos()):
                return obj

        return None

        # if self.orbit_object:
        #     self.world_x, self.world_y= panzoom.screen_2_world(self.get_screen_x(), self.get_screen_y())
        #     self.orbit_object = None
