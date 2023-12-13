import math
import random

from source.factories.building_factory import building_factory
from source.multimedia_library.images import get_image_names_from_folder




class SolarSystemFactory__:
    def __init__(self, width, height, universe_density, collectable_item_amount, suns, planets, moons):
        self.width = width
        self.height = height
        self.universe_density = universe_density
        self.collectable_item_amount = collectable_item_amount
        self.suns = suns
        self.planets = planets
        self.moons = moons
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

    def initialize_data(self):
        return {
            "globals": {
                "width": self.width,
                "height": self.height,
                "universe_density": self.universe_density,
                "collectable_item_amount": self.collectable_item_amount
                },
            "celestial_objects": {}
            }

    def randomize_data(self):
        data = self.initialize_data()
        self.create_moons(data, self.create_planets(data, self.create_suns(data)))
        return data

    def create_suns(self, data):
        sun_ids = []
        sun_images = get_image_names_from_folder("suns")
        border = min(self.width, self.height) / 4

        for i in range(self.suns):
            world_x = self.get_random_position(self.width, border)
            world_y = self.get_random_position(self.height, border)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "sun", sun_images, i, world_x, world_y)
            sun_ids.append(i)

        return sun_ids

    def create_planets(self, data, sun_ids):
        planet_ids = []
        planet_images = get_image_names_from_folder("planets")
        for i in range(self.suns, self.suns + self.planets):
            orbit_object_id = random.choice(sun_ids)
            orbit_distance = self.width / len(sun_ids) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "planet", planet_images, orbit_object_id, world_x, world_y)
            planet_ids.append(i)

        return planet_ids

    def create_moons(self, data, planet_ids):
        moon_images = ["moon.gif", "moon1.gif"]#get_image_names_from_folder("moons")
        for i in range(self.suns + self.planets, self.suns + self.planets + self.moons):
            orbit_object_id = random.choice(planet_ids)
            orbit_distance = self.width / len(planet_ids) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "moon", moon_images, orbit_object_id, world_x, world_y)

    def get_random_position(self, limit, border):
        position = random.uniform(0 + border, limit - border)
        return min(max(position, 0), limit)

    def get_orbit_position(self, orbit_object, orbit_distance):
        angle = random.uniform(0, 2 * math.pi)
        world_x = orbit_object["world_x"] + orbit_distance * math.cos(angle)
        world_y = orbit_object["world_y"] + orbit_distance * math.sin(angle)
        return world_x, world_y

    def create_celestial_object__(self, i, body_type, images, orbit_object_id, world_x, world_y):
        return {
            "id": i,
            "level": 1,
            "name": "Default " + body_type,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": 110,
            "world_height": 110,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": 0.0,
            "alien_population": 0,
            "buildings_max": 8,
            "building_slot_amount": 5,
            "specials": "[]",
            "type": body_type,
            "possible_resources": self.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": "atmosphere_120.png",
            "has_atmosphere": 0,
            "orbit_angle": random.uniform(0, 360)
            }

    def randomize_planet_resources(self):
        all_possible_resources = building_factory.get_resource_categories()
        num_resources = random.randint(3, len(all_possible_resources))
        resources = random.sample(all_possible_resources, num_resources)
        return resources

    def create_celestial_object(self, i, body_type, images, orbit_object_id, world_x, world_y):
        name = self.generate_name(i, body_type, orbit_object_id)
        return {
            "id": i,
            "level": 1,
            "name": name,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": 110,
            "world_height": 110,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": 0.0,
            "alien_population": 0,
            "buildings_max": 8,
            "building_slot_amount": 5,
            "specials": "[]",
            "type": body_type,
            "possible_resources": self.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": "atmosphere_120.png",
            "has_atmosphere": 0,
            "orbit_angle": random.uniform(0, 360)
            }

    def generate_name(self, i, body_type, orbit_object_id):
        if body_type == "sun":
            return random.choice(self.solar_system_names)
        elif body_type == "planet":
            sun_name = self.solar_system_names[orbit_object_id]
            planet_number = self.to_roman(i + 1)
            return f"{sun_name} {planet_number}"
        elif body_type == "moon":
            planet_name = self.solar_system_names[orbit_object_id]
            moon_letter = chr(97 + i)  # 97 is the ASCII value for 'a'
            return f"{planet_name} {moon_letter}"

    def to_roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_num = ''
        for i in range(len(val)):
            count = int(num / val[i])
            roman_num += syb[i] * count
            num -= val[i] * count
        return roman_num



