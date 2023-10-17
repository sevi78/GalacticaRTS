import math

import pygame
from pygame import gfxdraw
from pygame_widgets.mouse import Mouse, MouseState

from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.widget_handler import update
from source.utils import global_params


class Slider(WidgetBase):
    """Main functionalities:
    The Slider class is a subclass of the WidgetBase class and represents a graphical slider widget that can be used to
    select a value within a given range. The slider can be either horizontal or vertical and can be curved or straight.
    The user can click and drag the handle of the slider to change the selected value. The slider also has customizable
    colors, border thickness, and handle radius.

    Methods:
    - __init__: initializes the Slider object with the given parameters and sets default values for optional parameters
    - listen: listens for mouse events and updates the selected value of the slider accordingly
    - draw: draws the slider on the screen with the current selected value and customizable colors and border thickness
    - contains: checks if the given coordinates are within the handle of the slider
    - round: rounds the given value to the nearest multiple of the step size
    - getValue: returns the current selected value of the slider
    - setValue: sets the current selected value of the slider to the given value

    Fields:
    - selected: a boolean indicating whether the handle of the slider is currently selected
    - min: the minimum value of the slider range
    - max: the maximum value of the slider range
    - step: the step size of the slider
    - colour: the color of the slider
    - handleColour: the color of the handle of the slider
    - borderThickness: the thickness of the border of the slider
    - borderColour: the color of the border of the slider
    - value: the current selected value of the slider
    - curved: a boolean indicating whether the slider is curved or straight
    - vertical: a boolean indicating whether the slider is vertical or horizontal
    - radius: the radius of the curved part of the slider
    - handleRadius: the radius of the handle of the slider
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)

        self.selected = False

        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 99)
        self.step = kwargs.get('step', 1)

        self.colour = kwargs.get('colour', (200, 200, 200))
        self.handleColour = kwargs.get('handleColour', (0, 0, 0))

        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))

        self.value = self.round(kwargs.get('initial', (self.max + self.min) / 2))
        # elf.value = max(min(self.value, self.max), self.min)

        self.curved = kwargs.get('curved', True)

        self.vertical = kwargs.get('vertical', False)

        if self.curved:
            if self.vertical:
                self.radius = self.screen_width // 2
            else:
                self.radius = self.screen_height // 2

        if self.vertical:
            self.handleRadius = kwargs.get('handleRadius', int(self.screen_width / 1.3))
        else:
            self.handleRadius = kwargs.get('handleRadius', int(self.screen_height / 1.3))

    # def listen(self, events):
    #     if not self._hidden and not self._disabled:
    #         mouseState = Mouse.getMouseState()
    #         x, y = Mouse.getMousePos()
    #
    #         if self.contains(x, y):
    #             if mouseState == MouseState.CLICK:
    #                 self.selected = True
    #                 global_params.enable_pan = not self.selected
    #
    #         if mouseState == MouseState.RELEASE:
    #             self.selected = False
    #             global_params.enable_pan = not self.selected
    #
    #         if self.selected:
    #             if self.vertical:
    #                 self.value = self.max - self.round((y - self.screen_y) / self.screen_height * self.max)
    #                 self.value = max(min(self.value, self.max), self.min)
    #             else:
    #                 self.value = self.round((x - self.screen_x) / self.screen_width * self.max + self.min)
    #                 self.value = max(min(self.value, self.max), self.min)
    #
    #             if hasattr(self.parent, "set_obj_values"):
    #                 self.parent.set_obj_values()
    #
    #
    #
    # def contains(self, x, y):
    #     if self.vertical:
    #         handleX = self.screen_x + self.screen_width // 2
    #         handleY = int(self.screen_y + (self.max - self.value) / (self.max - self.min) * self.screen_height)
    #     else:
    #         handleX = int(self.screen_x + (self.value - self.min) / (self.max - self.min) * self.screen_width)
    #         handleY = self.screen_y + self.screen_height // 2
    #
    #     if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
    #         return True
    #
    #     return False
    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.selected = True
                    global_params.enable_pan = not self.selected

            if mouseState == MouseState.RELEASE:
                self.selected = False
                global_params.enable_pan = not self.selected

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round((y - self.screen_y) / self.screen_height * self.max)
                    self.value = max(min(self.value, self.max), self.min)
                else:
                    self.value = self.round((x - self.screen_x) / self.screen_width * self.max + self.min)
                    self.value = max(min(self.value, self.max), self.min)

                if hasattr(self.parent, "set_obj_values"):
                    self.parent.set_obj_values()

    def contains(self, x, y):
        if self.vertical:
            return self.screen_x <= x <= self.screen_x + self.screen_width and self.screen_y <= y <= self.screen_y + self.screen_height
        else:
            return self.screen_x <= x <= self.screen_x + self.screen_width and self.screen_y <= y <= self.screen_y + self.screen_height

    def round(self, value):
        return self.step * round(value / self.step)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def draw(self):
        if not self._hidden and not self._disabled:
            pygame.draw.rect(self.win, self.colour, (
                self.screen_x, self.screen_y, self.screen_width, self.screen_height))

            if self.vertical:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (
                        self.screen_x + self.screen_width // 2, self.screen_y), self.radius)
                    pygame.draw.circle(self.win, self.colour, (
                        self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height),
                        self.radius)
                circle = (int(self.screen_x + self.screen_width // 2),
                          int(self.screen_y + (self.max - self.value) / (self.max - self.min) * self.screen_height))
            else:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (
                        self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.colour, (
                        self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                        self.radius)
                circle = (int(self.screen_x + (self.value - self.min) / (self.max - self.min) * self.screen_width),
                          int(self.screen_y + self.screen_height // 2))

            gfxdraw.filled_circle(self.win, *circle, int(self.handleRadius), self.handleColour)
            gfxdraw.aacircle(self.win, *circle, int(self.handleRadius), self.handleColour)


if __name__ == '__main__':
    from pygame_widgets.textbox import TextBox

    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    slider = Slider(win, 100, 100, 800, 40, min=0, max=99, step=1)
    output = TextBox(win, 475, 200, 50, 50, font_size=30)

    v_slider = Slider(win, 900, 200, 40, 300, min=0, max=99, step=1, vertical=True)
    v_output = TextBox(win, 800, 320, 50, 50, font_size=30)

    output.disable()
    v_output.disable()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        output.setText(slider.getValue())
        v_output.setText(v_slider.getValue())

        update(events)
        pygame.display.update()
