import math
import random

from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.handlers.file_handler import load_file
from source.multimedia_library.images import get_image_names_from_folder
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

        owner = random.randint(-1, config.app.level_handler.data["globals"]["players"])
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
