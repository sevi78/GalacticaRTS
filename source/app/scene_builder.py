import pygame

from source.app.ui_helper import UIHelper
from source.economy.economy_params import EconomyParams
from source.handlers.color_handler import colors


class GameObjectStorage:
    def __init__(self):
        """TODO: reduce dependencies """
        self.building_widget_list = []
        self.editors = []
        self.building_button_widgets = []
        self.explored_planets = []

    def add_explored_planet(self, planet):
        self.explored_planets.append(planet)
        # sort the planets by orbit_object_id and type
        self.explored_planets.sort(key=lambda x: (x.orbit_object_id, self.get_type_order(x.type)))
        self.update_building_button_widgets()

    def get_type_order(self, type_):
        order = {"sun": 1, "planet": 2, "moon": 3}
        return order.get(type_, 4)


class SceneBuilder(EconomyParams, GameObjectStorage):
    def __init__(self, width, height):
        """
        creates all scene elemets like ships and planets, background , fog of war
        :param width:
        :param height:
        """

        EconomyParams.__init__(self)
        GameObjectStorage.__init__(self)

        # UI Helper
        self.frame_color = colors.frame_color
        self.ui_helper = UIHelper(self)

        # ship
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2
        spacing = 100

        self._ship = None
        self.ship = self.ship_factory.create_ship("spaceship", center_x, center_y + 300, self, {}, owner=0)

    @property
    def ship(self):
        return self._ship

    @ship.setter
    def ship(self, value):  # orig
        self._ship = value
        if value:
            if hasattr(self, "ship_edit"):
                if self.ship_edit:
                    self.ship_edit.set_obj(value)

            if hasattr(self, "weapon_select"):
                if self.weapon_select:
                    self.weapon_select.obj = value
                    self.weapon_select.update_obj()
                    self.weapon_select.update()
