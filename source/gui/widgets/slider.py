import pygame
from pygame import gfxdraw

from source.configuration.game_config import config
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.mouse_handler import mouse_handler, MouseState
from source.handlers.widget_handler import update


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
    - get_value: returns the current selected value of the slider
    - set_value: sets the current selected value of the slider to the given value

    Fields:
    - selected: a boolean indicating whether the handle of the slider is currently selected
    - min: the minimum value of the slider range
    - max: the maximum value of the slider range
    - step: the step size of the slider
    - color: the color of the slider
    - handle_color: the color of the handle of the slider
    - border_thickness: the thickness of the border of the slider
    - border_color: the color of the border of the slider
    - value: the current selected value of the slider
    - curved: a boolean indicating whether the slider is curved or straight
    - vertical: a boolean indicating whether the slider is vertical or horizontal
    - radius: the radius of the curved part of the slider
    - handle_radius: the radius of the handle of the slider
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)

        self.selected = False

        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 99)
        self.step = kwargs.get('step', 1)

        self.color = kwargs.get('color', (200, 200, 200))
        self.handle_color = kwargs.get('handle_color', (0, 0, 0))

        self.border_thickness = kwargs.get('border_thickness', 3)
        self.border_color = kwargs.get('border_color', (0, 0, 0))

        self.value = self.round(kwargs.get('initial', (self.max + self.min) / 2))
        self.function = kwargs.get('function', None)

        self.curved = kwargs.get('curved', True)

        self.vertical = kwargs.get('vertical', False)

        if self.curved:
            if self.vertical:
                self.radius = self.screen_width // 2
            else:
                self.radius = self.screen_height // 2

        if self.vertical:
            self.handle_radius = kwargs.get('handle_radius', int(self.screen_width / 1.3))
        else:
            self.handle_radius = kwargs.get('handle_radius', int(self.screen_height / 1.3))

    def listen(self, events):
        # if not config.app.game_client.is_host:
        #     return

        if not self._hidden and not self._disabled:
            mouse_state = mouse_handler.get_mouse_state()
            x, y = mouse_handler.get_mouse_pos()

            if self.contains(x, y):
                if mouse_state == MouseState.LEFT_CLICK:
                    self.selected = True
                    config.enable_pan = not self.selected

            if mouse_state == MouseState.LEFT_RELEASE:
                self.selected = False
                config.enable_pan = not self.selected

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round((y - self.screen_y) / self.screen_height * self.max)
                    self.value = max(min(self.value, self.max), self.min)
                else:
                    self.value = self.round((x - self.screen_x) / self.screen_width * self.max + self.min)
                    self.value = max(min(self.value, self.max), self.min)

                if self.function:
                    self.function(self.value)

                if hasattr(self.parent, "set_obj_values"):
                    self.parent.set_obj_values()

    def contains(self, x, y):
        if self.vertical:
            return self.screen_x <= x <= self.screen_x + self.screen_width and self.screen_y <= y <= self.screen_y + self.screen_height
        else:
            return self.screen_x <= x <= self.screen_x + self.screen_width and self.screen_y <= y <= self.screen_y + self.screen_height

    def round(self, value):
        return self.step * round(value / self.step)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        if self.function:
            self.function(self.value)

    def draw(self):
        if not self._hidden and not self._disabled:
            pygame.draw.rect(self.win, self.color, (
                self.screen_x, self.screen_y, self.screen_width, self.screen_height))

            if self.vertical:
                if self.curved:
                    pygame.draw.circle(self.win, self.color, (
                        self.screen_x + self.screen_width // 2, self.screen_y), self.radius)
                    pygame.draw.circle(self.win, self.color, (
                        self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height),
                            self.radius)
                circle = (int(self.screen_x + self.screen_width // 2),
                          int(self.screen_y + (self.max - self.value) / (self.max - self.min) * self.screen_height))
            else:
                if self.curved:
                    pygame.draw.circle(self.win, self.color, (
                        self.screen_x, self.screen_y + self.screen_height // 2), self.radius)
                    pygame.draw.circle(self.win, self.color, (
                        self.screen_x + self.screen_width, self.screen_y + self.screen_height // 2),
                            self.radius)
                circle = (int(self.screen_x + (self.value - self.min) / (self.max - self.min) * self.screen_width),
                          int(self.screen_y + self.screen_height // 2))

                gfxdraw.filled_circle(self.win, *circle, int(self.handle_radius), self.handle_color)
                gfxdraw.aacircle(self.win, *circle, int(self.handle_radius), self.handle_color)


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

        output.setText(slider.get_value())
        v_output.setText(v_slider.get_value())

        update(events)
        pygame.display.update()
