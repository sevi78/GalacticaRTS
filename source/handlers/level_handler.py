import copy
import math
import random
from pprint import pprint

from source.configuration import global_params
from source.factories.building_factory import building_factory

from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.gui.event_text import event_text
from source.handlers.economy_handler import economy_handler
from source.handlers.file_handler import load_file, write_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image_names_from_folder
from source.multimedia_library.screenshot import capture_screenshot
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
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
        # !!! here must be the orbit bug!!! setting the orbit distance and angele might be a bad idea
        planet_ids = []
        planet_images = get_image_names_from_folder("planets")
        for i in range(
                self.parent.data["globals"]["suns"],
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"]):
            orbit_object_id = random.choice(list(self.sun_names.keys()))  # Get a random sun ID
            orbit_distance = self.parent.data["globals"]["width"] / len(self.sun_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            planet_name = f"{self.sun_names[orbit_object_id]} {to_roman(i - self.parent.data['globals']['suns'] + 1)}"
            self.planet_names[i] = planet_name  # Store planet name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "planet", planet_images, orbit_object_id, world_x, world_y)

    def create_moons(self, data):
        moon_images = ["moon.gif", "moon1.gif"]  # get_image_names_from_folder("moons")#
        for i in range(
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"],
                self.parent.data["globals"]["suns"] + self.parent.data["globals"]["planets"] +
                self.parent.data["globals"]["moons"]):
            orbit_object_id = random.choice(list(self.planet_names.keys()))  # Get a random planet ID
            orbit_distance = self.parent.data["globals"]["width"] / len(self.planet_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            moon_name = f"{self.planet_names[orbit_object_id]}, {chr(97 + i - self.parent.data['globals']['suns'] + self.parent.data['globals']['planets'])}"
            self.moon_names[i] = moon_name  # Store moon name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "moon", moon_images, orbit_object_id, world_x, world_y)

    def get_random_position(self, limit, border):
        position = random.uniform(0 + border, limit - border)
        return min(max(position, 0), limit)

    def get_orbit_position(self, orbit_object, orbit_distance):
        angle = random.uniform(0, 2 * math.pi)
        world_x = orbit_object["world_x"] + orbit_distance * math.cos(angle)
        world_y = orbit_object["world_y"] + orbit_distance * math.sin(angle)
        return world_x, world_y

    def generate_name(self, i, body_type, orbit_object_id):
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

    def create_celestial_object(self, i, body_type, images, orbit_object_id, world_x, world_y):
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

        return {
            "id": i,
            "name": name,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": size,
            "world_height": size,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": random.uniform(0.1, 1.0),
            "population":0,
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
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": random.choice(atmospheres),
            "orbit_angle": None,
            "explored": False,
            "gif": random.choice(moons)
            }


class LevelHandler:
    def __init__(self, app):
        self.app = app
        self.win = app.win
        self.data = load_file(f"level_{0}.json", folder="levels")
        self.data_default = copy.deepcopy(self.data)
        self.level_dict_generator = LevelDictGenerator(self)

    def delete_level(self):
        # delete objects
        universe_factory.delete_universe()
        universe_factory.delete_artefacts()
        planet_factory.delete_planets()
        self.app.ship_factory.delete_ships()
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()
        for i in sprite_groups.ufos.sprites():
            i.end_object(explode=False)
        for i in sprite_groups.gif_handlers.sprites():
            i.end_object()

    def create_universe(self):
        universe_factory.amount = int(math.sqrt(math.sqrt(self.data["globals"]["width"])) * self.data["globals"][
            "universe_density"])
        universe_factory.create_universe(0, 0, self.data["globals"]["width"], self.data["globals"]["height"])
        universe_factory.create_artefacts(0, 0, self.data["globals"]["width"], self.data["globals"]["height"],
            self.data["globals"]["collectable_item_amount"])

    def generate_level_dict_from_scene(self):
        data = self.data
        # get player
        player = global_params.app.player
        data["player"]["stock"] = player.get_stock()
        data["player"]["population"] = player.population

        # get all planets
        for planet in sprite_groups.planets.sprites():
            print(f"generate_level_dict_from_scene: {data['globals']['level']}")
            if not str(planet.id) in data["celestial_objects"].keys():
                data["celestial_objects"][str(planet.id)] = self.data_default["celestial_objects"]["0"]
                print(f"generate_level_dict_from_scene key error: planet.id not in data['celestial_objects']: planet.id: {planet.id}\n keys: {data['celestial_objects'].keys()}")

            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    value_ = getattr(planet, key)
                    data["celestial_objects"][str(planet.id)][key] = value_
                else:
                    print(f"generate_level_dict_from_scene key error: {planet} has no attribute {key}\n")

        # get ship config, used if ship is created dynamically
        ship_config = load_file("ship_settings.json")

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
        print("self.data:")
        # pprint (self.data["globals"])
        self.level_dict_generator.create_suns(self.data)
        self.level_dict_generator.create_planets(self.data)
        self.level_dict_generator.create_moons(self.data)

        print("celestial_objects:")
        # print (f"identical:{self.data['celestial_objects']['0'].keys() == self.data_default['celestial_objects']['0'].keys()}")
        print(f"not in keys(): {[i for i in self.data['celestial_objects']['0'].keys() if i not in self.data_default['celestial_objects']['0'].keys()]}")
        pprint(self.data['celestial_objects'])

    def load_level(self, filename, folder):
        self.data = load_file(filename, folder=folder)
        global_params.app.level_edit.set_selector_current_value()


        # delete level
        self.delete_level()

        # reset player
        self.app.player.reset(self.data["player"])

        # create planets
        planet_factory.create_planets_from_data(self.data)

        # create ships
        ships = self.data.get("ships")
        for key in ships.keys():
            self.app.ship_factory.create_ship(f"{ships[key]['name']}_30x30.png", int(
                ships[key]["world_x"]), int(
                ships[key]["world_y"]), global_params.app, ships[key]["weapons"], data=ships[key])

        # setup level_edit
        # self.app.level_edit.data = self.data
        # self.app.level_edit.set_data_to_editor(self.level)
        # self.app.level_edit.set_selector_current_value()
        # self.app.level_edit.width = self.data.get("globals").get("width")
        # self.app.level_edit.height = self.data.get("globals").get("height")
        #
        # # create universe
        self.create_universe()

        # setup game_event_handler
        self.app.game_event_handler.level = global_params.app.level_handler.data.get("globals").get("level")
        self.app.game_event_handler.set_goal(global_params.app.level_handler.data.get("globals").get("goal"))

        # setup mission
        self.app.resource_panel.mission_icon.info_text = info_panel_text_generator.create_info_panel_mission_text()
        global_params.edit_mode = False

        self.app.calculate_global_production()

    def save_level(self, filename, folder, data):
        data = self.generate_level_dict_from_scene()
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
