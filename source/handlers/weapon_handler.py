import copy
import random

import pygame

from source.factories.weapon_factory import weapon_factory
from source.gui.lod import inside_screen
from source.multimedia_library.sounds import sounds


class WeaponHandler:
    def __init__(self, parent, current_weapon):
        self.parent = parent
        self.all_weapons = copy.deepcopy(weapon_factory.get_all_weapons())
        self.weapons = {}
        self.current_weapon = self.all_weapons[current_weapon]
        self.current_weapon_select = ""

    def attack(self, defender):
        if not inside_screen(self.parent.get_screen_position()):
            return

        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)

        startpos = (self.parent.rect.centerx, self.parent.rect.centery)
        endpos = (defender.rect.centerx + r0, defender.rect.centery + r0)

        # shoot laser
        if r == 2 and defender.energy > 0:
            pygame.draw.line(surface=self.parent.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["white"], width=2)

            # make damage to target
            defender.energy -= self.gun_power
            sounds.play_sound(sounds.laser)

        if defender.energy <= defender.energy_max / 2:
            defender.target = self.parent

        if defender.energy <= 0:
            # explode
            defender.end_object()
            self.parent.enemy = None
