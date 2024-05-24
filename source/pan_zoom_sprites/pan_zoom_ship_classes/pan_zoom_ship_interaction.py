import random

from source.configuration.game_config import config
from source.interaction.interaction_handler import InteractionHandler
from source.multimedia_library.sounds import sounds


class PanZoomShipInteraction(InteractionHandler):
    def __init__(self, kwargs):
        InteractionHandler.__init__(self)
        # functionality
        # self.orbiting = False
        self._selected = False
        self.target = None
        self.autopilot = kwargs.get("autopilot", False)

    # @property
    # def autopilot(self):
    #     return self._autopilot
    #
    # @autopilot.setter
    # def autopilot(self, value):
    #     self._autopilot = value
    #     self.state_engine.set_state()

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
            self.orbit_object_id = value.id
            self.orbit_object_name = value.name
        else:
            self.orbiting = False
            self.orbit_angle = None
            self.orbit_object_id = -1
            self.orbit_object_name = ""

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
            config.app.ship = self
