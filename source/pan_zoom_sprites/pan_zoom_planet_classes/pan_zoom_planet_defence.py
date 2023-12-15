import random
import time

import pygame

from source.draw import scope
from source.draw.circles import draw_electromagnetic_impulse
from source.draw.zigzag_line import draw_zigzag_line
from source.factories.building_factory import building_factory
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.attack import attack, launch_missile
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.positioning import get_distance

MISSILE_LAUNCH_INTERVAL = 2
EMP_PULSE_INTERVAL = 7
EMP_PULSE_TIME = 1
ENERGY_BLAST_POWER = 10


class PanZoomPlanetDefence:
    def __init__(self, parent):
        self.parent = parent
        self.attack_distance_raw = 300
        self.attack_distance = self.attack_distance_raw
        self.defence_units_names = building_factory.get_defence_unit_names()
        self.last_missile_launch = time.time()
        self.missile_launch_interval = MISSILE_LAUNCH_INTERVAL
        self.emp_pulse_interval = EMP_PULSE_INTERVAL
        self.last_emp = time.time()
        self.emp_pulse_time = time.time()
        self.emp_active = False


    def __delete__(self, instance):
        print("PanZoomPlanetDefence.__delete__: ")
        self.parent = None
        del self

    def get_defence_units(self):
        return [i for i in self.parent.buildings if i in self.defence_units_names]

    def get_missiles(self):
        return len([i for i in self.parent.buildings if i == "missile"])

    def activate_electro_magnetic_impulse(self, pulse_time, ufo):
        if time.time() - pulse_time < self.emp_pulse_time:
            draw_electromagnetic_impulse(
                self.parent.win,
                self.parent.rect.center,
                15,
                self.attack_distance,
                1, pulse_time * 1000, circles=5)

            ufo.emp_attacked = True

        else:
            self.emp_pulse_time = time.time()
            self.emp_active = False

    def activate_energy_blast(self):
        scope.draw_scope(self.parent)
        if pygame.mouse.get_pressed()[2]:
            hit_obj = self.parent.get_hit_object()
            if hit_obj:
                if hit_obj in sprite_groups.ufos.sprites():
                    hit_obj.energy -= ENERGY_BLAST_POWER
                    global_params.app.player.energy -= ENERGY_BLAST_POWER
                    color = random.choice(list(pygame.color.THECOLORS.keys()))
                    # draw_zigzag_line(
                    #     surface=self.parent.win,
                    #     color=color,
                    #     start_pos=self.parent.rect.center,
                    #     end_pos=hit_obj.rect.center,
                    #     num_segments=24,
                    #     pan_zoom_handler=pan_zoom_handler)
                    draw_zigzag_line(
                        surface=self.parent.win,
                        color=color,
                        start_pos=self.parent.rect.center,
                        end_pos=hit_obj.rect.center,
                        num_segments=24)
                    sounds.play_sound(sounds.laser)
                    sounds.play_sound(sounds.electricity2)

    def defend(self):
        defence_units = self.get_defence_units()
        self.attack_distance = self.attack_distance_raw * self.parent.get_zoom()
        if len(defence_units) == 0:
            return

        # for ufo in global_params.app.ufos:
        for ufo in sprite_groups.ufos:
            dist = get_distance(self.parent.rect.center, ufo.rect.center)
            if dist < self.attack_distance:
                if "cannon" in defence_units:
                    attack(self.parent, ufo)

                if "missile" in defence_units:
                    missiles = self.get_missiles()
                    if time.time() - self.missile_launch_interval / missiles > self.last_missile_launch:
                        launch_missile(self.parent, ufo)
                        self.last_missile_launch = time.time()

                if "energy blast" in defence_units:
                    if self.parent == global_params.app.selected_planet:
                        self.activate_energy_blast()

                if "electro magnetic impulse" in defence_units:
                    pass

                    if time.time() - self.emp_pulse_interval > self.last_emp:
                        self.emp_active = True
                        self.last_emp = time.time()
                        self.emp_pulse_time = time.time()

                    if self.emp_active:
                        self.activate_electro_magnetic_impulse(EMP_PULSE_TIME, ufo)