class SolarSystemFactory:
    def __init__(self, width, height, universe_density, collectable_item_amount, suns, planets, moons):
        self.width = width
        self.height = height
        self.universe_density = universe_density
        self.collectable_item_amount = collectable_item_amount
        self.suns = suns
        self.planets = planets
        self.moons = moons
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

    def initialize_data(self):
        return {
            "globals": {
                "width": self.width,
                "height": self.height,
                "universe_density": self.universe_density,
                "collectable_item_amount": self.collectable_item_amount
                },
            "celestial_objects": {}
            }

    def randomize_data_(self):
        data = self.initialize_data()
        self.create_moons(data, self.create_planets(data, self.create_suns(data)))
        return data

    def randomize_data(self):
        data = self.initialize_data()
        self.create_suns(data)
        self.create_planets(data)
        self.create_moons(data)
        return data

    def create_suns(self, data):
        sun_images = get_image_names_from_folder("suns")
        border = min(self.width, self.height) / 4

        for i in range(self.suns):
            world_x = self.get_random_position(self.width, border)
            world_y = self.get_random_position(self.height, border)
            sun_name = random.choice(self.solar_system_names)
            self.sun_names[i] = sun_name  # Store sun name in the dictionary
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "sun", sun_images, i, world_x, world_y)

    def create_planets(self, data):
        planet_ids = []
        planet_images = get_image_names_from_folder("planets")
        for i in range(self.suns, self.suns + self.planets):
            orbit_object_id = random.choice(list(self.sun_names.keys()))  # Get a random sun ID
            orbit_distance = self.width / len(self.sun_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            planet_name = f"{self.sun_names[orbit_object_id]} {self.to_roman(i - self.suns + 1)}"
            self.planet_names[i] = planet_name  # Store planet name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "planet", planet_images, orbit_object_id, world_x, world_y)

    def create_moons(self, data):
        moon_images = ["moon.gif", "moon1.gif"]#get_image_names_from_folder("moons")#
        for i in range(self.suns + self.planets, self.suns + self.planets + self.moons):
            orbit_object_id = random.choice(list(self.planet_names.keys()))  # Get a random planet ID
            orbit_distance = self.width / len(self.planet_names) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            moon_name = f"{self.planet_names[orbit_object_id]}, {chr(97 + i - self.suns - self.planets)}"
            self.moon_names[i] = moon_name  # Store moon name in the dictionary
            data["celestial_objects"][
                str(i)] = self.create_celestial_object(i, "moon", moon_images, orbit_object_id, world_x, world_y)
    def create_suns_(self, data):
        sun_ids = []
        sun_images = get_image_names_from_folder("suns")
        border = min(self.width, self.height) / 4

        for i in range(self.suns):
            world_x = self.get_random_position(self.width, border)
            world_y = self.get_random_position(self.height, border)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "sun", sun_images, i, world_x, world_y)
            sun_ids.append(i)

        return sun_ids

    def create_planets_(self, data, sun_ids):
        planet_ids = []
        planet_images = get_image_names_from_folder("planets")
        for i in range(self.suns, self.suns + self.planets):
            orbit_object_id = random.choice(sun_ids)
            orbit_distance = self.width / len(sun_ids) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "planet", planet_images, orbit_object_id, world_x, world_y)
            planet_ids.append(i)

        return planet_ids

    def create_moons_(self, data, planet_ids):
        moon_images = ["moon.gif", "moon1.gif"]#get_image_names_from_folder("moons")
        for i in range(self.suns + self.planets, self.suns + self.planets + self.moons):
            orbit_object_id = random.choice(planet_ids)
            orbit_distance = self.width / len(planet_ids) / 2
            world_x, world_y = self.get_orbit_position(data["celestial_objects"][str(orbit_object_id)], orbit_distance)
            data["celestial_objects"][str(i)] = self.create_celestial_object(i, "moon", moon_images, orbit_object_id, world_x, world_y)

    def get_random_position(self, limit, border):
        position = random.uniform(0 + border, limit - border)
        return min(max(position, 0), limit)

    def get_orbit_position(self, orbit_object, orbit_distance):
        angle = random.uniform(0, 2 * math.pi)
        world_x = orbit_object["world_x"] + orbit_distance * math.cos(angle)
        world_y = orbit_object["world_y"] + orbit_distance * math.sin(angle)
        return world_x, world_y

    def create_celestial_object__(self, i, body_type, images, orbit_object_id, world_x, world_y):
        return {
            "id": i,
            "level": 1,
            "name": "Default " + body_type,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": 110,
            "world_height": 110,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": 0.0,
            "alien_population": 0,
            "buildings_max": 8,
            "building_slot_amount": 5,
            "specials": "[]",
            "type": body_type,
            "possible_resources": self.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": "atmosphere_120.png",
            "has_atmosphere": 0,
            "orbit_angle": random.uniform(0, 360)
            }

    def randomize_planet_resources(self):
        all_possible_resources = building_factory.get_resource_categories()
        num_resources = random.randint(3, len(all_possible_resources))
        resources = random.sample(all_possible_resources, num_resources)
        return resources

    def create_celestial_object___(self, i, body_type, images, orbit_object_id, world_x, world_y):
        name = self.generate_name(i, body_type, orbit_object_id)
        return {
            "id": i,
            "level": 1,
            "name": name,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": 110,
            "world_height": 110,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": 0.0,
            "alien_population": 0,
            "buildings_max": 8,
            "building_slot_amount": 5,
            "specials": "[]",
            "type": body_type,
            "possible_resources": self.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": "atmosphere_120.png",
            "has_atmosphere": 0,
            "orbit_angle": random.uniform(0, 360)
            }

    def generate_name__(self, i, body_type, orbit_object_id):
        if body_type == "sun":
            return random.choice(self.solar_system_names)
        elif body_type == "planet":
            sun_name = self.solar_system_names[orbit_object_id]
            planet_number = self.to_roman(i + 1)
            return f"{sun_name} {planet_number}"
        elif body_type == "moon":
            planet_name = self.solar_system_names[orbit_object_id]
            moon_letter = chr(97 + i)  # 97 is the ASCII value for 'a'
            return f"{planet_name} {moon_letter}"

    def to_roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
            ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
            ]
        roman_num = ''
        for i in range(len(val)):
            count = int(num / val[i])
            roman_num += syb[i] * count
            num -= val[i] * count
        return roman_num

    def create_celestial_object(self, i, body_type, images, orbit_object_id, world_x, world_y):
        name = self.generate_name(i, body_type, orbit_object_id)

        if body_type == "sun":
            size = random.randint(90, 110)
        elif body_type == "planet":
            size = random.randint(60, 80)
        elif body_type == "moon":
            size = random.randint(30, 50)


        return {
            "id": i,
            "level": 1,
            "name": name,
            "world_x": world_x,
            "world_y": world_y,
            "world_width": size,
            "world_height": size,
            "info_text": "unknown " + body_type + ":\n\nresources: ???\nenergy: ???\n",
            "population_grow": 0.0,
            "alien_population": 0,
            "buildings_max": 8,
            "building_slot_amount": 5,
            "specials": "[]",
            "type": body_type,
            "possible_resources": self.randomize_planet_resources() if body_type != "sun" else [],
            "image_name_small": random.choice(images),
            "image_name_big": random.choice(images),
            "orbit_speed": random.uniform(0.001, 0.005) * (5 if body_type == "moon" else 1),
            "orbit_object_id": orbit_object_id,
            "orbit_distance": 0,
            "atmosphere_name": "atmosphere_120.png",
            "has_atmosphere": 0,
            "orbit_angle": random.uniform(0, 360)
            }

    def generate_name(self, i, body_type, orbit_object_id):
        if body_type == "sun":
            return self.sun_names[orbit_object_id]  # Retrieve sun name from the dictionary
        elif body_type == "planet":
            sun_name = self.sun_names[orbit_object_id]
            planet_number = self.to_roman(i - self.suns + 1)
            return f"{sun_name} {planet_number}"
        elif body_type == "moon":
            planet_name = self.planet_names[orbit_object_id]
            moon_letter = chr(97 + i - self.suns - self.planets)  # 97 is the ASCII value for 'a'
            return f"{planet_name}, {moon_letter}"
