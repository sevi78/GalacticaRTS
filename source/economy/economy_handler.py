import random

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.math.math_handler import get_sum_up_to_n


class EconomyHandler:
    def __init__(self):
        self.player = None
        self.population_limit = 0
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0,
            "technology": 0
            }

        # self.production_water = self.production["water"]
        # self.production_energy = self.production["energy"]
        # self.production_food = self.production["food"]
        # self.production_minerals = self.production["minerals"]
        # self.production_technology = self.production["technology"]
        self.planet_production = {}
        self.planet_buildings = {}
        self.all_buildings = []

    def set_planet_buildings(self):
        self.planet_buildings = {}
        self.all_buildings = []
        for i in sprite_groups.planets.sprites():
            self.planet_buildings[
                str(i.id)] = {"buildings": i.economy_agent.buildings, "specials": i.economy_agent.specials}
            self.all_buildings.append(i.economy_agent.buildings)

        self.all_buildings = [item for sublist in self.all_buildings for item in sublist]

    def setup_planet_specials_dict(self, planet):
        planet.economy_agent.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "population": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0},
            "buildings_max": {"operator": "", "value": 0}
            }

        for special in planet.economy_agent.specials:
            special_key, operator, special_value = special.split()
            special_value = float(special_value)
            planet.economy_agent.specials_dict[special_key]["operator"] = operator
            planet.economy_agent.specials_dict[special_key]["value"] += special_value

        # pprint (f"setup_planet_specials_dict:{planet}: {planet.specials_dict}")
        return planet.economy_agent.specials_dict

    def calculate_planet_production(self, economy_agent):
        economy_agent.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0,
            "technology": 0
            }

        # Calculate production from buildings
        for i in economy_agent.buildings:
            for key, value in building_factory.get_production_from_buildings_json(i).items():
                economy_agent.production[key] += value

        special_key = ""
        special_value = 1

        # Apply specials if they exist
        if hasattr(economy_agent, 'specials') and economy_agent.specials:
            for index, special in enumerate(economy_agent.specials):
                special_key, operator, special_value = special.split()
                special_value = float(special_value)
                if special_key in economy_agent.production:
                    if operator == "*":
                        if economy_agent.production[special_key] > 0:
                            economy_agent.production[special_key] *= special_value
                    elif operator == "+":
                        if economy_agent.production[special_key] > 0:
                            economy_agent.production[special_key] += special_value
                else:
                    # set the value to the planet
                    if not special_key == "population_grow_factor":
                        setattr(economy_agent, special_key, eval(f"{getattr(economy_agent, special_key)}{operator}{special_value}"))
                        # delete special to make sure it is only applied once
                        economy_agent.specials.pop(index)
                    else:
                        pass

        return economy_agent.production

    def calculate_global_production(self, player):
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        self.population_limit = 0

        for planet in sprite_groups.planets:
            if planet.owner == player.owner:
                planet.economy_agent.calculate_production()
                planet.economy_agent.add_population()

                # set population limits
                self.population_limit += planet.economy_agent.population_limit
                for key, value in planet.economy_agent.production.items():
                    # self.production[key] += getattr(planet, "production_" + key)
                    self.production[key] += planet.economy_agent.production[key]
                # subtract the building_slot_upgrades ( they cost 1 energy)
                self.production[
                    "energy"] -= get_sum_up_to_n(planet.economy_agent.building_slot_upgrade_energy_consumption,
                        planet.economy_agent.building_slot_upgrades + 1)

        player.population_limit = self.population_limit
        player.production = self.production

    def randomize_planet_resources(self):
        all_possible_resources = building_factory.get_resource_categories()
        num_resources = random.randint(3, len(all_possible_resources))
        resources = random.sample(all_possible_resources, num_resources)
        return resources

    def update(self):
        self.set_planet_buildings()
        for planet in sprite_groups.planets.sprites():
            self.calculate_planet_production(planet.economy_agent)
            self.setup_planet_specials_dict(planet)
            # planet.economy_agent.update()

        for key, value in config.app.players.items():
            economy_handler.calculate_global_production(value)


economy_handler = EconomyHandler()
