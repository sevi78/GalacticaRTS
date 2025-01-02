import math
import random

import pygame

from source.configuration.game_config import config
from source.draw.zigzag_line import draw_zigzag_line
from source.factories.building_factory import building_factory
from source.factories.universe_factory import universe_factory
from source.gui.widgets.moving_image import MovingImage
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_missile import MISSILE_POWER, Missile
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomGif

MISSILE_LAUNCH_INTERVAL = 2
EMP_PULSE_INTERVAL = 7
EMP_PULSE_TIME = 1
ENERGY_BLAST_POWER = 10
CANNON_GUNPOWER = 3
MOVING_IMAGE_DRAW_REDUCER_RATE = 50
MOVING_IMAGE_RANDOM_VELOCITY_RANGE = 3


class PanZoomPlanetDefence:  # new
    def __init__(self, parent):
        self.parent = parent
        self.attack_distance_raw = 300
        self.attack_distance = self.attack_distance_raw
        self.defence_units_names = building_factory.get_defence_unit_names()
        self.last_missile_launch = time_handler.time
        self.missile_launch_interval = MISSILE_LAUNCH_INTERVAL
        self.resize_factor = 1 / self.parent.image_raw.get_rect().width * self.parent.world_width
        self.emp = EMP(self)
        self.enemies_in_attack_range = []
        self.moving_image_draw_reducer = 0
        self.moving_image_draw_reducer_rate = MOVING_IMAGE_DRAW_REDUCER_RATE
        self.moving_image_random_velocities = [(x, y) for x in
                                               range(-MOVING_IMAGE_RANDOM_VELOCITY_RANGE, MOVING_IMAGE_RANDOM_VELOCITY_RANGE)
                                               for y in
                                               range(-MOVING_IMAGE_RANDOM_VELOCITY_RANGE, MOVING_IMAGE_RANDOM_VELOCITY_RANGE)]

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
        # set cursor to aim if not pressed but energy blast is active
        config.app.cursor.set_cursor("aim")

        if pygame.mouse.get_pressed()[2]:
            # set moving image reducer to ensure they are not drawn every frame
            self.moving_image_draw_reducer += 1

            # set cursor to shoot
            config.app.cursor.set_cursor("shoot")

            # get hit objects
            hitobjects = [i for i in self.enemies_in_attack_range if i.rect.collidepoint(pygame.mouse.get_pos())]
            hit_obj = hitobjects[0] if hitobjects else None

            if hit_obj:
                # add damage to hit object
                hit_obj.energy -= ENERGY_BLAST_POWER

                # draw moving image every x-th frame
                if self.moving_image_draw_reducer > self.moving_image_draw_reducer_rate:
                    self.draw_moving_image(hit_obj, ENERGY_BLAST_POWER * self.moving_image_draw_reducer_rate, random.choice(self.moving_image_random_velocities))
                    self.moving_image_draw_reducer = 0

                # reduce energy from player
                config.app.player.stock["energy"] -= ENERGY_BLAST_POWER

                # get random color
                color = random.choice(list(pygame.color.THECOLORS.keys()))

                # draw zigzag line
                draw_zigzag_line(
                        surface=self.parent.win,
                        color=color,
                        start_pos=self.parent.rect.center,
                        end_pos=hit_obj.rect.center,
                        num_segments=24)

                # play sound
                sounds.play_sound(sounds.laser)
                sounds.play_sound(sounds.electricity2)

    def cannon(self, attacker, defender) -> None:
        """
        used by planet defence
        """

        # this might be deleted: should not attacker attack defender even if not on screen ???
        # if not level_of_detail.inside_screen(attacker.get_screen_position()):
        #     return

        # if attacker is planet
        if attacker.property == "planet":
            gun_power = len([i for i in attacker.economy_agent.buildings if i == "cannon"]) * CANNON_GUNPOWER
        else:
            gun_power = attacker.gun_power

        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)
        r_m = random.randint(0, 20)

        startpos = (attacker.rect.center[0], attacker.rect.center[1])
        endpos = (defender.rect.center[0] + r0, defender.rect.center[1] + r0)

        # shoot laser
        if r == 2 and defender.energy > 0:
            pygame.draw.line(surface=attacker.win, start_pos=startpos, end_pos=endpos,
                    color=pygame.color.THECOLORS["white"], width=2)

            self.draw_moving_image(defender,gun_power , random.choice(self.moving_image_random_velocities))

            # make damage to target
            defender.energy -= gun_power
            sounds.play_sound(sounds.laser)

        if defender.energy <= defender.energy_max / 2:
            defender.target = attacker

    def launch_missile(self, attacker, defender) -> None:
        app = config.app
        screen = app.win
        x, y = pan_zoom_handler.screen_2_world(attacker.rect.centerx, attacker.rect.centery)
        # rx = int(attacker.rect.width / 4)
        # ry = int(attacker.rect.height / 4)
        # x += random.randint(-rx, rx)
        # y += random.randint(-ry, ry)

        if defender.energy - MISSILE_POWER >= 0:
            # missile = PanZoomMissile(
            #         screen,
            #         x,
            #         y,
            #         42,
            #         17,
            #         pan_zoom_handler,
            #         "missile_42x17.gif",
            #         group="missiles",
            #         loop_gif=True,
            #         move_to_target=True,
            #         align_image="topleft",
            #         explosion_relative_gif_size=1.0,
            #         layer=9,
            #         debug=False,
            #         target=defender,
            #         appear_at_start=True, zoomable=True)

            missile = Missile(
                    win=self.parent.win,
                    world_x=x,
                    world_y=y,
                    world_width=42 * self.resize_factor,
                    world_height=17 * self.resize_factor,
                    layer=9,
                    group=sprite_groups.missiles,
                    gif_name="missile_42x17.gif",
                    gif_index=0,
                    gif_animation_time=None,
                    loop_gif=True,
                    kill_after_gif_loop=True,
                    image_alpha=None,
                    rotation_angle=0,
                    movement_speed=random.randint(2, 10),
                    world_rect=universe_factory.world_rect,
                    target=defender,
                    missile_power=MISSILE_POWER,
                    friction=random.uniform(0.95, 0.99),
                    explosion_relative_gif_size=random.uniform(1.0, 1.5), )

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
        all_enemies = sprite_groups.ufos.sprites() + sprite_groups.ships.sprites()
        self.enemies_in_attack_range = \
            [i for i in all_enemies if
             math.dist(self.parent.rect.center, i.rect.center) < self.attack_distance and i.owner != self.parent.owner]

        for enemy in self.enemies_in_attack_range:
            if "cannon" in defence_units:
                self.cannon(self.parent, enemy)

            if "missile" in defence_units:
                missiles = self.get_missiles()
                if time_handler.time - self.missile_launch_interval / missiles > self.last_missile_launch:
                    self.launch_missile(self.parent, enemy)
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
                gif_name="maria-yakovleva-lightning-ball1.gif",
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

            for i in self.weapon_handler.enemies_in_attack_range:
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
            if len(self.weapon_handler.enemies_in_attack_range) == 0:
                return

            # else activate EMP, set last_emp and pulse_time
            self.emp_active = True
            self.last_emp = time_handler.time
            self.emp_pulse_time = time_handler.time

        # finally activate electro magnetic impulse
        if self.emp_active:
            self.activate_electro_magnetic_impulse(EMP_PULSE_TIME)
