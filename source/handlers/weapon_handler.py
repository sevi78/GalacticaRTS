import copy
import random

import pygame
from source.test.beam_test import draw_segmented_beam

from source.configuration.game_config import config
from source.draw.circles import draw_transparent_circle
from source.factories.universe_factory import universe_factory
from source.factories.weapon_factory import weapon_factory
from source.gui.widgets.moving_image import MovingImage
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image, rotate_image_to
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_missile import PanZoomMissile, MISSILE_POWER, Missile
from source.pan_zoom_sprites.rack import Rack

CANNON_GUNPOWER = 3


class WeaponRack(Rack):
    def __init__(self, width, height, pivot: tuple, points_by_level: dict):
        self.level = 0

        self.points_by_level = points_by_level
        self.levels = list(points_by_level.keys())
        super().__init__(width, height, pivot, self.points_by_level[self.level])

    def set_level(self, level):
        self.level = level
        self.points_raw = self.points_by_level[level]
        self.points = self.points_by_level[level]


def calculate_weapon_positions_(spaceship_size, rocket_size, levels):
    offset_x = (spaceship_size[0] - rocket_size[0] * 2) / 6
    offset_y = 16

    positions = {}
    for level in levels:
        if level == 0:
            positions[level] = [(offset_x + rocket_size[0] / 2, offset_y)]
        elif level == 1:
            positions[level] = [
                (offset_x + rocket_size[0] / 2, offset_y),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2, offset_y)
                ]
        elif level == 2:
            outside_offset = 3
            outer_y_offset = 5
            inner_y_offset = outer_y_offset - 5
            positions[level] = [
                (offset_x + outside_offset + rocket_size[0] / 2, offset_y - outer_y_offset),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2 - outside_offset, offset_y - outer_y_offset),
                (offset_x - outside_offset + rocket_size[0] / 2, offset_y - inner_y_offset),
                (spaceship_size[0] - offset_x - rocket_size[0] / 2 + outside_offset, offset_y - inner_y_offset)
                ]

    return positions


# def calculate_weapon_positions(spaceship_size, rocket_size, levels, resize_factor=1):
#     offset_x = (spaceship_size[0] - rocket_size[0] * 2) / 6
#     offset_y = 16
#
#     positions = {}
#     for level in levels:
#         if level == 0:
#             positions[level] = [(offset_x + rocket_size[0] / 2, offset_y)]
#         elif level == 1:
#             positions[level] = [
#                 (offset_x + rocket_size[0] / 2, offset_y),
#                 (spaceship_size[0] - offset_x - rocket_size[0] / 2, offset_y)
#                 ]
#         elif level == 2:
#             outside_offset = 3
#             outer_y_offset = 5
#             inner_y_offset = outer_y_offset - 5
#             positions[level] = [
#                 (offset_x + outside_offset + rocket_size[0] / 2, offset_y - outer_y_offset),
#                 (spaceship_size[0] - offset_x - rocket_size[0] / 2 - outside_offset, offset_y - outer_y_offset),
#                 (offset_x - outside_offset + rocket_size[0] / 2, offset_y - inner_y_offset),
#                 (spaceship_size[0] - offset_x - rocket_size[0] / 2 + outside_offset, offset_y - inner_y_offset)
#                 ]
#
#     return positions


def calculate_weapon_positions(spaceship_size, rocket_size, levels, resize_factor):
    # Apply resize_factor to spaceship and rocket sizes
    adjusted_spaceship_size = (spaceship_size[0] * resize_factor, spaceship_size[1] * resize_factor)
    adjusted_rocket_size = (rocket_size[0] * resize_factor, rocket_size[1] * resize_factor)

    offset_x = (adjusted_spaceship_size[0] - adjusted_rocket_size[0] * 2) / 6
    offset_y = 16 * resize_factor

    positions = {}
    for level in levels:
        if level == 0:
            positions[level] = [(offset_x + adjusted_rocket_size[0] / 2, offset_y)]
        elif level == 1:
            positions[level] = [
                (offset_x + adjusted_rocket_size[0] / 2, offset_y),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2, offset_y)
                ]
        elif level == 2:
            outside_offset = 3 * resize_factor
            outer_y_offset = 5 * resize_factor
            inner_y_offset = outer_y_offset - 5 * resize_factor
            positions[level] = [
                (offset_x + outside_offset + adjusted_rocket_size[0] / 2, offset_y - outer_y_offset),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2 - outside_offset,
                 offset_y - outer_y_offset),
                (offset_x - outside_offset + adjusted_rocket_size[0] / 2, offset_y - inner_y_offset),
                (adjusted_spaceship_size[0] - offset_x - adjusted_rocket_size[0] / 2 + outside_offset,
                 offset_y - inner_y_offset)
                ]

    return positions


def create_weapon_rack(spaceship_size, weapon_size, levels, resize_factor):
    positions = calculate_weapon_positions(spaceship_size, weapon_size, [0, 1, 2], resize_factor)
    rack = WeaponRack(
            width=spaceship_size[0],
            height=spaceship_size[1],
            pivot=(spaceship_size[0] / 2, spaceship_size[1] / 2),
            points_by_level=positions
            )
    return rack


