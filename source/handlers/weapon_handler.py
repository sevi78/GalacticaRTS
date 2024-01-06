import copy
import random
import time

import pygame

from source.draw.circles import draw_transparent_circle
from source.draw.zigzag_line import draw_zigzag_line
from source.factories.weapon_factory import weapon_factory
from source.gui.lod import inside_screen
from source.gui.widgets.moving_image import MovingImage
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_missile import PanZoomMissile, MISSILE_POWER
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.configuration import global_params

CANNON_GUNPOWER = 3
class WeaponHandler:
    def __init__(self, parent, current_weapon):
        self.parent = parent
        self.all_weapons = copy.deepcopy(weapon_factory.get_all_weapons())
        self.weapons = {}
        self.current_weapon = self.all_weapons[current_weapon]
        self.current_weapon_select = ""
        self.setup_interval_timers()


    def setup_interval_timers(self):
        for i in self.all_weapons.keys():
            setattr(self, f"{i}_last_shoot", time.time())

    def laser(self, defender, power, shoot_interval):
        actual_time = time.time()
        if actual_time - self.laser_last_shoot > 1 / shoot_interval:
            self.laser_last_shoot = actual_time

            r0 = random.randint(-4, 5)
            r = random.randint(-3, 4)
            startpos = (self.parent.rect.centerx, self.parent.rect.centery)
            endpos = (defender.rect.centerx + r0, defender.rect.centery + r0)
            defender.energy -= power

            # shoot laser
            if defender.energy > 0:
                pygame.draw.line(surface=self.parent.win, start_pos=startpos, end_pos=endpos,
                    color=pygame.color.THECOLORS["white"], width=2)

                self.draw_moving_image(defender, power)
                sounds.play_sound(sounds.laser)

    def phaser(self, defender, power, shoot_interval):
        actual_time = time.time()
        if actual_time - self.phaser_last_shoot > 1 / shoot_interval:
            self.phaser_last_shoot = actual_time
            self.draw_moving_image(defender, power)
            global_params.app.player.energy -= self.current_weapon.get("energy_consumtion", 1)
            color = random.choice(list(pygame.color.THECOLORS.keys()))
            draw_zigzag_line(
                surface=self.parent.win,
                color=color,
                start_pos=self.parent.rect.center,
                end_pos=defender.rect.center,
                num_segments=24)
            sounds.play_sound(sounds.laser)
            sounds.play_sound(sounds.electricity2)
            defender.energy -= power

    def rocket(self, defender, power, shoot_interval):
        actual_time = time.time()
        if actual_time - self.phaser_last_shoot > 1 / shoot_interval:
            self.phaser_last_shoot = actual_time
            app = global_params.app
            screen = app.win
            x, y = pan_zoom_handler.screen_2_world(self.parent.rect.centerx, self.parent.rect.centery)
            rx = int(self.parent.rect.width / 4)
            ry = int(self.parent.rect.height / 4)
            x += random.randint(-rx, rx)
            y += random.randint(-ry, ry)
            power = self.get_current_value("power")

            if defender.energy >= 0:
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
                    target=defender, missile_power=power)
                    # missile.set_target(defender)


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
            "georgiaproblack", 1, defender, target=None)

    def get_current_value(self, var):
        level = self.current_weapon.get("level")
        upgrade_value = self.current_weapon["upgrade values"][f"level_{level}"][var]
        weapon_value = self.current_weapon.get(var)
        value = weapon_value * upgrade_value
        return value



    def attack(self, defender):
        if not inside_screen(self.parent.get_screen_position()):
            return

        # activate weapon
        if self.current_weapon["name"] in self.weapons.keys():
            power = self.get_current_value("power")
            shoot_interval = self.get_current_value("shoot_interval")
            getattr(self, self.current_weapon["name"])(defender, power, shoot_interval)

        # make enemy attack you
        if defender.energy <= defender.energy_max / 2:
            defender.target = self.parent

        # kill enemy
        if defender.energy <= 0:
            # explode
            defender.end_object()
            self.parent.enemy = None

    def draw_attack_distance(self):
        draw_transparent_circle(self.parent.win, self.parent.frame_color, self.parent.rect.center, self.get_current_value("range"), 20)





def launch_missile(attacker, defender):
    app = global_params.app
    screen = app.win
    x, y = pan_zoom_handler.screen_2_world(attacker.rect.centerx, attacker.rect.centery)
    rx = int(attacker.rect.width / 4)
    ry = int(attacker.rect.height / 4)
    x += random.randint(-rx, rx)
    y += random.randint(-ry, ry)

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
            target=defender)
        # missile.set_target(defender)
def attack(attacker, defender):
    if not inside_screen(attacker.get_screen_position()):
        return

    # if attacker is planet
    if attacker.property == "planet":
        gun_power = len([i for i in attacker.buildings if i == "cannon"]) * CANNON_GUNPOWER
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