import copy

import pygame

from source.configuration.game_config import config
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.multimedia_library.images import images, pictures_path, get_image

BUTTON_SIZE = 30
FRAME_THICKNESS = 2
BORDER_RADIUS = 5


class Checkbox(ImageButton):
    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        ImageButton.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)

        self.name = kwargs.get("name")
        self.parent = kwargs.get("parent")
        self.win = win
        self.layer = kwargs.get("layer", 9)
        self.key = kwargs.get("key")
        self.color = kwargs.get("color")
        self.image_name = kwargs.get("image_name", None)
        self.button_size = kwargs.get("button_size", BUTTON_SIZE)

        self.image_check = pygame.transform.scale(
                get_image("check.png"), (self.button_size * .7, self.button_size * .7))
        self.image_uncheck = pygame.transform.scale(
                get_image("uncheck.png"), (self.button_size, self.button_size))

        if self.image_name:
            self.image = pygame.transform.scale(get_image(self.image_name), (self.button_size, self.button_size))

        if not self.image:
            try:
                self.image = pygame.transform.scale(
                        get_image(self.key + "_25x25.png"), (self.button_size, self.button_size))
            except KeyError:
                try:
                    self.image = pygame.transform.scale(
                            get_image(self.key + ".png"), (self.button_size, self.button_size))
                except KeyError:
                    self.image = pygame.transform.scale(
                            get_image("no_icon.png"), (self.button_size, self.button_size))

        self.image_raw = copy.copy(self.image)
        self.rect = self.image.get_rect()
        self.tooltip = kwargs.get("tooltip")
        self.checked = True

        self.hide()

    def draw_frame(self):
        # Drawing Rectangle
        pygame.draw.rect(self.win, self.color, pygame.Rect(
                self.world_x, self.world_y, self.button_size, self.button_size), FRAME_THICKNESS, border_radius=BORDER_RADIUS)

    def draw_image(self):
        rect = self.image_check.get_rect()
        if self.checked:
            rect.x, rect.y = self.world_x + self.image.get_rect().width / 5, self.world_y
            self.win.blit(self.image_check, rect)
        else:
            rect.x, rect.y = self.world_x, self.world_y
            self.win.blit(self.image_uncheck, rect)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_image()
            config.app.tooltip_instance.reset_tooltip(self)

            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.rect.collidepoint(x, y):  # checks if mouse over ??
                if mouse_state == MouseState.LEFT_CLICK:
                    if self.checked:
                        self.checked = False
                    else:
                        self.checked = True

                    # selector_callback to parent
                    self.parent.get_checkbox_values(checkbox=self, value=self.checked)

                elif mouse_state == MouseState.HOVER or mouse_state == MouseState.LEFT_DRAG:
                    if self.tooltip != "":
                        config.tooltip_text = self.tooltip

    def update(self, value):
        self.checked = value
