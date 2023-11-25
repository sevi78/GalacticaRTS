import pygame
from pygame_widgets import Mouse
from pygame_widgets.mouse import MouseState

from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
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

        self.image_check = pygame.transform.scale(
            get_image("check.png"), (BUTTON_SIZE * .7, BUTTON_SIZE * .7))
        self.image_uncheck = pygame.transform.scale(
            get_image("uncheck.png"), (BUTTON_SIZE, BUTTON_SIZE))

        if self.image_name:
            self.image = pygame.transform.scale(get_image(self.image_name), (BUTTON_SIZE, BUTTON_SIZE))

        if not self.image:
            try:
                self.image = pygame.transform.scale(
                    images[pictures_path]["resources"][self.key + "_25x25.png"], (BUTTON_SIZE, BUTTON_SIZE))
            except KeyError:
                try:
                    self.image = pygame.transform.scale(
                        get_image(self.key + ".png"), (BUTTON_SIZE, BUTTON_SIZE))
                except KeyError:
                    self.image = pygame.transform.scale(
                        get_image("no_icon.png"), (BUTTON_SIZE, BUTTON_SIZE))

        self.image_raw = self.image
        self.rect = self.image.get_rect()

        self.tooltip = kwargs.get("tooltip")

        self.checked = True

        self.hide()

    def draw_frame(self):
        # Drawing Rectangle
        pygame.draw.rect(self.win, self.color, pygame.Rect(
            self.world_x, self.world_y, BUTTON_SIZE, BUTTON_SIZE), FRAME_THICKNESS, border_radius=BORDER_RADIUS)

    def draw_image(self):
        if self.checked:
            rect = self.image_check.get_rect()
            rect.x, rect.y = self.world_x + self.image.get_rect().width / 5, self.world_y
            self.win.blit(self.image_check, rect)

        else:
            rect = self.image_check.get_rect()
            rect.x, rect.y = self.world_x, self.world_y
            self.win.blit(self.image_uncheck, rect)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_image()
            global_params.app.tooltip_instance.reset_tooltip(self)

            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.rect.collidepoint(x, y):  # checks if mouse over ??
                if mouseState == MouseState.CLICK:
                    if self.checked:
                        self.checked = False
                    else:
                        self.checked = True

                    # selector_callback to parent
                    self.parent.get_checkbox_values()

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    if self.tooltip != "":
                        global_params.tooltip_text = self.tooltip

    def update(self, value):
        self.checked = value
