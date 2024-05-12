import random

from source.factories.building_factory import building_factory
from source.economy.economy_handler import economy_handler
from source.configuration.game_config import config


def get_sum_up_to_n(dict, n):
    sum = 0
    for key, value in dict.items():
        if key < n:
            sum += value

    return sum


class PanZoomPlanetEconomy():  # , SpecialHandler):
    def __init__(self, kwargs):
        self.population_special = None
        self.technology_special = None
        self.minerals_special = None
        self.food_special = None
        self.energy_special = None
        self.water_special = None
        self.population_grow_factor = 0.1
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}

        self.buildings = kwargs.get("buildings", [])
        self.buildings_max = kwargs.get("buildings_max", 10)
        self.population = kwargs.get("population", 0)
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = kwargs.get("alien_population", 0)
        self.alien_attitude = kwargs.get("alien_attitude", random.randint(0, 100))

        self.building_slot_amount = kwargs.get("building_slot_amount", 3)
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0: 500, 1: 750, 2: 1250, 3: 2500, 4: 5000, 5: 25000, 6: 100000}
        self.building_slot_upgrade_energy_consumption = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 25}
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

        self.building_cue = 0
        self.specials = kwargs.get("specials", [])
        self.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "population": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0}
            }
        self.possible_resources = kwargs.get("possible_resources")

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0,
            "technology": 0
            }

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_population = self.production["population"]
        self.production_technology = self.production["technology"]

        # population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # create building slots
        self.building_buttons_energy = []
        self.building_buttons_water = []
        self.building_buttons_food = []
        self.building_buttons_minerals = []

        self.building_buttons = {
            "energy": self.building_buttons_energy,
            "food": self.building_buttons_food,
            "minerals": self.building_buttons_minerals,
            "water": self.building_buttons_water
            }
        self.building_buttons_list = self.building_buttons_energy + self.building_buttons_food + \
                                     self.building_buttons_minerals + self.building_buttons_water

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value
        if self._population < 1:
            self._population = 0

    def update_planet_resources(self, checkbox_values):
        # get new values
        resources = ["water", "energy", "food", "minerals", "technology", "population"]
        self.possible_resources = [i for i in checkbox_values if i in resources]

    def calculate_production(self):
        self.production = economy_handler.calculate_planet_production(self)
        self.production["energy"] -= get_sum_up_to_n(
                self.building_slot_upgrade_energy_consumption,
                self.building_slot_upgrades + 1)

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_technology = self.production["technology"]
        self.production_population = self.production["population"]

        self.calculate_population()
        self.set_thumpsup_status()
        self.set_smiley_status()
        self.set_technology_level_status()
        self.set_overview_images()

    def calculate_population(self):
        """ calculates population"""
        if self.production["food"] > 0:
            self.population_grow = self.population_grow_factor * self.production[
                "food"] * config.game_speed
        if self.population < 0:
            self.population = 0

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildings:
        "town":1000,  "city":10000, "metropole":100000
        """
        self.population_limit = sum([self.population_buildings_values[i] for i in self.buildings if
                                     i in self.population_buildings])

    def set_technology_upgrades(self, building):
        upgrade = building_factory.get_technology_upgrade(building)
        for key, value in upgrade.items():
            setattr(self, key, getattr(self, key) + value)

    def add_population(self):
        # check if it can grow
        if self.population_limit > self.population and self.production_food > 0:
            self.population += self.population_grow * config.game_speed
        if self.production_food < 0 and self.population > 0:
            self.population += self.production_food
