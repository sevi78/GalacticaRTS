import pygame

from source.configuration.game_config import config
from source.gui.widgets.buttons.button import Button
from source.multimedia_library.images import get_image


class BuildingPanelConstructor:
    def create_icons(self):
        self.image = get_image("clock.png")
        self.image_size = self.image.get_size()
        self.arrow_size = 15

        # planet selection buttons
        self.planet_minus_arrow_button = Button(win=self.win,
                x=self.get_screen_x() + self.spacing * 2,
                y=self.get_screen_y() + 40,
                width=self.image_size[0],
                height=self.image_size[1],
                is_sub_widget=False,
                image=pygame.transform.scale(
                        get_image("arrow-left.png"), (self.arrow_size, self.arrow_size)),
                tooltip="",
                frame_color=self.frame_color,
                transparent=True,
                on_click=lambda: config.app.set_planet_selection(-1),
                parent=self.parent, layer=self.layer
                )
        self.planet_plus_arrow_button = Button(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() - self.spacing * 2 - self.arrow_size,
                y=self.get_screen_y() + 40,
                width=self.image_size[0],
                height=self.image_size[1],
                is_sub_widget=False,
                image=pygame.transform.scale(
                        get_image("arrow-right.png"), (self.arrow_size, self.arrow_size)),
                tooltip="",
                frame_color=self.frame_color,
                transparent=True,
                on_click=lambda: config.app.set_planet_selection(1),
                parent=self.parent, layer=self.layer
                )
