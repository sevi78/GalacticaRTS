import random

import pygame

from source.app.app_helper import get_sum_up_to_n

from source.factories.building_factory import building_factory
from source.game_play.ranking import Rank
from source.handlers.economy_handler import economy_handler
from source.utils import global_params
from source.multimedia_library.images import get_image


class SpecialHandler:
    def __init__(self):
        pass

    def set_specials_icons(self, key, value):
        if hasattr(self, key):
            print("set_specials_icons:", key, value)

    def get_special_string(self, key):
        # Specials
        specials = eval(self.specials)

        for special in specials:
            key, operand, value = special.split(" ")
            value = float(value)  # Convert the value to a float for arithmetic operations


class PanZoomPlanetEconomy(Rank, SpecialHandler):
    def __init__(self, kwargs):
        Rank.__init__(self)
        SpecialHandler.__init__(self)
        self.city_special = None
        self.technology_special = None
        self.minerals_special = None
        self.food_special = None
        self.energy_special = None
        self.water_special = None
        self.population_grow_factor = 0.1
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}

        self.buildings = []
        self.buildings_max = kwargs.get("buildings_max", 10)
        self.population = 0.0
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
            "city": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0}
            }
        self.possible_resources = kwargs.get("possible_resources")

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "city": 0,
            "technology": 0
            }

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_city = self.production["city"]
        self.production_technology = self.production["technology"]

        # population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # create building slots
        self.building_buttons_energy = []
        self.building_buttons_water = []
        self.building_buttons_food = []
        self.building_buttons_minerals = []

        self.building_buttons = {"energy": self.building_buttons_energy,
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
        resources = ["water", "energy", "food", "minerals", "technology", "city"]
        self.possible_resources = [i for i in checkbox_values if i in resources]
        # self.building_button_widget.show()

    def calculate_production(self):
        # """
        # calculates the production, sets the overview icons (smiley, thumpsup) for display the condition of the planet
        # """
        # self.production = {
        #     "energy": 0,
        #     "food": 0,
        #     "minerals": 0,
        #     "water": 0,
        #     "technology": 0,
        #     "city": 0
        #     }
        # # buildings
        # for i in self.buildings:
        #     # print("get_production_from_buildings_json(i)", building_factory.get_production_from_buildings_json(i))
        #     for key, value in building_factory.get_production_from_buildings_json(i).items():
        #         self.production[key] += value
        # print ("self.production", self.production)
        # #self.production["food"] = 5
        # print("self.production", self.production)
        #
        # # # specials
        # specials = eval(self.specials)
        # for i in specials:
        #     key = i.split(" ")[0]
        #     operand = i.split(" ")[1]
        #     value = i.split(" ")[2]
        #     if key in self.production.keys():
        #         prod = self.production[key]
        #         prod_new = prod * float(value)
        #         print ("prod", prod, prod_new, value)
        #         self.production[key] = prod_new
        #     #setattr(self, getattr(self, key), exec(f"{getattr(self, key)} {operand} {value}"))
        #     #print(f"self.specials: {self.specials}")
        #     #print (i.split(" "))
        #
        # print("self.production_new", self.production)
        # print (self.production_food)
        # self.calculate_specials_production()

        # Convert the string representation of specials to a dictionary
        # specials = eval(self.specials)
        # for i in specials:
        #     key = i.split(" ")[0]
        #     operand = i.split(" ")[1]
        #     value = i.split(" ")[2]
        #     if key in self.production.keys():
        #         # Include the special in the calculation of self.production
        #         self.production[key] = eval(f"self.production[key] {operand} {value}")
        #     else:
        #         # If the key is not in self.production, add it with the calculated value
        #         setattr(self, key, eval(f"{getattr(self, key)} {operand} {value}"))

        # Print the updated self.production
        # print("self.production", self.specials)
        #
        # self.water_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('water')])
        # self.energy_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('energy')])
        # self.food_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('food')])
        # self.minerals_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('minerals')])
        # self.technology_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('technology')])
        # self.city_special = sum([float(entry.split(' * ')[1]) for entry in self.specials if entry.startswith('city')])

        self.production = economy_handler.calculate_planet_production(self)
        # Calculate the sum only if the list is not empty, otherwise return 1
        self.water_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('water')]) if self.water_special else 1
        self.energy_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('energy')]) if self.energy_special else 1
        self.food_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('food')]) if self.food_special else 1
        self.minerals_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('minerals')]) if self.minerals_special else 1
        self.technology_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('technology')]) if self.technology_special else 1
        self.city_special = 1  # sum([float(entry.split(' * ')[1]) for entry in self.specials if
        # entry.startswith('city')]) if self.city_special else 1

        #
        # print ("specials:",self.water_special, self.energy_special, self.food_special, self.minerals_special, self.technology_special, self.city_special )
        # specials = eval(self.specials)
        # for i in specials:
        #     key = i.split(" ")[0]
        #     operand = i.split(" ")[1]
        #     value = i.split(" ")[2]
        #
        #     if hasattr(self, key + "_special"):
        #         attr = getattr(self, key + "_special")
        #
        #         setattr(self, key + "_special", attr + eval(value))
        #         print ("", attr, attr + eval(value), getattr(self, key + "_special"))
        self.production[
            "energy"] -= get_sum_up_to_n(self.building_slot_upgrade_energy_consumption, self.building_slot_upgrades + 1)

        self.production_water = self.production["water"] * self.water_special
        self.production_energy = self.production["energy"] * self.energy_special
        self.production_food = self.production["food"] * self.food_special
        self.production_minerals = self.production["minerals"] * self.minerals_special
        self.production_technology = self.production["technology"] * self.technology_special
        self.production_city = self.production["city"] * self.city_special

        # print (self.production_food)

        self.calculate_population()
        self.set_thumpsup_status()
        self.set_smiley_status()
        self.set_technology_level_status()
        self.set_overview_images()

    def calculate_population(self):
        """ calculates population"""
        if self.production["food"] > 0:
            self.population_grow = self.population_grow_factor * self.production[
                "food"] * global_params.time_factor
        if self.population < 0:
            self.population = 0

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildongs:
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
            self.population += self.population_grow * global_params.game_speed
        if self.production_food < 0 and self.population > 0:
            self.population += self.production_food
