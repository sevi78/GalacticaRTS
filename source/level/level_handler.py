import copy
import math
import random

import pygame

from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.factories.building_factory import building_factory
from source.factories.planet_factory import planet_factory
from source.factories.ship_factory import ship_factory
from source.factories.universe_factory import universe_factory
from source.factories.weapon_factory import weapon_factory
from source.game_play.navigation import navigate_to_position
from source.gui.event_text import event_text
# from source.handlers.building_widget_handler import building_widget_handler
from source.handlers.file_handler import load_file, write_file, get_level_list
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.level.level_dict_generator import LevelDictGenerator
from source.multimedia_library.images import get_image_names_from_folder
from source.multimedia_library.screenshot import capture_screenshot
from source.player.player_handler import player_handler
from source.text.info_panel_text_generator import info_panel_text_generator


class LevelHandler:
    def __init__(self, app):
        self.app = app
        self.win = app.win
        self.data = load_file(f"level_{0}.json", folder="levels")
        # print(f"level_handler.self.data: {self.data}")
        self.data_default = copy.deepcopy(self.data)
        self.level_dict_generator = LevelDictGenerator(self)
        self.level_successes = {}
        self.current_game = None
        self.owner_change = 0

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

    def create_universe(self, **kwargs):
        collectable_items = kwargs.get("collectable_items", None)
        universe_factory.amount = int(math.sqrt(math.sqrt(self.data["globals"]["width"])) * self.data["globals"][
            "universe_density"])
        universe_factory.create_universe(
                pygame.Rect(0, 0,
                self.data["globals"]["width"],
                self.data["globals"]["height"]),

                self.data["globals"]["collectable_item_amount"], collectable_items=collectable_items)

    def generate_level_dict_from_scene(self, **kwargs):
        # start_time = time.time()  # Start timing
        ignore_buildings = kwargs.get("ignore_buildings", False)
        ignore_population = kwargs.get("ignore_population", False)

        data = self.data

        # get players
        data["players"] = {}
        for key, player_obj in config.app.players.items():
            # if not "players" in data.keys():

            data["players"][key] = {}
            data["players"][key]["stock"] = player_obj.get_stock()
            data["players"][key]["population"] = player_obj.stock["population"]
            if ignore_population:
                data["players"][key]["population"] = 0
            data["players"][key]["enemies"] = player_obj.enemies

        # this is to set the human player, should maybe be removed and replaced
        player = config.app.player
        data["player"]["stock"] = player.get_stock()
        data["player"]["population"] = player.stock["population"]
        if ignore_population:
            data["player"]["population"] = 0
        data["player"]["enemies"] = player.enemies

        # get all planets
        for planet in sprite_groups.planets.sprites():
            # print(f"generate_level_dict_from_scene: {data['globals']['level']}")
            if not str(planet.id) in data["celestial_objects"].keys():
                data["celestial_objects"][str(planet.id)] = self.data_default["celestial_objects"]["0"]
                # print(f"generate_level_dict_from_scene key error: planet.id not in data['celestial_objects']: planet.id: {planet.id}\n keys: {data['celestial_objects'].keys()}")

            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    value_ = getattr(planet, key)

                    if key == "buildings" and ignore_buildings:
                        value_ = []

                    if key == "population" and ignore_population:
                        value_ = 0

                    data["celestial_objects"][str(planet.id)][key] = value_
                else:
                    pass
                    # print(f"generate_level_dict_from_scene key error: {planet} has no attribute {key}\n")

        # get all collectable items
        data["collectable_items"] = {}
        for collectable_item in sprite_groups.collectable_items.sprites():
            # initialize data if collectable_item is not in data
            data["collectable_items"][str(collectable_item.id)] = {}

            default_data = {
                "id": 0,
                "image_name": "artefact1_60x31.png",
                "specials": [],
                "world_height": 110,
                "world_width": 110,
                "world_x": 0,
                "world_y": 0,
                "resources": {
                    "energy": 1000,
                    "food": 1000,
                    "minerals": 1000,
                    "water": 1000,
                    "technology": 1000,
                    "population": 0
                    }
                }

            # fill the data from the collectable_item data
            for key, value in default_data.items():
                if hasattr(collectable_item, key):
                    data["collectable_items"][str(collectable_item.id)][key] = getattr(collectable_item, key)

        # get ship config, used if ship is created dynamically
        ship_config = load_file("ship_settings.json", "config")

        # get all ships
        data["ships"] = {}
        for ship in sprite_groups.ships.sprites():
            # initialize data if ship is not in data
            if not str(ship.id) in data["ships"].keys():
                # print(f"generate_level_dict_from_scene key error: ship.id ({ship.id} not in keys: {data['ships'].keys()}\n")
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

            # save owner
            data["ships"][str(ship.id)]["owner"] = ship.owner

        # end_time = time.time()  # End timing
        # execution_time = end_time - start_time
        # print(f"generate_level_dict_from_scene execution time: {execution_time:.4f} seconds")# generate_level_dict_from_scene execution time: 0.0065 seconds

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

    def load_level(self, filename, folder, **kwargs):
        data = kwargs.get("data", None)
        if not data:
            self.current_game = filename
            self.data = load_file(filename, folder=folder)
        else:
            self.data = data

        config.app.level_edit.set_selector_current_value()

        # delete level
        self.delete_level()

        # reset player
        player_handler.reset_players()
        player_handler.set_players_data(self.data)

        # create planets, AND SELECT ONE ! to make ensure no errors are generated!!!
        planet_factory.create_planets_from_data(self.data)
        self.app.selected_planet = sprite_groups.planets.sprites()[0]

        # create ships
        ships = self.data.get("ships")
        for key in ships.keys():
            weapons = ships[key]["weapons"]

            self.app.ship_factory.create_ship(f"{ships[key]['name']}", int(
                    ships[key]["world_x"]), int(
                    ships[key]["world_y"]), config.app, weapons, data=ships[key], owner=ships[key]["owner"])

        # create universe
        if config.draw_universe:
            if "collectable_items" in self.data.keys():
                self.create_universe(collectable_items=self.data["collectable_items"])
            else:
                print("level_handler: collectable_items not in data")
                self.create_universe(collectable_items={})

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
            self.app.ship_container.set_widgets(sprite_groups.convert_sprite_groups_to_container_widget_items_list("ships"))

        if hasattr(self.app, "planet_container"):
            self.app.planet_container.set_widgets(sprite_groups.convert_sprite_groups_to_container_widget_items_list("planets"))

        # setup event_text
        event_text.planet_links = planet_factory.get_all_planet_names()

        # # setup player_edit
        config.app.create_player_edit((self.data["globals"]["players"]))

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

        # print(f"level_handler.update_level_successes(): self.level_successes: {self.level_successes}")
        # update the icons of level select to display the successes
        self.app.level_select.update_icons()

    def reset_planet_owners(self):
        for p in sprite_groups.planets.sprites():
            p.owner = -1
            p.explored = False

    def set_planet_owners_base_planet(self):
        players = self.data["globals"]["players"]

        self.reset_planet_owners()
        planets = [_ for _ in sprite_groups.planets.sprites() if not _.type == "sun"]

        def calculate_distance(p1, p2):
            return ((p1.world_x - p2.world_x) ** 2 + (p1.world_y - p2.world_y) ** 2) ** 0.5

        assigned_planets = []

        for player in range(players):
            if assigned_planets:
                distances = [min(calculate_distance(p, ap) for ap in assigned_planets) for p in planets]
                farthest_planet_idx = distances.index(max(distances))
            else:
                farthest_planet_idx = 0

            farthest_planet = planets.pop(farthest_planet_idx)
            farthest_planet.owner = player
            farthest_planet.get_explored(player)
            assigned_planets.append(farthest_planet)

        # If there are more planets than players, leave the remaining planets unassigned
        for p in planets:
            p.owner = -1
            p.explored = False

    def set_planet_owners(self):
        """
Assigns ownership of celestial bodies to players in three stages:
1. Reset ownerships
2. Set base planets
3. Distribute remaining bodies

Main algorithm:
- Calculates bodies to assign based on population density
- Assigns base planet (sun > planet > moon) to each player
- Distributes remaining bodies by proximity
- Marks planets as explored and allocates resources

Uses:
- Population density setting
- Player list
- Celestial body sprites

Effects:
- Updates planet ownership and exploration
- Resets and updates player data

Note: Requires three consecutive calls for complete setup.
            """

        if self.owner_change == 0:
            self.owner_change += 1
            self.reset_planet_owners()
            return

        elif self.owner_change == 1:
            self.owner_change += 1
            self.set_planet_owners_base_planet()
            return

        elif self.owner_change == 2:
            self.owner_change = 0

        # Reset players
        player_handler.reset_players()

        # Get the number of players
        num_players = len(config.app.players)
        player_ids = [i for i in range(num_players)]

        # Get the population density from configuration
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
                    if moons:
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
                p.get_explored(owner)

        # complete resources
        self.complete_player_resources()

    def get_all_possible_resources_of_player(self) -> dict:
        """ get all possible resources from all players and all its planets:
            returns a dict: {player.owner: list}
        """
        owner_resources = {}
        for planet in sprite_groups.planets.sprites():
            owner = planet.owner
            if not owner == -1:
                owner_resources[owner] = []
                for resource in planet.economy_agent.possible_resources:
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
                    planet.economy_agent.possible_resources = resource_categories

                text += f"complete_player_resources: fixed: {player_name}\n"

            text += f"{self.get_all_possible_resources_of_player()}"

        return text

    def clean_up_level(self) -> None:
        """
Cleans up and corrects inconsistencies in the game level data.

This method performs the following cleanup operations:

1. For each ship in the game:

- Ensures the ship has a valid owner (sets to 0 if -1).
- Resets orbit_object_id to -1 if it's not -1.
- Sets orbit_object to None if it exists.
- Sets target to None if it exists.

2. Checks for and completes any missing player resources.

Side effects:
- Modifies ship attributes: owner, orbit_object_id, orbit_object, and target.
- May modify player resources if incomplete.
"""
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
            print(self.complete_player_resources())

    def update_scene(self, key: str):
        # get selector value
        selector_value = self.data["globals"][key]

        # add object to scene:
        self.update_ships()
        self.update_planets(key, selector_value)
        self.setup_pan_zoom_handler()

    def update_ships(self) -> None:
        # error handling
        owned_planets = [_ for _ in sprite_groups.planets.sprites() if _.owner != -1]
        if not owned_planets:
            print(f"update_ships.error: no owned planets")
            return

        # get data
        players = self.data["globals"]["players"]
        spaceships = self.data["globals"]["spaceship"]
        cargoloaders = self.data["globals"]["cargoloader"]
        spacehunters = self.data["globals"]["spacehunter"]

        # print(f"players:{players},spaceships: {spaceships}, cargoloaders:{cargoloaders},spacehunters: {spacehunters}")

        # delete all ships
        ship_factory.delete_ships()

        # create ships
        weapons = weapon_factory.get_all_weapons()
        for p in owned_planets:
            for spaceship in range(spaceships):
                ship_factory.create_ship("spaceship", p.world_x, p.world_y, config.app,
                        {"laser": weapons["laser"]}, owner=p.owner)

            for spacehunter in range(spacehunters):
                ship_factory.create_ship("spacehunter", p.world_x, p.world_y, config.app,
                        {"rocket": weapons["rocket"]}, owner=p.owner)

            for cargoloader in range(cargoloaders):
                ship_factory.create_ship("cargoloader", p.world_x, p.world_y, config.app, {}, owner=p.owner)

    def update_planets(self, key, selector_value):
        # check if key is a planet:
        if not key in ["suns", "planets", "moons"]:
            return

        key_ = key[:-1]
        # get all planets with the given key
        planet_key_list = [_.id for _ in sprite_groups.planets.sprites() if _.type == key_]

        # check if object needs to be added or deleted based on selector_value
        if selector_value > len(planet_key_list):
            add = True
        else:
            add = False

        # add planet
        if add:
            # get values for the constructor
            border = min(self.data["globals"]["width"], self.data["globals"]["height"]) / 4
            world_x = self.level_dict_generator.get_random_position(
                    self.data["globals"]["width"], border)
            world_y = self.level_dict_generator.get_random_position(
                    self.data["globals"]["height"], border)
            id_ = len(sprite_groups.planets.sprites())

            if key_ == "sun":
                orbit_object_id = id_
                image_names = get_image_names_from_folder(key)

            elif key_ == "planet":
                orbit_object_id = random.choice([_.id for _ in sprite_groups.planets.sprites() if _.type == "sun"])
                image_names = get_image_names_from_folder(key)

            elif key_ == "moon":
                orbit_object_id = random.choice([_.id for _ in sprite_groups.planets.sprites() if _.type == "planet"])
                image_names = get_image_names_from_folder("gifs", startswith_string="moon")

            # generate data
            planet_data = self.level_dict_generator.create_celestial_object(
                    id_, key_, image_names, orbit_object_id, world_x, world_y)
            data = {"celestial_objects": {str(id_): planet_data}}

            # add planet to the scene
            planet_factory.create_planets_from_data(data)
            planet = [_ for _ in sprite_groups.planets.sprites() if _.id == id_][0]

            planet.name = "not set"
        else:
            # remove object from scene
            if len(sprite_groups.planets.sprites()) > 0:
                # get id of the last created planet
                last_planet_id = max([_.id for _ in sprite_groups.planets.sprites() if _.type == key_])

                # get last created planet
                last_planet = [_ for _ in sprite_groups.planets.sprites() if _.type == key_ and _.id == last_planet_id][
                    0]

                # finally delete the planet
                planet_factory.delete_planet(last_planet)

    def randomize_level(self):
        ignorables = ["level"]
        for selector in config.app.level_edit.selectors:
            if not selector.key in ignorables:
                selector.current_value = random.choice(selector.list)
                config.app.level_edit.selector_callback(selector.key, selector.current_value, selector)
        self.refresh_level()

    def refresh_level(self):
        """
Refreshes the current game level by regenerating all game elements.

This method performs the following operations:
1. Deletes the existing level.
2. Generates a new level dictionary from the editor.
3. Creates planets based on the new data.
4. Sets the first planet as the selected planet.
5. Creates ships based on the new data.
6. Initializes the universe.
7. Updates the info text for all buttons in the level editor.
8. Sets up the pan and zoom handler.

Side effects:
- Modifies game state by deleting and recreating level elements.
- Updates config.app.selected_planet.
- Modifies button info texts in the level editor.
- Reinitializes the pan and zoom handler.

Note:
This method assumes the existence of various game components and factories,
such as planet_factory, ship_factory, and level editor buttons.
            """
        self.delete_level()
        self.generate_level_dict_from_editor()
        planet_factory.create_planets_from_data(data=self.data)
        config.app.selected_planet = sprite_groups.planets.sprites()[0]
        config.app.ship_factory.create_ships_from_data(data=self.data)
        self.create_universe()

        # set info text
        for i in config.app.level_edit.buttons:
            i.info_text = info_panel_text_generator.create_create_info_panel_level_text(
                    self.data["globals"]["level"], self.data)

        self.setup_pan_zoom_handler()

    def delete_object(self):
        selected_ships = config.app.box_selection.selected_objects

        # used for ships
        if len(selected_ships) > 0:
            for i in selected_ships:
                i.__delete__(i)

        # used for planets
        selected_planet = config.app.selected_planet
        # planet_id = str(selected_planet.id)
        # if planet_id in config.app.level_handler.data["celestial_objects"].keys():
        #     del config.app.level_handler.data["celestial_objects"][planet_id]
        planet_factory.delete_planet(selected_planet)

    def on_players_changed(self, value: int) -> None:
        # print("on_players_changed:", value)
        config.app.create_player_edit(value)
        self.setup_level_based_on_players()


    def setup_level_based_on_players(self) -> None:
        # print("setup_level_based_on_players")
        # set owner change to ensure the correct planet owner functionality is called
        self.owner_change = 1

        # set planet onwers
        self.set_planet_owners()

        # update the ships
        self.update_ships()

        # generate level dict
        self.generate_level_dict_from_scene(ignore_buildings=True, ignore_population=True)
        # print (f"setup_level_based_on_players: ", self.data)
