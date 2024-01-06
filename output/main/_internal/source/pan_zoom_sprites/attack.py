import random

import pygame

from source.gui.lod import inside_screen
from source.pan_zoom_sprites.pan_zoom_missile import PanZoomMissile, MISSILE_POWER
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils import global_params

from source.multimedia_library.sounds import sounds

CANNON_GUNPOWER = 3


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