class WeaponHandler:
    """
    This class handles the weapons:
        - laser
        - rocket
        - phaser

    :param parent: parent object: the game object (ship/ufo or planet)
    :param current_weapon: name of the current weapon
     kwargs:
        - weapons: dictionary of all weapons of the object
    """

    def __init__(self, parent, current_weapon, **kwargs):
        self.laser_last_shoot = None
        self.parent = parent
        self.all_weapons = copy.deepcopy(weapon_factory.get_all_weapons())
        self.weapons = kwargs.get("weapons", {})
        self.current_weapon = self.all_weapons[current_weapon]
        self.current_weapon_select = ""
        self.max_weapons_upgrade_level = 2
        self.setup_interval_timers()

        # setup weapon rack
        self.no_weapon_image = copy.copy(self.parent.image_raw)
        self.weapon_images = {
            "rocket": get_image("rocket_attached.png"),
            "laser": get_image("laser_attached.png"),
            "phaser": get_image("phaser_attached.png")
            }

        # this is the image that has the weapons blitted onto
        self.weapon_image = copy.copy(self.parent.image_raw)

        # adjust sizes to setuo the rack correctly
        self.spaceship_size = (self.parent.world_width, self.parent.world_height)

        # get the original rocket size
        self.weapon_size = (17, 42)

        # calculate the resize factr
        self.resize_factor = 1 / self.parent.image_raw.get_rect().width * self.parent.world_width

        # calculate all positions
        self.all_level_rack_positions = calculate_weapon_positions(self.parent.image_raw.get_rect().size, self.weapon_size, [
            0, 1, 2], self.resize_factor)

        self.weapon_rack = WeaponRack(
                width=self.spaceship_size[0],
                height=self.spaceship_size[1],
                pivot=(self.spaceship_size[0] / 2, self.spaceship_size[1] / 2),
                points_by_level=copy.copy(self.all_level_rack_positions),
                )

    @property
    def current_weapon_select(self) -> str:
        return self._current_weapon_select

    @current_weapon_select.setter
    def current_weapon_select(self, value) -> None:
        self._current_weapon_select = value
        self.parent.attack_distance_raw = self.get_current_value("range")

        if value != "":
            # check if weapon exists
            if not value in self.weapons.keys():
                self.parent.image_raw = self.no_weapon_image
                return

            # set new points for the rack
            self.weapon_rack.set_points(self.all_level_rack_positions[self.current_weapon.get("level")])

            # reset the image for correct drawing
            self.parent.image_raw = self.no_weapon_image

            # get the image
            self.weapon_image = get_image(f"{self.parent.name}_{self.current_weapon['name']}_{self.current_weapon['level']}.png")

            # set image to the ship
            self.parent.image_raw = self.weapon_image

            # set new orbit radius
            self.parent.desired_orbit_radius_raw = self.get_current_value("range") - 10
            self.parent.attack_distance_raw = self.get_current_value("range")

    def update_gun_positions(self):
        self.weapon_rack.update(
                x=self.parent.rect.centerx,
                y=self.parent.rect.centery,
                width=self.parent.screen_width,
                height=self.parent.screen_height,
                pivot=self.parent.rect.center,
                angle=self.parent.angle,
                scale=pan_zoom_handler.zoom
                )

        # self.weapon_rack.draw(self.parent.win)

    def setup_interval_timers(self):
        for i in self.all_weapons.keys():
            setattr(self, f"{i}_last_shoot", time_handler.time)

    def laser(self, defender, power, shoot_interval):
        """
        Shoots a laser
        :param defender: defender object
        :param power: laser power
        :param shoot_interval: laser interval
        """
        actual_time = time_handler.time
        if actual_time - self.laser_last_shoot > 1 / shoot_interval:
            self.laser_last_shoot = actual_time

            r0 = random.randint(-4, 5)
            r = random.randint(-3, 4)
            start_pos = random.choice(self.weapon_rack.points)
            end_pos = (defender.rect.centerx + r0, defender.rect.centery + r0)

            defender.energy -= power

            # shoot laser
            if defender.energy > 0:
                pygame.draw.line(surface=self.parent.win, start_pos=start_pos, end_pos=end_pos,
                        color=pygame.color.THECOLORS["white"], width=2)

                self.draw_moving_image(defender, power)
                sounds.play_sound(sounds.laser)

    def phaser(self, defender, power, shoot_interval):
        actual_time = time_handler.time
        if actual_time - self.phaser_last_shoot > 1 / shoot_interval:
            self.phaser_last_shoot = actual_time
            self.draw_moving_image(defender, power)
            config.app.player.stock["energy"] -= self.current_weapon.get("energy_consumtion", 1)
            color = random.choice(list(pygame.color.THECOLORS.keys()))

            r0 = random.randint(-4, 5)
            start_pos = random.choice(self.weapon_rack.points)
            end_pos = (defender.rect.centerx + r0, defender.rect.centery + r0)

            # draw_zigzag_line(
            #         surface=self.parent.win,
            #         color=color,
            #         start_pos=start_pos,
            #         end_pos=end_pos,
            #         num_segments=24)

            draw_segmented_beam(
                    surface=self.parent.win,
                    color=color,
                    start_pos=start_pos,
                    end_pos=end_pos,
                    num_lines=1,
                    segments_per_line=24,
                    spreading=20 * pan_zoom_handler.zoom)

            sounds.play_sound(sounds.laser)
            sounds.play_sound(sounds.electricity2)
            defender.energy -= power

    def rocket(self, defender, power, shoot_interval):
        actual_time = time_handler.time
        if actual_time - self.phaser_last_shoot > 1 / shoot_interval:
            self.phaser_last_shoot = actual_time
            x, y = pan_zoom_handler.screen_2_world(self.parent.rect.centerx, self.parent.rect.centery)
            rx = int(self.parent.rect.width / 4)
            ry = int(self.parent.rect.height / 4)
            x += random.randint(-rx, rx)
            y += random.randint(-ry, ry)
            power = self.get_current_value("power")
            defender.energy -= power

            # if defender.property in ["ship", "ufo"]:
            if defender.energy >= 0:
                x_, y_ = random.choice(self.weapon_rack.points)
                x, y = pan_zoom_handler.screen_2_world(x_, y_)
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
                        rotation_angle=self.parent.angle + 90,
                        movement_speed=random.randint(2, 10),
                        world_rect=universe_factory.world_rect,
                        target=defender,
                        missile_power=power,
                        friction=random.uniform(0.95, 0.99),
                        explosion_relative_gif_size=random.uniform(1.0, 1.5), )

    def draw_moving_image(self, defender, power):
        MovingImage(
                self.parent.win,
                defender.rect.top,
                defender.rect.right,
                18,
                18,
                get_image("energy_25x25.png"),
                1,
                (random.randint(-1, 1), 2),
                f"-{power}", pygame.color.THECOLORS["red"],
                "georgiaproblack", 1, defender.rect, target=None)

    def get_current_value(self, var):
        level = self.current_weapon.get("level")
        upgrade_value = self.current_weapon["upgrade values"][f"level_{level}"][var]
        weapon_value = self.current_weapon.get(var)
        value = weapon_value * upgrade_value
        return value

    def draw_attack_distance(self):
        # draw_transparent_circle(self.parent.win, self.parent.frame_color, self.parent.rect.center, self.get_current_value("range") * pan_zoom_handler.zoom, 20)
        draw_transparent_circle(self.parent.win, self.parent.player_color, self.parent.rect.center, self.get_current_value("range") * pan_zoom_handler.zoom, 20)

    def attack(self, defender):
        # if not level_of_detail.inside_screen(self.parent.get_screen_position()):
        #     return
        self.parent.state_engine.set_state("attacking")
        # activate weapons
        power = None
        if self.current_weapon["name"] in self.weapons.keys():
            power = self.get_current_value("power")
            shoot_interval = self.get_current_value("shoot_interval")

            # here the attack function should be called
            getattr(self, self.current_weapon["name"])(defender, power, shoot_interval)

        if defender.property in ["ship", "ufo"]:
            # self.parent.orbit_object = None
            # rotate_image_to(self.parent, defender.rect.center, self.parent.rotate_correction_angle)
            # make enemy attack you
            if defender.energy <= defender.energy_max / 2:
                defender.target = self.parent

            # kill enemy
            if defender.energy <= 0:
                # explode
                defender.end_object()
                self.parent.enemy = None

        if defender.property == "planet" and power:
            attack_planet(self.parent, defender, power)


