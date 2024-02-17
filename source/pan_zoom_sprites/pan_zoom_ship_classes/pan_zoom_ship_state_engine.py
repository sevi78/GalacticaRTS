import pygame

from source.gui.widgets.image_widget import ImageSprite
from source.multimedia_library.images import get_image

STATE_IMAGE_SPACING = 35

STATE_IMAGE_SIZE = 17


class PanZoomShipStateEngine:
    def __init__(self, parent: object) -> None:
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
        self.rank_image = ImageSprite(-200, -200, 25, 25, get_image("warning_icon.png"), "state_images", parent=self)

        # set up image
        x, y = self.parent.get_screen_position()

        self.state_image = ImageSprite(x, y,
            STATE_IMAGE_SIZE,
            STATE_IMAGE_SIZE, get_image("sleep.png"), "state_images")

    def __del__(self) -> None:
        self.state_image.kill()
        self.rank_image.kill()

    def set_state(self) -> None:
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

    def draw_rank_image(self) -> None:
        # set image
        if not self.rank_image.image == self.parent.ranking.rank_images[self.parent.rank]:
            self.rank_image.set_image(self.parent.ranking.rank_images[self.parent.rank])

        # calculate position
        rank_image_pos = (self.parent.rect.x + self.parent.get_screen_width() / 2 / self.parent.get_zoom(),
                          self.parent.rect.y - self.parent.get_screen_height() / 2 / self.parent.get_zoom())

        # set position
        self.rank_image.set_position(rank_image_pos[0], rank_image_pos[1], "topright")

    def draw_state_image(self) -> None:
        state_image_position = self.rank_image.rect.x + STATE_IMAGE_SPACING, self.rank_image.rect.y
        self.state_image.set_position(
            state_image_position[0], state_image_position[1] - STATE_IMAGE_SIZE / 2, "topright")

    def update(self) -> None:
        self.draw_rank_image()
        self.draw_state_image()
        # self._hidden = self.parent._hidden
