import random

from source.multimedia_library.sounds import sounds
from source.utils import global_params


class PanZoomShipInteraction:
    def __init__(self):
        # functionality
        self.orbiting = False
        self._selected = False
        self.target = None

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def orbit_object(self):
        return self._orbit_object

    @orbit_object.setter
    def orbit_object(self, value):
        self._orbit_object = value
        if value:
            self.target = None
            self.orbiting = True
            self.orbit_direction = random.choice([-1, 1])
        else:
            self.orbiting = False
            self.orbit_angle = None

    @property
    def enemy(self):
        return self._enemy

    @enemy.setter
    def enemy(self, value):
        self._enemy = value
        if not value:
            self.orbit_angle = None
            self.orbit_object = None
            self.target_reached = False

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)
            global_params.app.ship = self


