import copy
import random

import pygame
from source.test.beam_test import draw_segmented_beam

from source.configuration.game_config import config
from source.draw.circles import draw_transparent_circle
from source.factories.building_factory import building_factory
from source.factories.universe_factory import universe_factory
from source.gui.event_text import event_text
from source.gui.widgets.moving_image import MovingImage
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_missile import Missile
from source.weapons.weapon_factory import weapon_factory
from source.weapons.weapon_rack import WeaponRack, calculate_weapon_positions


class WeaponHandler:  # upgrade weapon fixed
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

        # calculate the resize factor
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

    def update_weapon_state(self, selected_weapon) -> str:
        """ sets the state of the weapon handler:
        - returns the state of the weapon (upgrade or buy)
        - sets the current weapon
        - if not weapon in self.weapons, copies the weapon from self.all_weapons into self.weapons
        """

        self.current_weapon_select = selected_weapon

        if self.current_weapon_select in self.weapons.keys():
            self.current_weapon = copy.deepcopy(self.weapons[self.current_weapon_select])
            return "upgrade"
        else:
            self.current_weapon = copy.deepcopy(self.all_weapons[self.current_weapon_select])
            return "buy"

    def can_upgrade_weapon(self) -> bool:  # working , but not possible to upgrade 3 times at once
        """
        checks if the current weapon can be upgraded:
        - checks if the max level is reached
        - checks if there are upgrades in progress
        """
        max_level = self.max_weapons_upgrade_level
        current_level = self.current_weapon["level"]
        weapon_name = self.current_weapon["name"]

        # Count upgrades in progress
        in_progress = len([w for w in config.app.building_widget_list
                           if w.receiver == self.parent and w.name == weapon_name])

        # Check if upgrade is possible
        return current_level + in_progress < max_level

    def upgrade_weapon(self) -> bool:  # working , but not possible to upgrade 3 times at oncewwww
        """
        upgrades the current weapon
        - checks if the current weapon can be upgraded
        - builds the weapon
        - returns True if the upgrade was successful
        - returns False if the upgrade was not successful
        - sets the event text
        """
        if self.can_upgrade_weapon():
            weapon_name = self.current_weapon["name"]
            prices = building_factory.get_prices_from_weapons_dict(weapon_name, self.current_weapon["level"])
            building_factory.build(weapon_name, self.parent, prices=prices)

            return True
        else:
            event_text.set_text(f"Maximum upgrade level of {self.max_weapons_upgrade_level} reached!",
                    sender=config.app.game_client.id)
            return False

    def update_gun_positions(self) -> None:
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

    def setup_interval_timers(self) -> None:
        for i in self.all_weapons.keys():
            setattr(self, f"{i}_last_shoot", time_handler.time)

    def laser(self, defender, power, shoot_interval) -> None:
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

    def phaser(self, defender, power, shoot_interval) -> None:
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

    def rocket(self, defender, power, shoot_interval) -> None:
        actual_time = time_handler.time
        if actual_time - self.phaser_last_shoot > 1 / shoot_interval:
            self.phaser_last_shoot = actual_time
            x, y = pan_zoom_handler.screen_2_world(self.parent.rect.centerx, self.parent.rect.centery)
            rx = int(self.parent.rect.width / 4)
            ry = int(self.parent.rect.height / 4)
            x += random.randint(-rx, rx)
            y += random.randint(-ry, ry)
            # power = self.get_current_value("power")
            # defender.energy -= power

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

    def draw_moving_image(self, defender, power) -> None:
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

    def get_current_value(self, var: str) -> float:
        level = self.current_weapon.get("level")
        upgrade_value = self.current_weapon["upgrade values"][f"level_{level}"][var]
        weapon_value = self.current_weapon.get(var)
        value = weapon_value * upgrade_value
        return value

    def draw_attack_distance(self) -> None:
        # draw_transparent_circle(self.parent.win, self.parent.frame_color, self.parent.rect.center, self.get_current_value("range") * pan_zoom_handler.zoom, 20)
        draw_transparent_circle(self.parent.win, self.parent.player_color, self.parent.rect.center, self.get_current_value("range") * pan_zoom_handler.zoom, 20)

    def attack(self, defender) -> None:
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
            self.attack_planet(self.parent, defender, power)

    def attack_planet(self, attacker, defender, power) -> None:
        if defender.economy_agent.population > 0:
            defender.economy_agent.population -= power / 100
        else:
            defender.owner = attacker.owner
            defender.get_explored(attacker.owner)
            defender.set_display_color()
            attacker.enemy = None

            attacker.orbit_object = defender
