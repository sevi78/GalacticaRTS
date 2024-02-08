import pygame

from source.gui.widgets.image_widget import ImageSprite
from source.multimedia_library.images import get_image

STATE_IMAGE_SIZE = 27


class PanZoomShipStateEngine:
    def __init__(self, parent):
        # pre-load images
        self.parent = parent
        self.noenergy_image = get_image("noenergy_25x25.png")
        self.moving_image = pygame.transform.scale(get_image("moving.png"), (
            STATE_IMAGE_SIZE - 5, STATE_IMAGE_SIZE - 5))
        self.sleep_image = pygame.transform.scale(get_image("sleep.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))
        self.sleep_image.set_alpha(130)
        self.orbit_image = pygame.transform.scale(get_image("orbit_icon.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))
        self.autopilot_image = pygame.transform.scale(get_image("autopilot.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))

        # very bloody hack to ensure the rank imageis not drawn at initial position, no idea why this its there
        self.rank_image = ImageSprite(-200, -200, 30, 30, get_image("warning_icon.png"), "moving_images", parent=self)

        # set up image
        x, y = self.parent.get_screen_position()

        self.state_image = ImageSprite(x, y,
            STATE_IMAGE_SIZE,
            STATE_IMAGE_SIZE, get_image("sleep.png"), "moving_images")

    def __del__(self):
        self.state_image.kill()
        self.rank_image.kill()

    def set_state(self):
        if self.parent.move_stop > 0:
            self.state_image.set_image(self.noenergy_image)
            self.state_image.image.set_alpha(255)

        if self.parent.moving:
            self.state_image.set_image(self.moving_image)
            self.state_image.image.set_alpha(255)

        elif self.parent.orbiting:
            self.state_image.set_image(self.orbit_image)
            self.state_image.image.set_alpha(255)

        # elif self.parent.autopilot:
        #     self.image.setImage(self.autopilot_image)

        else:
            self.state_image.set_image(self.sleep_image)
            self.state_image.image.set_alpha(130)

    def draw_rank_image(self):
        rank_image_pos = (self.parent.rect.centerx + self.parent.get_screen_width() / 2 / self.parent.get_zoom(),
                          self.parent.rect.centery - self.parent.get_screen_height() / 2 / self.parent.get_zoom())

        self.rank_image.set_image(self.parent.ranking.rank_images[self.parent.rank])
        self.rank_image.set_position(rank_image_pos[0], rank_image_pos[1], "center")

    def update(self):
        self.draw_rank_image()
        self.state_image.set_position(
            self.parent.get_screen_position()[0], self.parent.get_screen_position()[1], "topleft")
        # self._hidden = self.parent._hidden
