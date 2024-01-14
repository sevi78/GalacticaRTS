import pygame

from source.app.ui_helper import UIHelper
from source.configuration.economy_params import EconomyParams
from source.handlers.file_handler import load_file
from source.factories.planet_factory import planet_factory
from source.universe.background_image import BackgroundImage
from source.universe.fog_of_war import FogOfWar
from source.factories.universe_factory import Universe
from source.configuration import global_params
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image


class GameObjectStorage:
    def __init__(self):
        """TODO: reduce dependencies """
        self.building_widget_list = []
        self.editors = []
        self.building_button_widgets = []
        self.explored_planets = []

    def add_explored_planet(self, planet):
        self.explored_planets.append(planet)
        self.update_building_button_widgets()


class SceneBuilder(EconomyParams, GameObjectStorage):
    def __init__(self, width, height):
        """
        creates all scene elemts like ships and planets, background , fog of war
        :param width:
        :param height:
        """

        EconomyParams.__init__(self)
        GameObjectStorage.__init__(self)


        # UI Helper
        self.frame_color = colors.frame_color
        self.ui_helper = UIHelper(self)

        # background
        self.create_universe_background()

        # fog of war
        self.create_fog_of_war()

        # planets
        planet_factory.create_planets_from_data(load_file(f"level_{0}.json"))

        # ship
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2
        spacing = 100

        self._ship = None
        self.ship = self.ship_factory.create_ship("spaceship_30x30.png", center_x, center_y + 300, self)

    @property
    def ship(self):
        return self._ship

    @ship.setter
    def ship(self, value):
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

    def create_fog_of_war(self):
        return
        self.fog_of_war = FogOfWar(global_params.win, 0, 0, global_params.scene_width, global_params.scene_height, False, layer=2)

    def create_background(self):
        self.background_image = BackgroundImage(global_params.win,
            x=0,
            y=0,
            width=global_params.WIDTH,
            height=global_params.HEIGHT,
            isSubWidget=False,
            image=get_image("bg.png").convert(),
            layer=0, property="background")

    def create_universe_background(self):
        if global_params.draw_universe:
            self.universe = Universe(global_params.win, 0, 0, global_params.scene_width, global_params.scene_height, isSubWidget=False, layer=3)
