import math
import random

import pygame

from source.configuration.game_config import config
from source.draw.circles import draw_electromagnetic_impulse
from source.draw.zigzag_line import draw_zigzag_line
from source.factories.building_factory import building_factory
from source.gui.widgets.moving_image import MovingImage
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.handlers.weapon_handler import attack, launch_missile
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds

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
        self.last_missile_launch = time_handler.time
        self.missile_launch_interval = MISSILE_LAUNCH_INTERVAL
        self.emp_pulse_interval = EMP_PULSE_INTERVAL
        self.last_emp = time_handler.time
        self.emp_pulse_time = time_handler.time
        self.emp_active = False
        self.slider_height = 100
        self.emp_progress_display = ProgressBar(win=self.parent.win,
                x=self.parent.get_screen_x(),
                y=self.parent.get_screen_y() + self.parent.get_screen_height() + self.parent.get_screen_height() / 5,
                width=self.parent.get_screen_width(),
                height=5,
                progress=lambda: 0.0,
                curved=True,
                completed_color=colors.frame_color,
                layer=self.parent.layer,
                parent=self.parent,
                h_align="right_outside",
                v_align="over_the_top",
                h_size=25, orientation=1, text="E.M.P."
                )
        self.emp_progress_display.hide()

    def __delete____(self, instance):  # unused ?
        print("PanZoomPlanetDefence.__delete__: ")
        self.parent = None
        del self

    def get_defence_units(self):
        return [i for i in self.parent.economy_agent.buildings if i in self.defence_units_names]

    def get_missiles(self):
        return len([i for i in self.parent.economy_agent.buildings if i == "missile"])

    def activate_electro_magnetic_impulse(self, pulse_time, ufo):
        # if config.show_overview_buttons:
        #     self.emp_progress_display.show()
        if time_handler.time - pulse_time < self.emp_pulse_time:

            draw_electromagnetic_impulse(
                    self.parent.win,
                    self.parent.rect.center,
                    15,
                    self.attack_distance,
                    1, pulse_time * 1000, circles=5)

            # gif_handler = GifHandler(self.parent, "emp.gif", loop=False, relative_gif_size=5.0)

            ufo.emp_attacked = True
        else:
            self.emp_pulse_time = time_handler.time
            self.emp_active = False

        self.emp_progress_display.progress = lambda: ((time_handler.time - self.last_emp) / self.emp_pulse_interval)
        # self.emp_progress_display.completed_color = [int(255/((time_handler.time - self.last_emp) / self.emp_pulse_interval)), self.emp_progress_display.completed_color[1], self.emp_progress_display.completed_color[2]]
        # self.update_emp_progress_display()

    def update_emp_progress_display(self):  # unused
        # Calculate the percentage of time elapsed
        elapsed_time_percentage = ((time_handler.time - self.last_emp) / self.emp_pulse_interval)

        # Interpolate the color from green to red based on the elapsed time percentage
        green_to_red = (
                               1 - elapsed_time_percentage) * pygame.color.THECOLORS.get("green") + elapsed_time_percentage * pygame.color.THECOLORS.get("red")

        # Update the progress bar color
        self.emp_progress_display.completed_color = green_to_red

        # Update the progress bar progress
        self.emp_progress_display.progress = lambda: elapsed_time_percentage * 100

    def draw_moving_image(self, defender: object, power: int, velocity: tuple):
        MovingImage(
                self.parent.win,
                defender.rect.top,
                defender.rect.right,
                18,
                18,
                get_image("energy_25x25.png"),
                1,
                velocity,
                f"-{power}", pygame.color.THECOLORS["red"],
                "georgiaproblack", 1, defender.rect, target=None)

    def activate_energy_blast(self):
        # if not scope.draw_scope(
        #         start_pos=self.parent.rect.center,
        #         range_=self.attack_distance / pan_zoom_handler.zoom,
        #         info={}):
        #     return
        #
        # draw_dashed_circle(self.parent.win, colors.ui_darker, self.parent.rect.center, self.attack_distance, 10, 1)
        if pygame.mouse.get_pressed()[2]:
            hit_obj = sprite_groups.get_hit_object()
            if hit_obj:
                if hit_obj in sprite_groups.ufos.sprites():
                    hit_obj.energy -= ENERGY_BLAST_POWER
                    self.draw_moving_image(hit_obj, ENERGY_BLAST_POWER, (0, 0))
                    config.app.player.energy -= ENERGY_BLAST_POWER
                    color = random.choice(list(pygame.color.THECOLORS.keys()))

                    draw_zigzag_line(
                            surface=self.parent.win,
                            color=color,
                            start_pos=self.parent.rect.center,
                            end_pos=hit_obj.rect.center,
                            num_segments=24)
                    sounds.play_sound(sounds.laser)
                    sounds.play_sound(sounds.electricity2)

    def update(self):
        defence_units = self.get_defence_units()
        self.attack_distance = self.attack_distance_raw * pan_zoom_handler.get_zoom()

        # handle self.emp_progress_display
        if "electro magnetic impulse" in defence_units and config.show_overview_buttons:
            self.emp_progress_display.set_progressbar_position()
            self.emp_progress_display.show()
        else:
            self.emp_progress_display.hide()

        # don't do anything if no defense units
        if len(defence_units) == 0:
            return

        # ckeck for ufos in range self.attack_distance and then activate defence

        for ufo in sprite_groups.ufos:
            dist = math.dist(self.parent.rect.center, ufo.rect.center)
            if dist < self.attack_distance:
                if "cannon" in defence_units:
                    attack(self.parent, ufo)

                if "missile" in defence_units:
                    missiles = self.get_missiles()
                    if time_handler.time - self.missile_launch_interval / missiles > self.last_missile_launch:
                        launch_missile(self.parent, ufo)
                        self.last_missile_launch = time_handler.time

                if "energy blast" in defence_units:
                    if self.parent == config.app.selected_planet:
                        self.activate_energy_blast()

                if "electro magnetic impulse" in defence_units:
                    if time_handler.time - self.emp_pulse_interval > self.last_emp:
                        self.emp_active = True
                        self.last_emp = time_handler.time
                        self.emp_pulse_time = time_handler.time

                    if self.emp_active:
                        self.activate_electro_magnetic_impulse(EMP_PULSE_TIME, ufo)
