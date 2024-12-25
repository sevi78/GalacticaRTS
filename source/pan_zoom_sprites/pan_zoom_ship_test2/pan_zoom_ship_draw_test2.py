import pygame
from pygame import Vector2


from source.configuration.game_config import config
from source.debug.function_disabler import disabler, auto_disable
from source.draw.arrow import draw_arrows_on_line_from_start_to_end
from source.factories.universe_factory import universe_factory
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.math.line_intersect import interectLineCircle
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_classes import PanZoomGif
from source.pan_zoom_sprites.rot_rect import RotRect
from source.player.player_handler import player_handler


#
# disabled_functions = ["draw_connections", "draw_selection"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable
class PanZoomShipDraw:
    def __init__(self, parent):

        self.parent = parent
        self._disabled = False
        self.frame_color = colors.frame_color
        self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.parent.owner))

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.parent.win,
                x=self.parent.rect.x,
                y=self.parent.rect.y + self.parent.rect.y + self.parent.rect.height / 5,
                width=self.parent.rect.width,
                height=5,
                progress=lambda: 1 / self.parent.energy_max * self.parent.energy,
                curved=True,
                completed_color=self.frame_color,
                layer=self.parent.layer,
                parent=self
                )

        # electro_discharge, used for energy reloading
        x, y = pan_zoom_handler.screen_2_world(self.parent.rect.centerx, self.parent.rect.centery)
        self.electro_discharge = PanZoomGif(
                win=self.parent.win,  # type: ignore
                world_x=x,
                world_y=y,
                world_width=114,
                world_height=64,
                layer=self.parent.layer,  # type: ignore
                group=sprite_groups.ships2,
                gif_name="electro_discharge_croped.gif",
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
        self.rot_rect = RotRect(self.parent.rect_raw)
        self.rot_rect.add_point(Vector2(self.rot_rect.midtop.x, self.rot_rect.midtop.y - 200), "aim_point")

    def update_electro_discharge(self):
        return
        if not self.parent.energy_reloader:
            self.electro_discharge.visible = False
            return

        self.rot_rect.update(
                x=self.parent.rect.centerx,
                y=self.parent.rect.centery,
                width=self.parent.world_width * pan_zoom_handler.zoom,
                height=self.parent.world_height * pan_zoom_handler.zoom,
                pivot=Vector2(self.parent.rect.center),
                angle=self.parent.angle,
                scale=pan_zoom_handler.zoom
                )
        # self.rot_rect.draw(self.win)

        # check intersection
        cpt = self.parent.energy_reloader.rect.center  # centerpoint
        radius = self.parent.energy_reloader.rect.width / 2
        intersection = interectLineCircle(self.parent.rect.center, self.rot_rect.aim_point, cpt, radius)
        # draw_intersection(self.win, cpt, intersection, self.rect.center, self.rot_rect.aim_point, radius)

        # Update electro discharge visibility
        if (self.target_reached and len(intersection) == 2):
            self.electro_discharge.visible = True

            # Update electro discharge position and rotation
            x, y = pan_zoom_handler.screen_2_world(self.rot_rect.midtop[0], self.rot_rect.midtop[1])
            self.electro_discharge.set_rotation_angle(self.angle + 90)
            self.electro_discharge.set_position(x, y)

    def draw_selection(self):
        """ this handles how the ship is displayed on screen:
            as a circle either in player color or in self.frame_color based on config.show_player_colors == True/False
        """
        # only draw selections of the local user
        # client_id = config.app.game_client.id
        # if not self.parent.owner == client_id:
        #     return

        if not self.parent.state_engine.state == "waiting for order":
            return
        # get the coler to display
        color = self.player_color if config.show_player_colors else self.frame_color

        # draw it
        # pygame.draw.circle(self.parent.win, color, self.parent.rect.center, self.parent.rect.width, int(6 * pan_zoom_handler.get_zoom()))

        pygame.draw.circle(self.parent.win, color, self.parent.rect.center,self.parent.scaled_rect.width/2, int(6 * pan_zoom_handler.get_zoom()))

    def draw_connections(self, target):
        """
        this calls draw_arrows_on_line_from_start_to_end
        """
        # client_id = config.app.game_client.id
        # if not self.parent.owner == client_id:
        #     return
        if self.parent.state_engine.state == "moving":
            draw_arrows_on_line_from_start_to_end(
                    surf=self.parent.win,
                    color=colors.ui_darker,
                    start_pos=self.parent.rect.center,
                    end_pos=target.rect.center,
                    width=1,
                    dash_length=30,
                    arrow_size=(0, 6),
                    )

    def update(self):
        # update the progress bar
        self.progress_bar.set_position((self.parent.scaled_rect.x, self.parent.scaled_rect.bottom + 15))
        self.progress_bar.set_screen_width(self.parent.scaled_rect.width)

