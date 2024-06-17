import copy
import math
import random

import source.trading.market
from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.factories.building_factory import building_factory
from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.game_play.navigation import navigate_to_position
from source.gui.event_text import event_text
from source.handlers.file_handler import load_file, write_file, get_level_list
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.level.level_dict_generator import LevelDictGenerator
from source.multimedia_library.screenshot import capture_screenshot
from source.player.player_handler import player_handler
from source.text.info_panel_text_generator import info_panel_text_generator


class LevelHandler:
    def __init__(self, app):
        self.app = app
        self.win = app.win
        self.data = load_file(f"level_{0}.json", folder="levels")
        self.data_default = copy.deepcopy(self.data)
        self.level_dict_generator = LevelDictGenerator(self)
        self.level_successes = {}
        self.current_game = None

    def delete_level(self):
        # delete objects
        # universe
        universe_factory.delete_universe()

        # artefacts
        universe_factory.delete_artefacts()

        # planets
        planet_factory.delete_planets()

        # ships
        self.app.ship_factory.delete_ships()

        # collectable items
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()

        # ufos
        for i in sprite_groups.ufos.sprites():
            i.end_object(explode=False)

        # gif_handlers
        for i in sprite_groups.gif_handlers.sprites():
            i.end_object()

        # building widgets
        for i in config.app.building_widget_list:
            i.delete()

        config.app.building_widget_list = []

    def create_universe(self):
        universe_factory.amount = int(math.sqrt(math.sqrt(self.data["globals"]["width"])) * self.data["globals"][
            "universe_density"])
        universe_factory.create_universe(0, 0, self.data["globals"]["width"], self.data["globals"]["height"])
        universe_factory.create_artefacts(0, 0, self.data["globals"]["width"], self.data["globals"]["height"],
                self.data["globals"]["collectable_item_amount"])

    def generate_level_dict_from_scene(self, **kwargs):
        ignore_buildings = kwargs.get("ignore_buildings", False)
        ignore_population = kwargs.get("ignore_population", False)

        data = self.data

        # get players
        data["players"] = {}
        for key, player_obj in config.app.players.items():
            # if not "players" in data.keys():

            data["players"][key] = {}
            data["players"][key]["stock"] = player_obj.get_stock()
            data["players"][key]["population"] = player_obj.population
            if ignore_population:
                data["players"][key]["population"] = 0
            data["players"][key]["enemies"] = player_obj.enemies

        # this is to set the human player, should maybe be removed and replaced
        player = config.app.player
        data["player"]["stock"] = player.get_stock()
        data["player"]["population"] = player.population
        if ignore_population:
            data["player"]["population"] = 0
        data["player"]["enemies"] = player.enemies

        # get all planets
        # data["celestial_objects"] = {}
        for planet in sprite_groups.planets.sprites():
            print(f"generate_level_dict_from_scene: {data['globals']['level']}")
            if not str(planet.id) in data["celestial_objects"].keys():
                data["celestial_objects"][str(planet.id)] = self.data_default["celestial_objects"]["0"]
                print(f"generate_level_dict_from_scene key error: planet.id not in data['celestial_objects']: planet.id: {planet.id}\n keys: {data['celestial_objects'].keys()}")

            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    value_ = getattr(planet, key)

                    if key == "buildings" and ignore_buildings:
                        value_ = []

                    if key == "population" and ignore_population:
                        value_ = 0

                    data["celestial_objects"][str(planet.id)][key] = value_
                else:
                    print(f"generate_level_dict_from_scene key error: {planet} has no attribute {key}\n")

        # get ship config, used if ship is created dynamically
        ship_config = load_file("ship_settings.json", "config")

        # get all ships
        for ship in sprite_groups.ships.sprites():
            # initialize data if ship is not in data
            if not str(ship.id) in data["ships"].keys():
                print(f"generate_level_dict_from_scene key error: ship.id ({ship.id} not in keys: {data['ships'].keys()}\n")
                data["ships"][str(ship.id)] = {"name": "", "world_x": 0, "world_y": 0}

            # fill the data from the ship data
            for key, value in data["ships"][str(ship.id)].items():
                if hasattr(ship, key):
                    data["ships"][str(ship.id)][key] = getattr(ship, key)

            # fill rest of the values from ship config
            for var in ship_config[ship.name].keys():
                if hasattr(ship, var):
                    data["ships"][str(ship.id)][var] = getattr(ship, var)

            # get weapons from ship weapon_handler
            data["ships"][str(ship.id)]["weapons"] = ship.weapon_handler.weapons

            # get specials loaded in ship
            data["ships"][str(ship.id)]["specials"] = ship.specials

        return data

    def generate_level_dict_from_editor(self):
        # print("self.data:")
        # pprint (self.data["globals"])
        self.level_dict_generator.create_suns(self.data)
        self.level_dict_generator.create_planets(self.data)
        self.level_dict_generator.create_moons(self.data)
        self.level_dict_generator.create_ships(self.data)

        # print("celestial_objects:")
        # # print (f"identical:{self.data['celestial_objects']['0'].keys() == self.data_default['celestial_objects']['0'].keys()}")
        # print(f"not in keys(): {[i for i in self.data['celestial_objects']['0'].keys() if i not in self.data_default['celestial_objects']['0'].keys()]}")
        # pprint(self.data['celestial_objects'])

    def setup_pan_zoom_handler(self) -> None:
        # calculate the min zoom factor
        pan_zoom_handler.zoom_min = 1000 / self.data["globals"]["width"]

        # set zoom
        pan_zoom_handler.set_zoom(pan_zoom_handler.zoom_min)

        # navigate zo center of the level
        navigate_to_position(self.data["globals"]["width"] / 2, self.data["globals"]["height"] / 2)

    def load_level(self, filename, folder):
        self.current_game = filename
        self.data = load_file(filename, folder=folder)
        config.app.level_edit.set_selector_current_value()

        # delete level
        self.delete_level()

        # reset player
        # self.app.player.reset(self.data["player"])
        player_handler.reset_players()
        player_handler.set_players_data(self.data)

        # create planets, AND SELECT ONE ! to make ensure no errors are generated!!!
        planet_factory.create_planets_from_data(self.data)
        self.app.selected_planet = sprite_groups.planets.sprites()[0]

        # create ships
        ships = self.data.get("ships")
        for key in ships.keys():
            self.app.ship_factory.create_ship(f"{ships[key]['name']}", int(
                    ships[key]["world_x"]), int(
                    ships[key]["world_y"]), config.app, ships[key]["weapons"], data=ships[key])

        # create universe
        if config.draw_universe:
            self.create_universe()

        # setup game_event_handler
        self.app.game_event_handler.level = config.app.level_handler.data.get("globals").get("level")
        self.app.game_event_handler.set_goal(config.app.level_handler.data.get("globals").get("goal"))

        # setup mission
        self.app.settings_panel.mission_icon.info_text = info_panel_text_generator.create_info_panel_mission_text()
        config.edit_mode = False

        economy_handler.calculate_global_production(config.app.player)

        # setup pan_zoom_handler
        self.setup_pan_zoom_handler()

        # setup container
        if hasattr(self.app, "ship_container"):
            self.app.ship_container.set_widgets(source.trading.market.convert_sprite_groups_to_container_widget_items_list("ships"))

            # self.app.ship_container.filter_widget.show()

        if hasattr(self.app, "planet_container"):
            self.app.planet_container.set_widgets(source.trading.market.convert_sprite_groups_to_container_widget_items_list("planets"))
            # self.app.ship_container.filter_widget.show()

        # setup event_text
        event_text.planet_links = planet_factory.get_all_planet_names()

    def save_level(self, filename, folder):
        data = self.generate_level_dict_from_scene(ignore_buildings=True, ignore_population=True)
        write_file(filename, folder, data)

        # save screenshot
        screen_x, screen_y = pan_zoom_handler.world_2_screen(0, 0)
        capture_screenshot(
                self.win,
                f"level_{self.data['globals']['level']}.png",
                (screen_x, screen_y, self.data["globals"]["width"] * pan_zoom_handler.zoom,
                 self.data["globals"]["height"] * pan_zoom_handler.zoom),
                (360, 360),
                event_text=event_text)

        # file_handler.get_level_list()
        self.app.level_select.update_icons()

    def save_level_succcess_to_file(self, filename, folder, value):
        # load file
        data = load_file(filename, folder=folder)

        # write value into the dict
        data["globals"]["level_success"] = value

        # write the data back to the file
        write_file(filename, folder, data)

    def get_level_success_from_file(self, filename, folder) -> dict:
        # load file
        data = load_file(filename, folder=folder)
        return {str(data["globals"]["level"]): data["globals"]["level_success"]}

    def update_level_successes(self):
        # update level_successes
        for filename in get_level_list():
            level_success_dict = self.get_level_success_from_file(filename, "levels")
            for key, value in level_success_dict.items():
                self.level_successes[key] = value

        print(f"level_handler.update_level_successes(): self.level_successes: {self.level_successes}")
        # update the icons of level select to display the successes
        self.app.level_select.update_icons()

    def set_planet_owners(self):  # best so far
        # Reset players
        player_handler.reset_players()

        # Get the number of players
        num_players = len(config.app.players)
        player_ids = [i for i in range(num_players)]
        player_ids.remove(0)

        # # Get the population density from configuration
        population_density = int(self.data["globals"]["population_density"])

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons
        num_celestial_bodies = len(celestial_bodies)

        # get all planets based on population_density
        planet_amount = int(num_celestial_bodies / 100 * population_density)

        # reset ownerships
        for p in celestial_bodies:
            p.owner = -1

        random.shuffle(player_ids)
        for owner in player_ids:
            # get free suns
            suns = [i for i in celestial_bodies if i.type == "sun" and i.owner == -1]
            base_planet = None

            # if a free sun is available, choose this sun
            if suns:
                base_planet = random.choice(suns)

            # if no free sun left, choose a planet
            else:
                planets = [i for i in celestial_bodies if i.type == "planet" and i.owner == -1]
                if planets:
                    base_planet = random.choice(planets)

                # if no free planet left, choose a moon
                else:
                    moons = [i for i in celestial_bodies if i.type == "moon" and i.owner == -1]
                    base_planet = random.choice(moons)

            # set owner to base planet
            if base_planet:
                base_planet.owner = owner

            # choose the nearest planets
            amount = int(planet_amount / len(player_ids))
            sorted_sprites = sprite_groups.sort_sprites_by_distance(sprite_groups.planets.sprites(), base_planet)

            owner_planets = sorted_sprites[0:amount]
            for p in owner_planets:
                p.owner = owner

        # complete resources
        self.complete_player_resources()

    def get_all_possible_resources_of_player(self) -> dict:
        """ get all possible resources from all players and all its planets:
            returns a dict: {player.owner: list}
        """
        owner_resources = {}
        for planet in sprite_groups.planets.sprites():
            owner = planet.owner
            if not owner ==-1:
                owner_resources[owner] = []
                for resource in planet.possible_resources:
                    if not resource in owner_resources[owner]:
                        owner_resources[owner].append(resource)

        return owner_resources

    def check_for_complete_player_resources(self) -> list:
        """ checks if every player has at least every resource in the planets
            returns a list with all incomplete player ids
        """
        # get all possible resources from all players and all planets
        owner_resources = self.get_all_possible_resources_of_player()
        incomplete_players_ids = []

        # check if it has all resources
        for id_, resource_list in owner_resources.items():
            if not len(resource_list) == 5:
                incomplete_players_ids.append(id_)
        return incomplete_players_ids

    def complete_player_resources(self) -> str:
        """ checks if every player has at least every resource in the planets,
            if not,  it completes the list of possible resources
        """
        resource_categories = building_factory.get_resource_categories()
        ids_ = self.check_for_complete_player_resources()
        text = "complete_player_resources: no incomplete player resources fixed"
        if len(ids_) != 0:
            text = ""
            for id_ in ids_:
                player = config.app.players[id_]
                player_name = player.name
                text += f"complete_player_resources: found incomplete player resources: {player_name}\n"
                owner_planets = [p for p in sprite_groups.planets.sprites() if p.owner == id_]
                for i in range(2):
                    planet = random.choice(owner_planets)
                    planet.possible_resources = resource_categories

                text += f"complete_player_resources: fixed: {player_name}\n"

            text += f"{self.get_all_possible_resources_of_player()}"

        return text

    def clean_up_level(self) -> None:
        """this cleas up all rubbish like false orbit object_ids ect"""
        print("clean_up_level: cleaning up: ")

        # ships
        for ship in sprite_groups.ships.sprites():
            # ensure the ships has a correct owner
            if ship.owner == -1:
                ship.owner = 0
                print(f"clean_up_level: setting ship owner to 0: {ship.name}")

            if ship.orbit_object_id != -1:
                ship.orbit_object_id = -1
                print(f"clean_up_level: setting ship orbit_object_id to -1: {ship.name}")

            if ship.orbit_object:
                ship.orbit_object = None
                print(f"clean_up_level: setting ship orbit_object to None: {ship.name}")

            if ship.target:
                ship.target = None
                print(f"clean_up_level: setting ship.target to None: {ship.name}")

        # planets
        ids_ = self.check_for_complete_player_resources()
        if len(ids_) != 0:
            print (self.complete_player_resources())
