import random

import pygame

from source.app.ui_helper import UIHelper
from source.configuration.economy_params import EconomyParams
from source.database.database_access import get_database_file_path, create_connection

from source.gui.build_menu import BuildMenu, config
from source.pan_zoom_sprites.pan_zoom_collectable_item import PanZoomCollectableItem
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet
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


class SceneBuilder(EconomyParams, GameObjectStorage, BuildMenu):
    def __init__(self, width, height):
        """
        creates all scene elemts like ships and planets, background , fog of war
        :param width:
        :param height:
        """

        EconomyParams.__init__(self)
        GameObjectStorage.__init__(self)
        BuildMenu.__init__(self, config)

        # UI Helper
        self.frame_color = colors.frame_color
        self.ui_helper = UIHelper(self)
        self.level = 1

        # background
        self.create_universe_background()

        # fog of war
        self.create_fog_of_war()

        # planets
        self.create_planets_from_db(get_database_file_path())

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

        # width = 800
        # height = 600
        # self.ship_edit = ShipEdit(pygame.display.get_surface(),
        #     pygame.display.get_surface().get_rect().centerx - width / 2,
        #     pygame.display.get_surface().get_rect().y,
        #     width, height, parent=self, obj=self.ship, layer=9)

        self.create_ship("cargoloader_30x30.png", center_x - spacing, center_y + 400)
        self.create_ship("spacehunter_30x30.png", center_x + spacing, center_y + 500)
        # self.create_ship("ufo_74x30.png", center_x + spacing, center_y + 400)

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
                align_image="center", layer= 1)

        if class_ == "Spacehunter":
            ship = Spacehunter(global_params.win, x, y, size_x, size_y, pan_zoom_handler, "spacehunter_30x30.png",
                debug=False, group="ships", parent=self, rotate_to_target=True, move_to_target=True,
                align_image="center", layer= 1)

        if class_ == "Cargoloader":
            ship = Cargoloader(global_params.win, x, y, size_x + 20 , size_y + 20, pan_zoom_handler, "cargoloader_30x30.png",
                debug=False, group="ships", parent=self, rotate_to_target=True, move_to_target=True,
                align_image="center", layer= 1)
        return ship

    def create_planets_from_db(self, database_file):
        """loads values from database and construct the planet object
        """
        conn = create_connection(database_file)
        cur = conn.cursor()
        ids_tuples_list = cur.execute("select id from planets").fetchall()
        ids = [t[0] for t in ids_tuples_list]

        for id in ids:
            self.create_planet(cur, id)








    def create_planet(self, cur, id):
        image_name = cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0]
        width, height = map(int, image_name.split("_")[1].split(".")[0].split("x"))
        type = cur.execute(f"select type from planets where id = {id}").fetchone()[0]

        gif = None

        has_atmosphere = cur.execute(f"SELECT has_atmosphere FROM planets WHERE id = {id}").fetchone()[0]
        if type == "sun":
            gif = "sun.gif"

        if type == "moon":
            gif = "moon1.gif"

        elif has_atmosphere:
            gif = "atmosphere.gif"


        pan_zoom_planet_button = PanZoomPlanet(
            win=global_params.win,
            x=cur.execute(f"select world_x from planets where id = {id}").fetchone()[0],
            y=cur.execute(f"select world_y from planets where id = {id}").fetchone()[0],
            width=int(cur.execute(f"select world_width from planets where id = {id}").fetchone()[0]),
            height=int(cur.execute(f"select world_height from planets where id = {id}").fetchone()[0]),
            pan_zoom=pan_zoom_handler,
            isSubWidget=False,
            image=get_image(
                cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0]),
            image_name=cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0],
            transparent=True,
            info_text=cur.execute(f"select info_text from planets where id = {id}").fetchone()[0],
            text=cur.execute(f"select name from planets where id = {id}").fetchone()[0],
            textColour=self.frame_color,
            property="planet",
            name=cur.execute(f"select name from planets where id = {id}").fetchone()[0],
            parent=self,
            tooltip="send your ship to explore the planet!",
            possible_resources=eval(
                cur.execute(f"select possible_resources from planets where id = {id}").fetchone()[0]),
            moveable=global_params.moveable,
            hover_image=get_image("selection_150x150.png"),
            has_atmosphere=cur.execute(f"SELECT has_atmosphere FROM planets WHERE id = {id}").fetchone()[0],
            textVAlign="below_the_bottom",
            layer=0,
            id=id,
            orbit_object_id=cur.execute(f"select orbit_object_id from planets where id = {id}").fetchone()[0],
            image_name_small=cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0],
            image_name_big=cur.execute(f"select image_name_big from planets where id = {id}").fetchone()[0],
            buildings_max=cur.execute(f"select buildings_max from planets where id = {id}").fetchone()[0],
            orbit_speed=cur.execute(f"select orbit_speed from planets where id = {id}").fetchone()[0],
            orbit_angle=cur.execute(f"select orbit_angle from planets where id = {id}").fetchone()[0],
            building_slot_amount=
            cur.execute(f"select building_slot_amount from planets where id = {id}").fetchone()[0],
            alien_population=cur.execute(f"select alien_population from planets where id = {id}").fetchone()[0],
            specials=cur.execute(f"select specials from planets where id = {id}").fetchone()[0],
            type=type,
            gif=gif,
            debug=False,
            align_image="center"
            )
        #pan_zoom_planet_button.load_from_db()
        sprite_groups.planets.add(pan_zoom_planet_button)
        #pan_zoom_planet_button.load_from_db()


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
                group="collectable_items", gif="sphere.gif", align_image= "center")

        for i in range(20):
            selected_resources = self.select_resources()
            artefact = PanZoomCollectableItem(global_params.win,
                random.randint(buffer, w - buffer), random.randint(buffer, h - buffer), 50, 50,
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
                gif="sphere.gif", relative_gif_size=0.1, align_image= "center")