# why is this outside the class??
def attack_planet(attacker, defender, power):
    if defender.economy_agent.population > 0:
        defender.economy_agent.population -= power / 100
    else:
        defender.owner = attacker.owner
        defender.get_explored(attacker.owner)
        defender.set_display_color()
        attacker.enemy = None

        attacker.orbit_object = defender


def attack(attacker, defender):
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

        # make damage to target
        defender.energy -= gun_power
        sounds.play_sound(sounds.laser)

    if defender.energy <= defender.energy_max / 2:
        defender.target = attacker


def launch_missile(attacker, defender):
    app = config.app
    screen = app.win
    x, y = pan_zoom_handler.screen_2_world(attacker.rect.centerx, attacker.rect.centery)
    # rx = int(attacker.rect.width / 4)
    # ry = int(attacker.rect.height / 4)
    # x += random.randint(-rx, rx)
    # y += random.randint(-ry, ry)

    if defender.energy - MISSILE_POWER >= 0:
        missile = PanZoomMissile(
                screen,
                x,
                y,
                42,
                17,
                pan_zoom_handler,
                "missile_42x17.gif",
                group="missiles",
                loop_gif=True,
                move_to_target=True,
                align_image="topleft",
                explosion_relative_gif_size=1.0,
                layer=9,
                debug=False,
                target=defender,
                appear_at_start=True, zoomable=True)
