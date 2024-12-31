import math
import random

import pygame

from source.configuration.game_config import config
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
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomGif

MISSILE_LAUNCH_INTERVAL = 2
EMP_PULSE_INTERVAL = 7
EMP_PULSE_TIME = 1
ENERGY_BLAST_POWER = 10


#
# class PanZoomPlanetDefence_:  # original
#     def __init__(self, parent):
#         self.parent = parent
#         self.attack_distance_raw = 300
#         self.attack_distance = self.attack_distance_raw
#         self.defence_units_names = building_factory.get_defence_unit_names()
#         self.last_missile_launch = time_handler.time
#         self.missile_launch_interval = MISSILE_LAUNCH_INTERVAL
#         self.emp_pulse_interval = EMP_PULSE_INTERVAL
#         self.last_emp = time_handler.time
#         self.emp_pulse_time = time_handler.time
#         self.emp_active = False
#         self.slider_height = 100
#         self.emp_progress_display = ProgressBar(win=self.parent.win,
#                 x=self.parent.get_screen_x(),
#                 y=self.parent.get_screen_y() + self.parent.get_screen_height() + self.parent.get_screen_height() / 5,
#                 width=self.parent.get_screen_width(),
#                 height=5,
#                 progress=lambda: 0.0,
#                 curved=True,
#                 completed_color=colors.frame_color,
#                 layer=self.parent.layer,
#                 parent=self.parent,
#                 h_align="right_outside",
#                 v_align="over_the_top",
#                 h_size=25, orientation=1, text="E.M.P."
#                 )
#         self.emp_progress_display.hide()
#
#     def __delete____(self, instance):  # unused ?
#         print("PanZoomPlanetDefence.__delete__: ")
#         self.parent = None
#         del self
#
#     def get_defence_units(self):
#         return [i for i in self.parent.economy_agent.buildings if i in self.defence_units_names]
#
#     def get_missiles(self):
#         return len([i for i in self.parent.economy_agent.buildings if i == "missile"])
#
#     def activate_electro_magnetic_impulse(self, pulse_time, ufo):
#         # if config.show_overview_buttons:
#         #     self.emp_progress_display.show()
#         if time_handler.time - pulse_time < self.emp_pulse_time:
#             # draw_electromagnetic_impulse(
#             #         self.parent.win,
#             #         self.parent.rect.center,
#             #         15,
#             #         self.attack_distance,
#             #         1, pulse_time * 1000, circles=5)
#
#             # gif_handler = GifHandler(self.parent, "emp.gif", loop=False, relative_gif_size=5.0)
#             emp_display = PanZoomGif(
#                     win=self.parent.win,
#                     world_x=self.parent.world_x,
#                     world_y=self.parent.world_y,
#                     world_width=200,
#                     world_height=200,
#                     layer=8,
#                     group=sprite_groups.universe,
#                     gif_name="emp.gif",
#                     gif_index=0,
#                     gif_animation_time=None,
#                     loop_gif=True,
#                     kill_after_gif_loop=False,
#                     image_alpha=None,
#                     rotation_angle=0
#                     )
#
#             ufo.emp_attacked = True
#         else:
#             self.emp_pulse_time = time_handler.time
#             self.emp_active = False
#
#         self.emp_progress_display.progress = lambda: ((time_handler.time - self.last_emp) / self.emp_pulse_interval)
#         # self.emp_progress_display.completed_color = [int(255/((time_handler.time - self.last_emp) / self.emp_pulse_interval)), self.emp_progress_display.completed_color[1], self.emp_progress_display.completed_color[2]]
#         # self.update_emp_progress_display()
#
#     def update_emp_progress_display(self):  # unused
#         # Calculate the percentage of time elapsed
#         elapsed_time_percentage = ((time_handler.time - self.last_emp) / self.emp_pulse_interval)
#
#         # Interpolate the color from green to red based on the elapsed time percentage
#         green_to_red = (
#                                1 - elapsed_time_percentage) * pygame.color.THECOLORS.get("green") + elapsed_time_percentage * pygame.color.THECOLORS.get("red")
#
#         # Update the progress bar color
#         self.emp_progress_display.completed_color = green_to_red
#
#         # Update the progress bar progress
#         self.emp_progress_display.progress = lambda: elapsed_time_percentage * 100
#
#     def draw_moving_image(self, defender: object, power: int, velocity: tuple):
#         MovingImage(
#                 self.parent.win,
#                 defender.rect.top,
#                 defender.rect.right,
#                 18,
#                 18,
#                 get_image("energy_25x25.png"),
#                 1,
#                 velocity,
#                 f"-{power}", pygame.color.THECOLORS["red"],
#                 "georgiaproblack", 1, defender.rect, target=None)
#
#     def activate_energy_blast(self):
#         # if not scope.draw_scope(
#         #         start_pos=self.parent.rect.center,
#         #         range_=self.attack_distance / pan_zoom_handler.zoom,
#         #         info={}):
#         #     return
#         #
#         # draw_dashed_circle(self.parent.win, colors.ui_darker, self.parent.rect.center, self.attack_distance, 10, 1)
#         if pygame.mouse.get_pressed()[2]:
#             hit_obj = sprite_groups.get_hit_object()
#             if hit_obj:
#                 if hit_obj in sprite_groups.ufos.sprites():
#                     hit_obj.energy -= ENERGY_BLAST_POWER
#                     self.draw_moving_image(hit_obj, ENERGY_BLAST_POWER, (0, 0))
#                     config.app.player.energy -= ENERGY_BLAST_POWER
#                     color = random.choice(list(pygame.color.THECOLORS.keys()))
#
#                     draw_zigzag_line(
#                             surface=self.parent.win,
#                             color=color,
#                             start_pos=self.parent.rect.center,
#                             end_pos=hit_obj.rect.center,
#                             num_segments=24)
#                     sounds.play_sound(sounds.laser)
#                     sounds.play_sound(sounds.electricity2)
#
#     def update(self):
#         defence_units = self.get_defence_units()
#         self.attack_distance = self.attack_distance_raw * pan_zoom_handler.get_zoom()
#
#         # handle self.emp_progress_display
#         if "electro magnetic impulse" in defence_units and config.show_overview_buttons:
#             self.emp_progress_display.set_progressbar_position()
#             self.emp_progress_display.show()
#         else:
#             self.emp_progress_display.hide()
#
#         # don't do anything if no defense units
#         if len(defence_units) == 0:
#             return
#
#         # ckeck for ufos in range self.attack_distance and then activate defence
#
#         for ufo in sprite_groups.ufos:
#             dist = math.dist(self.parent.rect.center, ufo.rect.center)
#             if dist < self.attack_distance:
#                 if "cannon" in defence_units:
#                     attack(self.parent, ufo)
#
#                 if "missile" in defence_units:
#                     missiles = self.get_missiles()
#                     if time_handler.time - self.missile_launch_interval / missiles > self.last_missile_launch:
#                         launch_missile(self.parent, ufo)
#                         self.last_missile_launch = time_handler.time
#
#                 if "energy blast" in defence_units:
#                     if self.parent == config.app.selected_planet:
#                         self.activate_energy_blast()
#
#                 if "electro magnetic impulse" in defence_units:
#                     if time_handler.time - self.emp_pulse_interval > self.last_emp:
#                         self.emp_active = True
#                         self.last_emp = time_handler.time
#                         self.emp_pulse_time = time_handler.time
#
#                     if self.emp_active:
#                         self.activate_electro_magnetic_impulse(EMP_PULSE_TIME, ufo)


