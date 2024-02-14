import pygame
from pygame.locals import *

VALUE_SMOOTHING_FACTOR = 0.001
VALUE_DECIMAL_PLACES = 12


class ValueSmoother:
    """Smooths a value over time."""

    def __init__(self, smoothing_factor: float, decimal_places: int) -> None:
        self.value = 0.0001
        self.smoothing_factor = smoothing_factor
        self.target_value = 0.001  # Add a target value to track the desired end value
        self.decimal_places = decimal_places

    def __repr__(self):
        return f"self.smoothing_factor:{self.smoothing_factor}, self.decimal_places: {self.decimal_places}, self.target_value: {self.target_value}, self.value: {self.value}"

    def update(self) -> None:
        # Determine the direction of the change
        if self.target_value > self.value:
            # If the target is greater, increase the current value
            self.value += (self.target_value - self.value) * self.smoothing_factor
        elif self.target_value < self.value:
            # If the target is less, decrease the current value
            self.value -= (self.value - self.target_value) * self.smoothing_factor

        # round to accuracy
        self.value = round(self.value, self.decimal_places)

    def get_smooth_value(self, new_value) -> float:
        self.target_value = new_value
        return self.value

    def set_target_value(self, new_value) -> None:
        self.target_value = new_value



class ValueHandler:
    def __init__(self) -> None:
        self.values = {}

    def __repr__(self):
        return f"self.values: {[(_, self.values[_].__repr__()) for _ in self.values.keys()]}"

    def add_value(self, key, value_smoother):
        self.values[key] = value_smoother

    def get_smooth_value(self, key, value):
        if key not in self.values:
            self.add_value(key, ValueSmoother(VALUE_SMOOTHING_FACTOR, VALUE_DECIMAL_PLACES))
        return self.values[key].get_smooth_value(value)


    def update(self):
        for _, value_smoother in self.values.items():
            value_smoother.update()


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.running = True

    def run(self):
        while self.running:
            value_handler.update()

            mx, my = pygame.mouse.get_pos()
            pygame.display.get_surface().fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 0, 255), (
                value_handler.get_smooth_value("mx", mx), value_handler.get_smooth_value("my", my), 10, 10), 1)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()

            pygame.display.flip()


if __name__ == '__main__':
    app = App()
    # value_smoother_x = ValueSmoother(VALUE_SMOOTHING_FACTOR)
    # value_smoother_y = ValueSmoother(VALUE_SMOOTHING_FACTOR)
    value_handler = ValueHandler()
    app.run()
