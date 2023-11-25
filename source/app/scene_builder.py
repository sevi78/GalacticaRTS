import random

import pygame

from source.app.ui_helper import UIHelper
from source.configuration.economy_params import EconomyParams
from source.database.database_access import get_database_file_path
from source.factories.planet_factory import planet_factory
from source.pan_zoom_sprites.pan_zoom_collectable_item import PanZoomCollectableItem
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ships import Spaceship, Spacehunter, Cargoloader
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.universe.background_image import BackgroundImage
from source.universe.fog_of_war import FogOfWar
from source.universe.universe_background import Universe
from source.utils import global_params
from source.utils.colors import colors
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups


class GameObjectStorage:
    def __init__(self):
        self.game_objects = []
        self.planets = sprite_groups.planets.sprites()
        self.collectables = []
        self.ufos = []
        self.building_widget_list = []
        self.planet_buttons = []
        self.ships = sprite_groups.ships.sprites()
        self.editors = []
        self.missiles = pygame.sprite.Group()
        self.gif_handlers = pygame.sprite.Group()
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
        # BuildMenu.__init__(self, config)

        # UI Helper
        self.frame_color = colors.frame_color
        self.ui_helper = UIHelper(self)
        self.level = 1

        # background
        self.create_universe_background()

        # fog of war
        self.create_fog_of_war()

        # planets
        planet_factory.create_planets_from_db(get_database_file_path())

        # artefacts
        self.create_artefacts()

        # ship
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2
        spacing = 100

        self._ship = None
        self.ship = self.create_ship("spaceship_30x30.png", center_x, center_y + 300)
        self.create_ship("cargoloader_30x30.png", center_x - spacing, center_y + 400)
        self.create_ship("spacehunter_30x30.png", center_x + spacing, center_y + 500)

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

    def create_ship(self, name, x, y):
        """ creates a ship from the image name like: schiff1_30x30"""
        size_x, size_y = map(int, name.split("_")[1].split(".")[0].split("x"))
        name = name.split("_")[0]
        class_ = name[0].upper() + name[1:]

        if class_ == "Spaceship":
            ship = Spaceship(global_params.win, x, y, size_x, size_y, pan_zoom_handler, "spaceship_30x30.png",
                debug=False, group="ships", parent=self, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1)

        if class_ == "Spacehunter":
            ship = Spacehunter(global_params.win, x, y, size_x, size_y, pan_zoom_handler, "spacehunter_30x30.png",
                debug=False, group="ships", parent=self, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1)

        if class_ == "Cargoloader":
            ship = Cargoloader(global_params.win, x, y, size_x + 20, size_y + 20, pan_zoom_handler, "cargoloader_30x30.png",
                debug=False, group="ships", parent=self, rotate_to_target=True, move_to_target=True,
                align_image="center", layer=1)
        return ship

    def select_resources(self):
        resources = ["water", "food", "energy", "technology", "minerals"]
        selected_resources = {"water": 0, "food": 0, "energy": 0, "technology": 0, "minerals": 0}
        amount_of_all = random.randint(0, 1000)
        total_amount = 0
        while total_amount < amount_of_all:
            resource = random.choice(resources)
            amount = random.randint(0, amount_of_all)
            if total_amount + amount > 1000:
                amount = 1000 - total_amount
            if resource in selected_resources:
                selected_resources[resource] += amount
            else:
                selected_resources[resource] = amount
            total_amount += amount
        return selected_resources

    def create_artefacts(self):
        w = global_params.scene_width * global_params.quadrant_amount
        h = global_params.scene_height * global_params.quadrant_amount
        buffer = 100

        images_scaled = {0: get_image("artefact1_60x31.png"),
                         1: get_image("meteor_50x50.png"),
                         2: get_image("meteor_60x83.png"),
                         3: get_image("meteor1_50x50.png")
                         }

        image_names = ["artefact1_60x31.png",
                       "meteor_50x50.png",
                       "meteor_60x83.png",
                       "meteor1_50x50.png"
                       ]

        for i in range(20):
            selected_resources = self.select_resources()
            artefact = PanZoomCollectableItem(global_params.win,
                random.randint(buffer, w - buffer), random.randint(buffer, h - buffer), 50, 50,
                pan_zoom=pan_zoom_handler,
                image_name=random.choice(image_names),
                isSubWidget=False,
                transparent=True,
                tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                moveable=True,
                energy=selected_resources["energy"],
                minerals=selected_resources["minerals"],
                food=selected_resources["food"],
                technology=selected_resources["technology"],
                water=selected_resources["water"],
                parent=self,
                group="collectable_items", gif="sphere.gif", align_image="center")

        for i in range(20):
            selected_resources = self.select_resources()
            artefact = PanZoomCollectableItem(global_params.win,
                random.randint(buffer, w - buffer), random.randint(buffer, h - buffer), 100, 100,
                pan_zoom=pan_zoom_handler,
                image_name="sphere.gif",
                isSubWidget=False,
                transparent=True,
                tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
                moveable=True,
                energy=selected_resources["energy"],
                minerals=selected_resources["minerals"],
                food=selected_resources["food"],
                technology=selected_resources["technology"],
                water=selected_resources["water"],
                parent=self,
                group="collectable_items",
                gif="sphere.gif", relative_gif_size=0.1, align_image="center")