class PanZoomPlanetDefence:  # new
    def __init__(self, parent):
        self.parent = parent
        self.attack_distance_raw = 300
        self.attack_distance = self.attack_distance_raw
        self.defence_units_names = building_factory.get_defence_unit_names()
        self.last_missile_launch = time_handler.time
        self.missile_launch_interval = MISSILE_LAUNCH_INTERVAL
        self.emp = EMP(self)

        self.ufos_in_attack_range = []

    def __delete____(self, instance):  # unused ?
        print("PanZoomPlanetDefence.__delete__: ")
        self.parent = None
        del self

    def get_defence_units(self):
        return [i for i in self.parent.economy_agent.buildings if i in self.defence_units_names]

    def get_missiles(self):
        return len([i for i in self.parent.economy_agent.buildings if i == "missile"])

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
        # set attack distance
        self.attack_distance = self.attack_distance_raw * pan_zoom_handler.get_zoom()

        # get defence units
        defence_units = self.get_defence_units()
        # don't do anything if no defense units
        if len(defence_units) == 0:
            return

        if "electro magnetic impulse" in defence_units:
            self.emp.update()

        # ckeck for ufos in range self.attack_distance and then activate defence
        self.ufos_in_attack_range = \
            [i for i in sprite_groups.ufos if math.dist(self.parent.rect.center, i.rect.center) < self.attack_distance]

        for ufo in self.ufos_in_attack_range:
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


