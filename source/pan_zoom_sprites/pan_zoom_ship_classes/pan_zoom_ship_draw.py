import math

import pygame
from pygame import Vector2

from source.configuration.game_config import config
# from source.debug.function_disabler import disabler, auto_disable
from source.draw.arrow import draw_arrows_on_line_from_start_to_end
from source.factories.universe_factory import universe_factory
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.math.line_intersect import interectLineCircle
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomGif
from source.pan_zoom_sprites.rot_rect import RotRect


#
# disabled_functions = ["draw_connections", "draw_selection"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable
class PanZoomShipDraw:
    def __init__(self, kwargs):
        self.frame_color = colors.frame_color

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
                x=self.get_screen_x(),
                y=self.get_screen_y() + self.get_screen_height() + self.get_screen_height() / 5,
                width=self.get_screen_width(),
                height=5,
                progress=lambda: 1 / self.energy_max * self.energy,
                curved=True,
                completed_color=self.frame_color,
                gradient_color=True,
                layer=self.layer,
                parent=self
                )

        # electro_discharge, used for energy reloading
        x, y = pan_zoom_handler.screen_2_world(self.rect.centerx, self.rect.centery)
        self.electro_discharge = PanZoomGif(
                win=self.win,  # type: ignore
                world_x=x,
                world_y=y,
                world_width=477,
                world_height=240,
                layer=self.layer,  # type: ignore
                group=sprite_groups.energy_reloader,
                gif_name="electro_discharge_big_transparent_crop.gif",
                gif_index=0,
                gif_animation_time=None,
                loop_gif=True,
                kill_after_gif_loop=False,
                image_alpha=None,
                rotation_angle=0,
                movement_speed=0,
                direction=Vector2(0, 0),
                world_rect=universe_factory.world_rect,
                align_image="center"
                )
        self.electro_discharge.visible = False

        # rot_rect used for several positions like lefttop, aim point ect
        self.rot_rect = RotRect(self.rect_raw)
        self.rot_rect.add_point(Vector2(self.rot_rect.midtop.x, self.rot_rect.midtop.y - 600), "aim_point")

    def update_electro_discharge(self):
        # Update electro discharge visibility: if no energy_reloader set invisible
        if not self.energy_reloader:
            self.electro_discharge.visible = False
            return

        # Update rot_rect to get the positions for electro discharge
        if self.weapon_handler.current_weapon_select == "rocket":
            angle = self.angle +90
        else:
            angle = self.angle

        self.rot_rect.update(
                x=self.rect.centerx,
                y=self.rect.centery,
                width=self.world_width * pan_zoom_handler.zoom,
                height=self.world_height * pan_zoom_handler.zoom,
                pivot=Vector2(self.rect.center),
                angle=angle,
                scale=pan_zoom_handler.zoom
                )

        # self.rot_rect.draw(self.win)

        # check intersection
        cpt = self.energy_reloader.rect.center  # centerpoint
        radius = self.energy_reloader.rect.width / 2
        intersection = interectLineCircle(self.rect.center, self.rot_rect.aim_point, cpt, radius)
        # draw_intersection(self.win, cpt, intersection, self.rect.center, self.rot_rect.aim_point, radius)

        # Update electro discharge visibility: if target reached and intersection is valid
        if self.target_reached and len(intersection) == 2 and self.reloading:
            self.electro_discharge.visible = True

            # Calculate the midpoint between aim_point and energy_reloader center
            aim_point = self.rot_rect.midtop
            reloader_center = self.energy_reloader.rect.center
            midpoint_x = (aim_point[0] + reloader_center[0]) / 2
            midpoint_y = (aim_point[1] + reloader_center[1]) / 2

            # Convert midpoint to world coordinates
            world_x, world_y = pan_zoom_handler.screen_2_world(midpoint_x, midpoint_y)

            # Update electro discharge position, rotation, and size
            self.electro_discharge.set_position(world_x, world_y)
            self.electro_discharge.set_rotation_angle(self.rot_rect.angle + 90)

            self.electro_discharge.world_width = math.dist(aim_point, reloader_center) / pan_zoom_handler.zoom
            self.electro_discharge.world_height = self.electro_discharge.world_width * self.electro_discharge.image_aspect_ratio
        else:
            # Set electro discharge visibility to False in any other case
            self.electro_discharge.visible = False

    def draw_selection(self):
        """ this handles how the ship is displayed on screen:
            as a circle either in player color or in self.frame_color based on config.show_player_colors == True/False
        """
        # only draw selections of the local user
        client_id = config.app.game_client.id
        if not self.owner == client_id:
            return

        # get the coler to display
        color = self.player_color if config.show_player_colors else self.frame_color

        # draw it
        pygame.draw.circle(self.win, color, self.rect.center, self.get_screen_width(), int(6 * pan_zoom_handler.get_zoom()))

    def draw_connections(self, target):
        """
        this calls draw_arrows_on_line_from_start_to_end
        """
        client_id = config.app.game_client.id
        if not self.owner == client_id:
            return

        draw_arrows_on_line_from_start_to_end(
                surf=self.win,
                color=colors.ui_darker,
                start_pos=self.rect.center,
                end_pos=target.rect.center,
                width=1,
                dash_length=30,
                arrow_size=(0, 4),
                )
