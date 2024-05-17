import copy
import math
import random

from source.configuration.game_config import config
from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.game_play.navigation import navigate_to_position
from source.gui.event_text import event_text
from source.economy.economy_handler import economy_handler
from source.handlers.file_handler import load_file, write_file, get_level_list
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.player_handler import player_handler
from source.multimedia_library.images import get_image_names_from_folder
from source.multimedia_library.screenshot import capture_screenshot
from source.text.info_panel_text_generator import info_panel_text_generator
from source.text.text_formatter import to_roman


class LevelDictGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.solar_system_names = [
            "Astrovoid",
            "Starhaven",
            "Nebulon",
            "Galactica",
            "Cosmoria",
            "Pulsaris",
            "Quasaria",
            "Vortexia",
            "Ecliptor",
            "Cometra",
            "Meteoros",
            "Supernovus",
            "Asteria",
            "Celestium",
            "Stargate",
            "Lunaris",
            "Satalia",
            "Planetara",
            "Astroisle",
            "Orbiton",
            "Graviton",
            "Radiance",
            "Interstella",
            "Galaxium",
            "Univera",
            "Exoplanos",
            "Photonis",
            "Spectron",
            "Dwarfstar",
            "Blackholia",
            "Redgianta",
            "Whitedwarf",
            "Neutronia",
            "Milkywaya",
            "Andromedus",
            "Pleiadia",
            "Orionis",
            "Cassiopea",
            "Cygnara",
            "Perseidus",
            "Ursara",
            "Tauron",
            "Arietis",
            "Geminia",
            "Cancera",
            "Leonis",
            "Virgon",
            "Libria",
            "Scorpius",
            "Sagittar",
            "Capricorn",
            "Aquaria",
            "Piscea",
            "Ophiuchi",
            "Serpentis",
            "Drakonis",
            "Centauri",
            "Phoenixa",
            "Hydria",
            "Lyria",
            "Pegasia",
            "Herculia",
            "Velara",
            "Carinae",
            "Puppis",
            "Aquilae",
            "Cygnara",
            "Lupus",
            "Corvus",
            "Cruxis",
            "Grusia",
            "Tucana",
            "Pavonis",
            "Indus",
            "Vulpecula",
            "Monoceros",
            "Lynx",
            "Caelum",
            "Columba",
            "Equuleus",
            "Microscopium",
            "Telescopium",
            "Horologium",
            "Reticulum",
            "Pictor",
            "Sculptor",
            "Fornax"
            ]
        self.sun_names = {}  # Dictionary to store sun names
        self.planet_names = {}  # Dictionary to store planet names
        self.moon_names = {}  # Dictionary to store moon names
        self.ship_settings = load_file("ship_settings.json", "config")

    def create_suns(self, data):
        sun_images = get_image_names_from_folder("suns")
        border = min(self.parent.data["globals"]["width"], self.parent.data["globals"]["height"]) / 4

        for i in range(self.parent.data["globals"]["suns"]):
            world_x = self.get_random_position(self.parent.data["globals"]["width"], border)
            world_y = self.get_random_position(self.parent.data["globals"]["height"], border)
            sun_name = random.choice(self.solar_system_names)
            self.sun_names[i] = sun_name  # Store sun name in the dictionary
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "sun", sun_images, i, world_x, world_y)

    def create_planets(self, data):
        planet_images = get_image_names_from_folder("planets")
        for i in range(
                self.parent.data["globals"]["suns"],
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"]):
            orbit_object_id = random.choice(list(self.sun_names.keys()))  # Get a random sun ID
            orbit_distance = self.parent.data["globals"]["width"] / len(self.sun_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            planet_name = f"{self.sun_names[orbit_object_id]} {to_roman(i - self.parent.data['globals']['suns'] + 1)}"
            self.planet_names[i] = planet_name

            # Store planet name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "planet", planet_images, orbit_object_id, world_x, world_y)

    def create_moons(self, data):
        moon_images = get_image_names_from_folder("gifs", startswith_string="moon")
        for i in range(
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"],
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"] +
                self.parent.data["globals"]["moons"]):
            orbit_object_id = random.choice(list(self.planet_names.keys()))  # Get a random planet ID
            orbit_distance = self.parent.data["globals"]["width"] / len(self.planet_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            moon_name = f"{self.planet_names[orbit_object_id]}, {chr(97 + i - self.parent.data['globals']['suns'] + self.parent.data['globals']['planets'])}"
            self.moon_names[i] = moon_name

            # Store moon name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "moon", moon_images, orbit_object_id, world_x, world_y)

    def create_ships(self, data):
        # get all ships from editor
        all_ships = []
        if "spaceship" in self.parent.data["globals"].keys():
            all_ships += ["spaceship" for _ in range(self.parent.data["globals"]["spaceship"])]
        if "spacehunter" in self.parent.data["globals"].keys():
            all_ships += ["spacehunter" for _ in range(self.parent.data["globals"]["spacehunter"])]
        if "cargoloader" in self.parent.data["globals"].keys():
            all_ships += ["cargoloader" for _ in range(self.parent.data["globals"]["cargoloader"])]

        # all_ships = (["spaceship" for _ in range(self.parent.data["globals"]["spaceship"])] +
        #              ["spacehunter" for _ in range(self.parent.data["globals"]["spacehunter"])] +
        #              ["cargoloader" for _ in range(self.parent.data["globals"]["cargoloader"])])

        border = min(self.parent.data["globals"]["width"], self.parent.data["globals"]["height"]) / 4

        # reset data
        self.parent.data["ships"] = {}

        # create data
        for index, ship_name in enumerate(all_ships):
            world_x = self.get_random_position(self.parent.data["globals"]["width"], border)
            world_y = self.get_random_position(self.parent.data["globals"]["height"], border)
            weapons = {
                "laser": {
                    "name": "laser",
                    "level": 0,
                    "production_energy": 0,
                    "production_food": 0,
                    "production_minerals": 0,
                    "production_water": 0,
                    "production_technology": 0,
                    "production_population": 0,
                    "price_energy": 2500,
                    "price_food": 2500,
                    "price_minerals": 2500,
                    "price_water": 2500,
                    "price_technology": 2500,
                    "price_population": 0,
                    "build_population_minimum": 0,
                    "building_production_time_scale": 5,
                    "building_production_time": 5,
                    "population_buildings_value": 0,
                    "technology_upgrade": {},
                    "range": 100,
                    "power": 3,
                    "shoot_interval": 1.0,
                    "upgrade cost": {
                        "level_0": {
                            "price_energy": 1500,
                            "price_food": 1000,
                            "price_minerals": 1500,
                            "price_water": 250,
                            "price_technology": 500,
                            "price_population": 0
                            },
                        "level_1": {
                            "price_energy": 2500,
                            "price_food": 2000,
                            "price_minerals": 2500,
                            "price_water": 250,
                            "price_technology": 500,
                            "price_population": 0
                            },
                        "level_2": {
                            "price_energy": 2500,
                            "price_food": 2000,
                            "price_minerals": 2500,
                            "price_water": 250,
                            "price_technology": 500,
                            "price_population": 0
                            }
                        },
                    "upgrade values": {
                        "level_0": {
                            "level": 0,
                            "range": 1.0,
                            "power": 1.0,
                            "shoot_interval": 1.0
                            },
                        "level_1": {
                            "level": 1,
                            "range": 1.5,
                            "power": 1.5,
                            "shoot_interval": 1.5
                            },
                        "level_2": {
                            "level": 2,
                            "range": 2.0,
                            "power": 2.0,
                            "shoot_interval": 2.0
                            }
                        }
                    }
                }

            ship_data = {
                "name": ship_name,
                "world_x": world_x,
                "world_y": world_y,
                "weapons": weapons if ship_name == "spacehunter" else {},
                "food": 0,
                "food_max": self.ship_settings[ship_name]["food_max"],
                "minerals": 0,
                "minerals_max": self.ship_settings[ship_name]["minerals_max"],
                "water": 0,
                "water_max": self.ship_settings[ship_name]["water_max"],
                "technology": 0,
                "technology_max": self.ship_settings[ship_name]["technology_max"],
                "energy": 9306,
                "energy_max": self.ship_settings[ship_name]["energy_max"],
                "crew": self.ship_settings[ship_name]["crew"],
                "crew_max": self.ship_settings[ship_name]["crew_max"],
                "fog_of_war_radius": 100,
                "fog_of_war_radius_max": 300,
                "upgrade_factor": 1.5,
                "upgrade_factor_max": 3.0,
                "reload_max_distance_raw": 300,
                "attack_distance_raw": 200,
                "desired_orbit_radius_raw": 100,
                "speed": self.ship_settings[ship_name]["speed"],
                "speed_max": self.ship_settings[ship_name]["speed_max"],
                "orbit_speed": 0.5,
                "orbit_speed_max": 0.6,
                "orbit_radius": 130,
                "orbit_radius_max": 300,
                "min_dist_to_other_ships": 80,
                "min_dist_to_other_ships_max": 200,
                "energy_use": self.ship_settings[ship_name]["energy_use"],
                "energy_reload_rate": self.ship_settings[ship_name]["energy_reload_rate"],
                "specials": [],
                "orbit_object_id": -1,
                "orbit_object_name": "",
                "owner": 0
                }

            self.parent.data["ships"][str(index)] = ship_data

    def get_random_position(self, limit, border):
        position = random.uniform(0 + border, limit - border)
        return min(max(position, 0), limit)

    def get_orbit_position(self, orbit_object, orbit_distance):
        angle = random.uniform(0, 2 * math.pi)
        world_x = orbit_object["world_x"] + orbit_distance * math.cos(angle)
        world_y = orbit_object["world_y"] + orbit_distance * math.sin(angle)
        return world_x, world_y

    def generate_name(self, i, body_type, orbit_object_id):
        try:
            if body_type == "sun":
                return self.sun_names[orbit_object_id]  # Retrieve sun name from the dictionary
            elif body_type == "planet":
                sun_name = self.sun_names[orbit_object_id]
                planet_number = to_roman(i - self.parent.data["globals"]["suns"] + 1)
                return f"{sun_name} {planet_number}"
            elif body_type == "moon":
                planet_name = self.planet_names[orbit_object_id]
                moon_letter = chr(97 + i - self.parent.data["globals"]["suns"] - self.parent.data["globals"][
                    "planets"])  # 97 is the ASCII value for 'a'
                return f"{planet_name}, {moon_letter}"

        except KeyError as e:
            print("generate_name error: ", e)
            return "no name generated"

    def create_celestial_object(
            self, i: int, body_type: str, images: list, orbit_object_id: int, world_x: int,
            world_y: int
            ):
        name = self.generate_name(i, body_type, orbit_object_id)
        gifs = get_image_names_from_folder("gifs")
        atmospheres = []
        moons = [i for i in gifs if i.startswith("moon")]

        if body_type == "sun":
            size = random.randint(90, 110)
            atmospheres = [i for i in gifs if i.startswith("sun")] + [""]
        elif body_type == "planet":
            size = random.randint(60, 80)
            atmospheres = [i for i in gifs if i.startswith("atmosphere")] + [""]
        elif body_type == "moon":
            size = random.randint(30, 50)
            atmospheres = [""]

        has_alien_pop = random.randint(0, 4)
        if has_alien_pop == 4:
            alien_population = random.randint(0, 1000000000)
        else:
            alien_population = 0

        owner = random.randint(-1, config.players)
        if owner == 0:
            owner = -1

        return {
            "id": i,
            "name": name,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": size,
            "world_height": size,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": random.uniform(0.1, 1.0),
            "population": 0,
            "alien_population": alien_population,
            "alien_attitude": random.randint(0, 100),
            "buildings_max": random.randint(5, 20),
            "building_slot_amount": random.randint(1, 5),
            "buildings": [],
            "specials": [],
            "type": body_type,
            "possible_resources": economy_handler.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.0001, 0.001) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": random.choice(atmospheres),
            "orbit_angle": None,
            "explored": False,
            "gif": random.choice(moons),
            "owner": owner
            }


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

        data = self.data

        # get players
        data["players"] = {}
        for key, player_obj in config.app.players.items():
            # if not "players" in data.keys():

            data["players"][key] = {}
            data["players"][key]["stock"] = player_obj.get_stock()
            data["players"][key]["population"] = player_obj.population
            data["players"][key]["enemies"] = player_obj.enemies

        # this is to set the human player, should maybe be removed and replaced
        player = config.app.player
        data["player"]["stock"] = player.get_stock()
        data["player"]["population"] = player.population
        data["player"]["enemies"] = player.enemies

        # get all planets
        for planet in sprite_groups.planets.sprites():
            print(f"generate_level_dict_from_scene: {data['globals']['level']}")
            if not str(planet.id) in data["celestial_objects"].keys():
                data["celestial_objects"][str(planet.id)] = self.data_default["celestial_objects"]["0"]
                print(f"generate_level_dict_from_scene key error: planet.id not in data['celestial_objects']: planet.id: {planet.id}\n keys: {data['celestial_objects'].keys()}")

            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    value_ = getattr(planet, key)

                    if key == "buildings":
                        if ignore_buildings:
                            value_ = []
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
            self.app.ship_container.set_widgets(sprite_groups.convert_sprite_groups_to_image_widget_list("ships"))

            # self.app.ship_container.filter_widget.show()

        if hasattr(self.app, "planet_container"):
            self.app.planet_container.set_widgets(sprite_groups.convert_sprite_groups_to_image_widget_list("planets"))
            # self.app.ship_container.filter_widget.show()

        # setup event_text
        event_text.planet_links = planet_factory.get_all_planet_names()

    def save_level(self, filename, folder):
        data = self.generate_level_dict_from_scene(ignore_buildings=True)
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

    def set_planet_owners(self):

        player_handler.reset_players()
        self.set_planet_owners_geographically()
        # self.set_celestial_body_owners()

        return
        population_density = int(self.data["globals"]["population_density"])
        for i in sprite_groups.planets:
            r = random.randint(0, 100)
            if r in range(0, population_density):
                i.owner = random.randint(0, len(config.app.players) - 1)
            else:
                i.owner = -1

    def set_planet_owners_geographically(self):
        player_handler.reset_players()
        population_density = int(self.data["globals"]["population_density"])
        num_players = len(config.app.players)

        # Step 1: Divide the planets into clusters
        clusters = self.divide_planets_into_clusters(num_players)

        # Step 2: Assign each cluster to a player
        for player_id, cluster in enumerate(clusters):
            for planet in cluster:
                # There's a chance based on population_density that a planet will be owned by a player
                r = random.randint(0, 100)
                if r < population_density:
                    planet.owner = player_id
                else:
                    planet.owner = -1

    def divide_planets_into_clusters(self, num_clusters):
        # This is a placeholder for the clustering logic. You might use a simple geometric approach,
        # or a more complex clustering algorithm like K-means, depending on your game's requirements
        # and the structure of your planet objects.
        # For simplicity, let's assume each planet has attributes `x` and `y` for its position.

        # Example simple clustering based on x-coordinate (for illustration purposes only):
        sorted_planets = sorted(sprite_groups.planets.sprites(), key=lambda p: p.world_x)
        clusters = [[] for _ in range(num_clusters)]
        for i, planet in enumerate(sorted_planets):
            clusters[i % num_clusters].append(planet)

        return clusters

    def set_celestial_body_owners_(self):# oroginal
        player_handler.reset_players()
        population_density = int(self.data["globals"]["population_density"])
        num_players = len(config.app.players)

        # Assuming `sprite_groups.suns` holds all sun objects
        suns = [i for i in sprite_groups.planets if i.type == "sun"]

        for sun in suns:
            # There's a chance based on population_density that a celestial body will be owned by a player
            r = random.randint(0, 100)
            if r < population_density:
                owner_id = random.randint(0, num_players - 1)
            else:
                owner_id = -1

            # Set owner for the sun
            sun.owner = owner_id

            # Propagate the owner to all planets of the sun
            sun_planets = [i for i in sprite_groups.planets if i.type == "planet" and i.orbit_object_id == sun.id]
            for planet in sun_planets:  # Assuming `sun.planets` holds all planet objects belonging to the sun
                planet.owner = owner_id

                # Propagate the owner to all moons of the planet
                planet_moons = [i for i in sprite_groups.planets if i.type == "moon" and i.orbit_object_id == planet.id]
                for moon in planet_moons:  # Assuming `planet.moons` holds all moon objects belonging to the planet
                    moon.owner = owner_id

    def set_celestial_body_owners___(self):
        player_handler.reset_players()
        population_density = int(self.data["globals"]["population_density"])
        num_players = len(config.app.players)

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons

        # Shuffle the list to ensure random distribution
        random.shuffle(celestial_bodies)

        # Assign each celestial body to a player based on population density
        for index, body in enumerate(celestial_bodies):
            if random.randint(0, 100) < population_density:
                owner_id = index % num_players  # This ensures a more even distribution
            else:
                owner_id = -1
            body.owner = owner_id

        # Optionally, you can propagate ownership from suns to their planets and moons
        for sun in [b for b in celestial_bodies if b.type == "sun"]:
            sun_planets = [p for p in celestial_bodies if p.type == "planet" and p.orbit_object_id == sun.id]
            for planet in sun_planets:
                planet.owner = sun.owner  # Propagate sun's owner to its planets
                planet_moons = [m for m in celestial_bodies if m.type == "moon" and m.orbit_object_id == planet.id]
                for moon in planet_moons:
                    moon.owner = planet.owner  # Propagate planet's owner to its moons

    def set_celestial_body_owners____(self):
        player_handler.reset_players()
        population_density = int(self.data["globals"]["population_density"])
        num_players = len(config.app.players)

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons

        # Shuffle the list to ensure random distribution
        random.shuffle(celestial_bodies)

        # Ensure each player gets at least one planet
        for i in range(num_players):
            celestial_bodies[i].owner = i

        # Assign the rest of the celestial bodies based on population density
        for index, body in enumerate(celestial_bodies[num_players:], start=num_players):
            if random.randint(0, 100) < population_density:
                owner_id = index % num_players  # This ensures a more even distribution
            else:
                owner_id = -1
            body.owner = owner_id

        # Optionally, propagate ownership from suns to their planets and moons
        for sun in [b for b in celestial_bodies if b.type == "sun"]:
            sun_planets = [p for p in celestial_bodies if p.type == "planet" and p.orbit_object_id == sun.id]
            for planet in sun_planets:
                planet.owner = sun.owner  # Propagate sun's owner to its planets
                planet_moons = [m for m in celestial_bodies if m.type == "moon" and m.orbit_object_id == planet.id]
                for moon in planet_moons:
                    moon.owner = planet.owner  # Propagate planet's owner to its moons

    def set_celestial_body_owners_____(self):
        # Reset players
        player_handler.reset_players()

        # Get population density from configuration
        population_density = int(self.data["globals"]["population_density"])

        # Get the number of players
        num_players = len(config.app.players)

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons

        # Shuffle the list to ensure random initial distribution
        random.shuffle(celestial_bodies)

        # Ensure each player gets at least one celestial body
        for i in range(num_players):
            celestial_bodies[i].owner = i

        # Assign the rest of the celestial bodies
        for index, body in enumerate(celestial_bodies[num_players:], start=num_players):
            # Calculate owner based on index to ensure even distribution
            owner_id = index % num_players
            body.owner = owner_id

        # Optionally, propagate ownership from suns to their planets and moons
        for sun in [b for b in celestial_bodies if b.type == "sun"]:
            sun_planets = [p for p in celestial_bodies if p.type == "planet" and p.orbit_object_id == sun.id]
            for planet in sun_planets:
                planet.owner = sun.owner  # Propagate sun's owner to its planets
                planet_moons = [m for m in celestial_bodies if m.type == "moon" and m.orbit_object_id == planet.id]
                for moon in planet_moons:
                    moon.owner = planet.owner  # Propagate planet's owner to its moons

    import random

    def set_celestial_body_owners_____(self):
        # Reset players
        player_handler.reset_players()

        # Get population density from configuration
        population_density = int(self.data["globals"]["population_density"])

        # Get the number of players
        num_players = len(config.app.players)

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons

        # Shuffle the list to ensure random initial distribution
        random.shuffle(celestial_bodies)

        # Calculate the minimum number of celestial bodies per player
        min_bodies_per_player = len(celestial_bodies) // num_players
        extra_bodies = len(celestial_bodies) % num_players

        # Distribute celestial bodies
        current_body_index = 0
        for player_id in range(num_players):
            # Assign the minimum number of bodies to each player
            for _ in range(min_bodies_per_player):
                celestial_bodies[current_body_index].owner = player_id
                current_body_index += 1

            # Distribute remaining bodies
            if extra_bodies > 0:
                celestial_bodies[current_body_index].owner = player_id
                current_body_index += 1
                extra_bodies -= 1

        # Optionally, propagate ownership from suns to their planets and moons
        for sun in [b for b in celestial_bodies if b.type == "sun"]:
            sun_planets = [p for p in celestial_bodies if p.type == "planet" and p.orbit_object_id == sun.id]
            for planet in sun_planets:
                planet.owner = sun.owner  # Propagate sun's owner to its planets
                planet_moons = [m for m in celestial_bodies if m.type == "moon" and m.orbit_object_id == planet.id]
                for moon in planet_moons:
                    moon.owner = planet.owner  # Propagate planet's owner to its moons

    import random

    import random

    # def set_celestial_body_owners(self):
    #     # Reset players
    #     player_handler.reset_players()
    #
    #     # Get the number of players
    #     num_players = len(config.app.players)
    #
    #     # Collect all celestial bodies
    #     celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons
    #
    #     # Shuffle the list to ensure random initial distribution
    #     random.shuffle(celestial_bodies)
    #
    #     # Group celestial bodies by their solar systems
    #     solar_systems = {}
    #     for body in celestial_bodies:
    #         if body.type == "sun":
    #             solar_systems[body.id] = {"sun": body, "planets": [], "moons": []}
    #         elif body.type == "planet":
    #             if body.orbit_object_id in solar_systems:
    #                 solar_systems[body.orbit_object_id]["planets"].append(body)
    #             else:
    #                 print(f"Warning: Sun with ID {body.orbit_object_id} not found for planet {body.id}")
    #         elif body.type == "moon":
    #             planet_found = False
    #             for system in solar_systems.values():
    #                 for planet in system["planets"]:
    #                     if planet.id == body.orbit_object_id:
    #                         system["moons"].append(body)
    #                         planet_found = True
    #                         break
    #                 if planet_found:
    #                     break
    #             if not planet_found:
    #                 print(f"Warning: Planet with ID {body.orbit_object_id} not found for moon {body.id}")
    #
    #     # Flatten the solar systems into a list for easier distribution
    #     solar_system_list = list(solar_systems.values())
    #
    #     # Calculate the minimum number of solar systems per player
    #     min_systems_per_player = len(solar_system_list) // num_players
    #     extra_systems = len(solar_system_list) % num_players
    #
    #     # Distribute solar systems
    #     current_system_index = 0
    #     for player_id in range(num_players):
    #         # Assign the minimum number of systems to each player
    #         for _ in range(min_systems_per_player):
    #             self.assign_system_to_player(solar_system_list[current_system_index], player_id)
    #             current_system_index += 1
    #
    #         # Distribute remaining systems
    #         if extra_systems > 0:
    #             self.assign_system_to_player(solar_system_list[current_system_index], player_id)
    #             current_system_index += 1
    #             extra_systems -= 1
    #
    # def assign_system_to_player(self, system, player_id):
    #     # Assign the sun to the player
    #     system["sun"].owner = player_id
    #
    #     # Assign all planets in the system to the player
    #     for planet in system["planets"]:
    #         planet.owner = player_id
    #
    #     # Assign all moons in the system to the player
    #     for moon in system["moons"]:
    #         moon.owner = player_id

    import random

    # def set_celestial_body_owners(self):
    #     # Reset players
    #     player_handler.reset_players()
    #
    #     # Get the number of players
    #     num_players = len(config.app.players)
    #
    #     # Collect all celestial bodies
    #     celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons
    #
    #     # Shuffle the list to ensure random initial distribution
    #     random.shuffle(celestial_bodies)
    #
    #     # Group celestial bodies by their solar systems
    #     solar_systems = {}
    #     for body in celestial_bodies:
    #         if body.type == "sun":
    #             solar_systems[body.id] = {"sun": body, "planets": [], "moons": []}
    #         elif body.type == "planet":
    #             if body.orbit_object_id in solar_systems:
    #                 solar_systems[body.orbit_object_id]["planets"].append(body)
    #             else:
    #                 print(f"Warning: Sun with ID {body.orbit_object_id} not found for planet {body.id}")
    #         elif body.type == "moon":
    #             planet_found = False
    #             for system in solar_systems.values():
    #                 for planet in system["planets"]:
    #                     if planet.id == body.orbit_object_id:
    #                         system["moons"].append(body)
    #                         planet_found = True
    #                         break
    #                 if planet_found:
    #                     break
    #             if not planet_found:
    #                 print(f"Warning: Planet with ID {body.orbit_object_id} not found for moon {body.id}")
    #
    #     # Flatten the solar systems into a list for easier distribution
    #     solar_system_list = list(solar_systems.values())
    #
    #     # Calculate the minimum number of solar systems per player
    #     min_systems_per_player = len(solar_system_list) // num_players
    #     extra_systems = len(solar_system_list) % num_players
    #
    #     # Distribute solar systems in a round-robin fashion
    #     player_systems = [[] for _ in range(num_players)]
    #     for i, system in enumerate(solar_system_list):
    #         player_id = i % num_players
    #         player_systems[player_id].append(system)
    #
    #     # Assign systems to players
    #     for player_id, systems in enumerate(player_systems):
    #         for system in systems:
    #             self.assign_system_to_player(system, player_id)
    #
    # def assign_system_to_player(self, system, player_id):
    #     # Assign the sun to the player
    #     system["sun"].owner = player_id
    #
    #     # Assign all planets in the system to the player
    #     for planet in system["planets"]:
    #         planet.owner = player_id
    #
    #     # Assign all moons in the system to the player
    #     for moon in system["moons"]:
    #         moon.owner = player_id

    # def set_celestial_body_owners(self):
    #     # Reset players
    #     player_handler.reset_players()
    #
    #     # Get the number of players
    #     num_players = len(config.app.players)
    #
    #     # Collect all celestial bodies
    #     celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons
    #
    #     # Shuffle the list to ensure random initial distribution
    #     random.shuffle(celestial_bodies)
    #
    #     # Group celestial bodies by their solar systems
    #     solar_systems = {}
    #     for body in celestial_bodies:
    #         if body.type == "sun":
    #             solar_systems[body.id] = {"sun": body, "planets": [], "moons": []}
    #         elif body.type == "planet":
    #             if body.orbit_object_id in solar_systems:
    #                 solar_systems[body.orbit_object_id]["planets"].append(body)
    #             else:
    #                 print(f"Warning: Sun with ID {body.orbit_object_id} not found for planet {body.id}")
    #         elif body.type == "moon":
    #             planet_found = False
    #             for system in solar_systems.values():
    #                 for planet in system["planets"]:
    #                     if planet.id == body.orbit_object_id:
    #                         system["moons"].append(body)
    #                         planet_found = True
    #                         break
    #                 if planet_found:
    #                     break
    #             if not planet_found:
    #                 print(f"Warning: Planet with ID {body.orbit_object_id} not found for moon {body.id}")
    #
    #     # Flatten the solar systems into a list for easier distribution
    #     solar_system_list = list(solar_systems.values())
    #
    #     # Calculate the minimum number of solar systems per player
    #     min_systems_per_player = len(solar_system_list) // num_players
    #     extra_systems = len(solar_system_list) % num_players
    #
    #     # Distribute solar systems
    #     player_systems = [[] for _ in range(num_players)]
    #     for i, system in enumerate(solar_system_list):
    #         player_id = i % num_players
    #         player_systems[player_id].append(system)
    #
    #         # Ensure each player gets at least the minimum number of systems
    #         if len(player_systems[player_id]) >= min_systems_per_player:
    #             continue
    #
    #     # Assign extra systems to players in a round-robin fashion
    #     for i in range(extra_systems):
    #         player_systems[i].append(solar_system_list[-(i + 1)])
    #
    #     # Assign systems to players
    #     for player_id, systems in enumerate(player_systems):
    #         for system in systems:
    #             self.assign_system_to_player(system, player_id)
    #
    # def assign_system_to_player(self, system, player_id):
    #     # Assign the sun to the player
    #     system["sun"].owner = player_id
    #
    #     # Assign all planets in the system to the player
    #     for planet in system["planets"]:
    #         planet.owner = player_id
    #
    #     # Assign all moons in the system to the player
    #     for moon in system["moons"]:
    #         moon.owner = player_id

    # def set_celestial_body_owners(self):
    #     # Reset players
    #     player_handler.reset_players()
    #
    #     # Get the number of players
    #     num_players = len(config.app.players)
    #
    #     # Collect all celestial bodies
    #     celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons
    #
    #     # Shuffle the list to ensure random initial distribution
    #     random.shuffle(celestial_bodies)
    #
    #     # Get the population density from configuration
    #     population_density = int(self.data["globals"]["population_density"])
    #
    #     # Group celestial bodies by their solar systems
    #     solar_systems = {}
    #     for body in celestial_bodies:
    #         if body.type == "sun":
    #             solar_systems[body.id] = {"sun": body, "planets": [], "moons": []}
    #         elif body.type == "planet":
    #             if body.orbit_object_id in solar_systems:
    #                 solar_systems[body.orbit_object_id]["planets"].append(body)
    #             else:
    #                 print(f"Warning: Sun with ID {body.orbit_object_id} not found for planet {body.id}")
    #         elif body.type == "moon":
    #             planet_found = False
    #             for system in solar_systems.values():
    #                 for planet in system["planets"]:
    #                     if planet.id == body.orbit_object_id:
    #                         system["moons"].append(body)
    #                         planet_found = True
    #                         break
    #                 if planet_found:
    #                     break
    #             if not planet_found:
    #                 print(f"Warning: Planet with ID {body.orbit_object_id} not found for moon {body.id}")
    #
    #     # Flatten the solar systems into a list for easier distribution
    #     solar_system_list = list(solar_systems.values())
    #
    #     # Calculate the minimum number of solar systems per player
    #     min_systems_per_player = len(solar_system_list) // num_players
    #     extra_systems = len(solar_system_list) % num_players
    #
    #     # Distribute solar systems
    #     player_systems = [[] for _ in range(num_players)]
    #     for i, system in enumerate(solar_system_list):
    #         player_id = i % num_players
    #         player_systems[player_id].append(system)
    #
    #         # Ensure each player gets at least the minimum number of systems
    #         if len(player_systems[player_id]) >= min_systems_per_player:
    #             continue
    #
    #     # Assign extra systems to players in a round-robin fashion
    #     for i in range(extra_systems):
    #         player_systems[i].append(solar_system_list[-(i + 1)])
    #
    #     # Assign systems to players
    #     for player_id, systems in enumerate(player_systems):
    #         for system in systems:
    #             self.assign_system_to_player(system, player_id, population_density)
    #
    # def assign_system_to_player(self, system, player_id, population_density):
    #     # Assign the sun to the player
    #     system["sun"].owner = player_id
    #
    #     # Assign planets in the system to the player based on population density
    #     for planet in system["planets"]:
    #         r = random.randint(0, 100)
    #         if r < population_density:
    #             planet.owner = player_id
    #         else:
    #             planet.owner = -1
    #
    #     # Assign moons in the system to the player based on their planet's owner
    #     for moon in system["moons"]:
    #         planet = next((p for p in system["planets"] if p.id == moon.orbit_object_id), None)
    #         if planet:
    #             moon.owner = planet.owner
    #         else:
    #             print(f"Warning: Planet with ID {moon.orbit_object_id} not found for moon {moon.id}")


    def set_celestial_body_owners(self):
        # Reset players
        player_handler.reset_players()

        # Get the number of players
        num_players = len(config.app.players)

        # Collect all celestial bodies
        celestial_bodies = sprite_groups.planets.sprites()  # Assuming this includes suns, planets, and moons

        # Shuffle the list to ensure random initial distribution
        random.shuffle(celestial_bodies)

        # Get the population density from configuration
        population_density = int(self.data["globals"]["population_density"])

        # Group celestial bodies by their solar systems
        solar_systems = {}
        for body in celestial_bodies:
            if body.type == "sun":
                solar_systems[body.id] = {"sun": body, "planets": [], "moons": []}
            elif body.type == "planet":
                if body.orbit_object_id in solar_systems:
                    solar_systems[body.orbit_object_id]["planets"].append(body)
                else:
                    print(f"Warning: Sun with ID {body.orbit_object_id} not found for planet {body.id}")
            elif body.type == "moon":
                planet_found = False
                for system in solar_systems.values():
                    for planet in system["planets"]:
                        if planet.id == body.orbit_object_id:
                            system["moons"].append(body)
                            planet_found = True
                            break
                    if planet_found:
                        break
                if not planet_found:
                    print(f"Warning: Planet with ID {body.orbit_object_id} not found for moon {body.id}")

        # Flatten the solar systems into a list for easier distribution
        solar_system_list = list(solar_systems.values())

        # Calculate the minimum number of solar systems per player
        min_systems_per_player = len(solar_system_list) // num_players
        extra_systems = len(solar_system_list) % num_players

        # Distribute solar systems
        player_systems = [[] for _ in range(num_players)]
        for i, system in enumerate(solar_system_list):
            player_id = i % num_players
            player_systems[player_id].append(system)

            # Ensure each player gets at least the minimum number of systems
            if len(player_systems[player_id]) >= min_systems_per_player:
                continue

        # Assign extra systems to players in a round-robin fashion
        for i in range(extra_systems):
            player_systems[i].append(solar_system_list[-(i + 1)])

        # Assign systems to players
        for player_id, systems in enumerate(player_systems):
            for system in systems:
                self.assign_system_to_player(system, player_id, population_density)

    def assign_system_to_player(self, system, player_id, population_density):
        # Assign the sun to the player
        system["sun"].owner = player_id

        # Assign planets in the system to the player based on population density
        for planet in system["planets"]:
            r = random.randint(0, 100)
            if r < population_density:
                planet.owner = player_id
            else:
                planet.owner = -1

        # Assign moons in the system to the player based on their planet's owner
        for moon in system["moons"]:
            planet = next((p for p in system["planets"] if p.id == moon.orbit_object_id), None)
            if planet:
                moon.owner = planet.owner
            else:
                print(f"Warning: Planet with ID {moon.orbit_object_id} not found for moon {moon.id}")

    import random