class EMP:
    def __init__(self, parent: PanZoomPlanetDefence):
        self.weapon_handler = parent
        self.parent = self.weapon_handler.parent

        self.emp_pulse_interval = EMP_PULSE_INTERVAL
        self.last_emp = time_handler.time
        self.emp_pulse_time = time_handler.time
        self.emp_active = False

        self.emp_gif = PanZoomGif(
                win=self.parent.win,
                world_x=self.parent.world_x,
                world_y=self.parent.world_y,
                world_width=self.weapon_handler.attack_distance_raw * 2,
                world_height=self.weapon_handler.attack_distance_raw * 2,
                layer=8,
                group=sprite_groups.energy_reloader,
                gif_name="XDZT(1).gif",
                gif_index=0,
                gif_animation_time=None,
                loop_gif=False,
                kill_after_gif_loop=False,
                image_alpha=1,
                rotation_angle=0
                )

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
                h_size=25,
                orientation=1,
                text="E.M.P."
                )
        self.emp_progress_display.hide()
        self.emp_gif.visible = False

    def activate_electro_magnetic_impulse(self, pulse_time):  # gif_index issues
        if time_handler.time - pulse_time < self.emp_pulse_time:
            if not self.emp_gif.visible:
                # Reset and start the GIF only when it becomes visible
                self.emp_gif.gif_index = 0
            self.emp_gif.visible = True

            for i in self.weapon_handler.ufos_in_attack_range:
                i.emp_attacked = True
        else:
            self.emp_pulse_time = time_handler.time
            self.emp_active = False
            self.emp_gif.visible = False

        self.emp_progress_display.progress = lambda: ((time_handler.time - self.last_emp) / self.emp_pulse_interval)

    def update(self):
        # set the position
        x, y = pan_zoom_handler.screen_2_world(self.parent.rect.centerx, self.parent.rect.centery)
        self.emp_gif.set_position(x, y)

        # handle self.emp_progress_display
        if config.show_overview_buttons:
            self.emp_progress_display.set_progressbar_position()
            self.emp_progress_display.show()
        else:
            self.emp_progress_display.hide()

        # if pulse time is reached
        if time_handler.time - self.emp_pulse_interval > self.last_emp:
            # wait for enemies to be in range, if none, don't do anything
            if len(self.weapon_handler.ufos_in_attack_range) == 0:
                return

            # else activate EMP, set last_emp and pulse_time
            self.emp_active = True
            self.last_emp = time_handler.time
            self.emp_pulse_time = time_handler.time

        # finally activate electro magnetic impulse
        if self.emp_active:
            self.activate_electro_magnetic_impulse(EMP_PULSE_TIME)
