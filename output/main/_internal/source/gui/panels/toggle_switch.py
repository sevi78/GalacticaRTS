import pygame

from source.gui.widgets.buttons.image_button import ImageButton
from source.utils.colors import colors
from source.multimedia_library.images import get_image


class ToggleSwitch:
    def __init__(self, parent, toggle_size, **kwargs):
        self.parent = parent
        self.toggle_size = toggle_size
        self.layer = self.parent.layer
        self.zero_y = kwargs.get("zero_y", 0)
        self.frame_color = colors.frame_color
        self.create_icons()
        self.reposition()

    def create_icons(self):
        image = pygame.transform.scale(
            get_image("arrow-right.png"), (self.toggle_size, self.toggle_size))

        self.toggle_panel_icon = ImageButton(win=self.parent.win,
            x=self.parent.surface_rect.centerx - self.toggle_size / 2,
            y=self.parent.max_height,
            width=self.toggle_size,
            height=self.toggle_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.rotate(image, 90),
            tooltip=f"close {self.parent.name}",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.toggle_panel())

    def toggle_panel(self):
        if not self.parent._hidden:
            self.parent.hide()
            image = pygame.transform.scale(get_image("arrow-left.png"), (self.toggle_size, self.toggle_size))
            self.toggle_panel_icon.image = pygame.transform.rotate(image, 90)
            self.toggle_panel_icon.tooltip = f"open {self.parent.name}"

        else:
            image = pygame.transform.scale(
                get_image("arrow-right.png"), (self.toggle_size, self.toggle_size))
            self.toggle_panel_icon.image = pygame.transform.rotate(image, 90)
            self.toggle_panel_icon.tooltip = f"close {self.parent.name}"
            self.parent.show()

        self.parent.reposition()
        self.reposition()

    def reposition(self):
        if self.parent._hidden:
            self.toggle_panel_icon.screen_y = self.zero_y
        else:
            self.toggle_panel_icon.screen_y = self.parent.max_height
        self.toggle_panel_icon.screen_x = self.parent.surface_rect.centerx - self.toggle_panel_icon.get_screen_width() / 2
