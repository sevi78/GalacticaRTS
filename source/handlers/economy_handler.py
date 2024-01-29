import random
from pprint import pprint

from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class EconomyHandler:
    def __init__(self):
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0,
            "technology": 0
            }
        self.planet_production = {}
        self.planet_buildings = {}
        self.all_buildings = []

    def set_planet_buildings(self):
        self.planet_buildings = {}
        self.all_buildings = []
        for i in sprite_groups.planets.sprites():
            self.planet_buildings[str(i.id)] = {"buildings": i.buildings, "specials": i.specials}
            self.all_buildings.append(i.buildings)

        self.all_buildings = [item for sublist in self.all_buildings for item in sublist]

    def setup_planet_specials_dict(self, planet):
        planet.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "population": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0},
            "buildings_max": {"operator": "", "value": 0}
            }
        for special in planet.specials:
            special_key, operator, special_value = special.split()
            special_value = float(special_value)
            planet.specials_dict[special_key]["operator"] = operator
            planet.specials_dict[special_key]["value"] += special_value

        #pprint (f"setup_planet_specials_dict:{planet}: {planet.specials_dict}")
        return planet.specials_dict

    def calculate_planet_production(self, planet):
        planet.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0,
            "technology": 0
            }

        # Calculate production from buildings
        for i in planet.buildings:
            for key, value in building_factory.get_production_from_buildings_json(i).items():
                planet.production[key] += value

        special_key = ""
        special_value = 1

        # Apply specials if they exist
        if hasattr(planet, 'specials') and planet.specials:
            for index, special in enumerate(planet.specials):
                special_key, operator, special_value = special.split()
                special_value = float(special_value)
                if special_key in planet.production:
                    if operator == "*":
                        if planet.production[special_key] > 0:
                            planet.production[special_key] *= special_value
                    elif operator == "+":
                        if planet.production[special_key] > 0:
                            planet.production[special_key] += special_value
                else:
                    # set the value to the planet
                    if not special_key == "population_grow_factor":
                        setattr(planet, special_key, eval(f"{getattr(planet, special_key)}{operator}{special_value}"))
                        # delete special to make sure it is only applied once
                        planet.specials.pop(index)
                    else:
                        pass


        return planet.production

    def randomize_planet_resources(self):
        all_possible_resources = building_factory.get_resource_categories()
        num_resources = random.randint(3, len(all_possible_resources))
        resources = random.sample(all_possible_resources, num_resources)
        return resources

    def update(self):
        self.set_planet_buildings()
        for planet in sprite_groups.planets.sprites():
            self.calculate_planet_production(planet)
            self.setup_planet_specials_dict(planet)


economy_handler = EconomyHandler()
