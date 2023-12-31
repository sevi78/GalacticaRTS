from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class EconomyHandler:
    def __init__(self):
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "city": 0,
            "technology": 0
            }
        self.planet_production = {}
        self.planet_buildings = {}
        self.all_buildings = []

    def set_planet_buildings(self):
        self.planet_buildings = {}
        self.all_buildings = []
        for i in sprite_groups.planets.sprites():
            # self.planet_buildings[str(i.id)] = []
            self.planet_buildings[str(i.id)] = {"buildings": i.buildings, "specials": i.specials}
            self.all_buildings.append(i.buildings)

        self.all_buildings = [item for sublist in self.all_buildings for item in sublist]
        # print (f"EconomyHandler.set_planet_buildings: {self.planet_buildings}\nall: {list(self.all_buildings)}")

    def setup_planet_specials_dict(self, planet):
        planet.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "city": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0}
            }
        for special in planet.specials:
            special_key, operator, special_value = special.split()
            special_value = float(special_value)
            planet.specials_dict[special_key]["operator"] = operator
            planet.specials_dict[special_key]["value"] += special_value

        # print (f"setup_planet_specials_dict:{planet}: {planet.specials_dict}")
        return planet.specials_dict

    def calculate_planet_production(self, planet):
        planet.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "city": 0,
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
            for special in planet.specials:
                special_key, operator, special_value = special.split()
                special_value = float(special_value)
                if special_key in planet.production:
                    if operator == "*":
                        if planet.production[special_key] > 0:
                            planet.production[special_key] *= special_value
                    elif operator == "+":
                        if planet.production[special_key] > 0:
                            planet.production[special_key] += special_value
                # print(f"calculate_planet_production: name: {planet.name} {planet.production}  {special_key}: {special_value}")

        return planet.production

    def update(self):
        self.set_planet_buildings()
        for planet in sprite_groups.planets.sprites():
            self.calculate_planet_production(planet)
            self.setup_planet_specials_dict(planet)


economy_handler = EconomyHandler()
