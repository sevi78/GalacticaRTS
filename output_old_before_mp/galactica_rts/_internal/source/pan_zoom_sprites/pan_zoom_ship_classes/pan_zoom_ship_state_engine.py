from source.configuration.game_config import config
from source.draw.cross import draw_dashed_cross_in_circle
from source.gui.widgets.image_widget import ImageSprite
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.multimedia_library.images import get_image

STATE_IMAGE_SPACING = 35
STATE_IMAGE_SIZE = 17
ARC_SIZE = 50
CROSS_RADIUS = 24
DASH_LENGHT = 6


class PanZoomShipStateEngine:
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.image_drawer = PanZoomShipStateEngineDraw(self.parent, self)
        self.state = "sleeping"

    def __del__(self) -> None:
        """ seems to be unused, state and rank image are getting deleted somehow :)"""
        if hasattr(self, "image_drawer"):
            return
            self.image_drawer.state_image.kill()
            self.image_drawer.rank_image.kill()

    def set_state(self) -> None:

        if self.parent.move_stop > 0:
            self.state = "move_stop"

        if self.parent.moving:
            self.state = "moving"

        if self.parent.following_path:
            self.state = "following_path"

        if self.parent.orbiting:
            self.state = "orbiting"
        else:
            if hasattr(self.parent, "autopilot"):
                if self.parent.autopilot:
                    self.state = "autopilot"
            else:
                self.state = "sleeping"

        self.image_drawer.set_state_image()

    def update(self) -> None:
        if config.cross_view_start < pan_zoom_handler.zoom:
            self.image_drawer.show()
            self.image_drawer.draw_rank_image()
            self.image_drawer.draw_state_image()
        else:
            self.image_drawer.hide()
            draw_dashed_cross_in_circle(self.parent.win, self.parent.frame_color, self.parent.get_screen_position(), config.ui_cross_size, config.ui_cross_thickness, config.ui_cross_dash_length / 2)


class PanZoomShipStateEngineDraw:
    def __init__(self, parent: object, engine: PanZoomShipStateEngine):
        self.parent = parent  # the ship
        self.win = self.parent.win
        self.engine = engine  # the engine that holds the states

        # set up images
        x, y = self.parent.get_screen_position()
        self.state_images = {
            "move_stop": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("noenergy_25x25.png"), parent=self.parent),
            "following_path": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("follow_path_icon.png"), parent=self.parent),
            "moving": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE - 5, STATE_IMAGE_SIZE - 5, get_image("moving.png"), parent=self.parent),
            "sleeping": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("sleep.png"), parent=self.parent),
            "orbiting": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("orbit_icon.png"), parent=self.parent),
            "autopilot": ImageSprite(self.parent.win, x, y, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("autopilot.png"), parent=self.parent)
            }

        # very bloody hack to ensure the rank image is not drawn at initial position, no idea why this its there
        self.rank_image = ImageSprite(self.parent.win, -200, -200, 25, 25, get_image("warning_icon.png"), parent=self.parent)
        self.state_image = ImageSprite(self.parent.win, -200, -200, STATE_IMAGE_SIZE, STATE_IMAGE_SIZE, get_image("sleep.png"), parent=self.parent)

        self.hide()

    def show(self):
        self.state_image.show()
        self.rank_image.show()

    def hide(self):
        self.state_image.hide()
        self.rank_image.hide()

    def set_state_image(self):
        for key, value in self.state_images.items():
            if key == self.engine.state:
                self.state_image = value

    def draw_rank_image(self) -> None:
        # set image
        if not self.rank_image.image == self.parent.ranking.rank_images[self.parent.rank]:
            self.rank_image.set_image(self.parent.ranking.rank_images[self.parent.rank])

        # calculate position
        rank_image_pos = (self.parent.rect.x + self.parent.get_screen_width() / 2 / self.parent.get_zoom(),
                          self.parent.rect.y - self.parent.get_screen_height() / 2 / self.parent.get_zoom())

        # set position
        self.rank_image.set_position(rank_image_pos[0], rank_image_pos[1], "topright")

        # draw
        self.rank_image.draw()

    def draw_state_image(self) -> None:
        # calculate position
        state_image_position = self.rank_image.rect.x + STATE_IMAGE_SPACING, self.rank_image.rect.y

        # set position
        self.state_image.set_position(
                state_image_position[0], state_image_position[1] - STATE_IMAGE_SIZE / 2, "topright")

        # draw
        self.state_image.draw()
