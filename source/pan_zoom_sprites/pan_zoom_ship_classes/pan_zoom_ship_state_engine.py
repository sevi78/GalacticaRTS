import pygame

from source.configuration.game_config import config
from source.debug.function_disabler import disabler, auto_disable
from source.draw.cross import draw_dashed_cross_in_circle
from source.gui.widgets.image_widget import ImageSprite
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image

STATE_IMAGE_SPACING = 35
STATE_IMAGE_SIZE = 17
ARC_SIZE = 50
CROSS_RADIUS = 24
DASH_LENGHT = 6

# disabled_functions = ["listen"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable

class PanZoomShipStateEngine:
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.image_drawer = PanZoomShipStateEngineDraw(self.parent, self)
        self.state = "sleeping"

    def end_object(self):
        self.image_drawer.end_object()

    def set_state(self, state) -> None:
        self.state = state
        self.parent.state = self.state
        self.image_drawer.set_state_image()

    def listen(self, events):
        pass

    def update(self) -> None:
        if not config.show_ship_state:
            self.image_drawer.hide()
            return


        if config.cross_view_start < pan_zoom_handler.zoom:
            self.image_drawer.show()
            self.image_drawer.update_rank_image()
            self.image_drawer.update_state_image()
        else:
            self.image_drawer.hide()
            draw_dashed_cross_in_circle(self.parent.win, self.parent.frame_color, self.parent.get_screen_position(), config.ui_cross_size, config.ui_cross_thickness, config.ui_cross_dash_length / 2)





# disabled_functions = ["set_state_image", "update_rank_image", "update_state_image"]
# for i in disabled_functions:
#     disabler.disable(i)

class PanZoomShipStateEngineDraw:
    def __init__(self, parent: object, engine: PanZoomShipStateEngine):
        self.parent = parent  # the ship
        self.win = self.parent.win
        self.engine = engine  # the engine that holds the states

        # set up images
        x, y = self.parent.get_screen_position()

        # this is still needed for the containers, ugly ---
        self.state_image_names = {
            "move_stop": "noenergy_25x25.png",
            "following_path": "follow_path_icon.png",
            "moving": "moving.png",
            "sleeping": "sleep.png",
            "orbiting": "orbit_icon.png",
            "autopilot": "autopilot.png",
            "attacking": "war_icon.png",
            "waiting for order": "question_mark.png"
            }

        self.state_images = {
            "move_stop": pygame.transform.scale(get_image("noenergy_25x25.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "following_path": pygame.transform.scale(get_image("follow_path_icon.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "moving": pygame.transform.scale(get_image("moving.png"), (STATE_IMAGE_SIZE - 5, STATE_IMAGE_SIZE - 5)),
            "sleeping": pygame.transform.scale(get_image("sleep.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "orbiting": pygame.transform.scale(get_image("orbit_icon.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "autopilot": pygame.transform.scale(get_image("autopilot.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "attacking": pygame.transform.scale(get_image("war_icon.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE)),
            "waiting for order": pygame.transform.scale(get_image("question_mark.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))
            }

        self.rank_image = ImageSprite(self.parent.win, -200, -200, 25, 25, get_image("warning_icon.png"), parent=self.parent)
        self.state_image = ImageSprite(self.parent.win, -200, -200, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("sleep.png"), parent=self.parent)

        self.hide()

    def end_object(self):
        self.rank_image.end_object()
        self.state_image.end_object()

    def show(self):
        self.state_image.show()
        self.rank_image.show()

    def hide(self):
        self.state_image.hide()
        self.rank_image.hide()

    def set_state_image(self):
        self.state_image.set_image(self.state_images[self.engine.state])

    def update_rank_image(self) -> None:
        # set image
        if not self.rank_image.image == self.parent.ranking.rank_images[self.parent.rank]:
            self.rank_image.set_image(self.parent.ranking.rank_images[self.parent.rank])

        # calculate position
        rank_image_pos = (self.parent.rect.x + self.parent.get_screen_width() / 2 / pan_zoom_handler.get_zoom(),
                          self.parent.rect.y - self.parent.get_screen_height() / 2 / pan_zoom_handler.get_zoom())

        # set position
        self.rank_image.set_position(rank_image_pos[0], rank_image_pos[1], "topright")

    def update_state_image(self) -> None:
        # calculate position
        state_image_position = self.rank_image.rect.x + STATE_IMAGE_SPACING, self.rank_image.rect.y

        # set position
        self.state_image.set_position(
                state_image_position[0], state_image_position[1] - STATE_IMAGE_SIZE / 2, "topright")
