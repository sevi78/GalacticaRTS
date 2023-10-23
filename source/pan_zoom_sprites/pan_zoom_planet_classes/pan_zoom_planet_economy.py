import pygame

from source.app.app_helper import get_sum_up_to_n

from source.game_play.building_factory import building_factory
from source.utils import global_params
from source.multimedia_library.images import get_image


class PanZoomPlanetEconomy:
    def __init__(self, kwargs):
        # self.technology_upgrades = {"university": {"buildings_max": 3}}
        self.population_grow_factor = 0.1
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}

        self.buildings = []
        self.buildings_max = kwargs.get("buildings_max", 10)
        self.population = 0.0
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = kwargs.get("alien_population", 0)

        self.building_slot_amount = kwargs.get("building_slot_amount", 3)
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0: 500, 1: 750, 2: 1250, 3: 2500, 4: 5000, 5: 25000, 6: 100000}
        self.building_slot_upgrade_energy_consumption = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 25}
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

        self.building_cue = 0
        self.specials = kwargs.get("specials", [])

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

    def update_planet_resources(self, checkbox_values):
        # get new values
        resources = ["water", "energy", "food", "minerals", "technology", "city"]
        self.possible_resources = [i for i in checkbox_values if i in resources]
        self.building_button_widget.show()

    def set_thumpsup_status(self):

        # is everything in plus, show thumpsup green,otherwise red, set smiley to sad if no food production
        vl = []
        for key, value in self.production.items():
            if value < 0:
                vl.append(value)
        if len(vl) > 0:
            self.thumpsup_status = True
        else:
            self.thumpsup_status = False

    def set_smiley_status(self):

        if self.production["food"] > 0:
            self.smiley_status = True
        else:
            self.smiley_status = False

    def calculate_production(self):
        """
        calculates the production, sets the overview icons (smiley, thumpsup) for display the condition of the planet
        """
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "city": 0
            }

        for i in self.buildings:
            # print("get_production_from_buildings_json(i)", building_factory.get_production_from_buildings_json(i))
            for key, value in building_factory.get_production_from_buildings_json(i).items():
                self.production[key] += value

        self.production[
            "energy"] -= get_sum_up_to_n(self.building_slot_upgrade_energy_consumption, self.building_slot_upgrades + 1)
        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_technology = self.production["technology"]
        self.production_city = self.production["city"]

        self.calculate_population()
        self.set_thumpsup_status()
        self.set_smiley_status()
        self.set_overview_images()

    def set_overview_images(self):
        if self.thumpsup_status:
            self.thumpsup_button.image_raw = pygame.transform.flip(pygame.transform.scale(
                get_image(
                    "thumps_upred.png"), self.thumpsup_button_size), True, True)
        else:
            self.thumpsup_button.image_raw = pygame.transform.flip(pygame.transform.scale(
                get_image(
                    "thumps_up.png"), self.thumpsup_button_size), True, False)
        if self.smiley_status:
            self.smiley_button.image_raw = get_image("smile.png")
        else:
            self.smiley_button.image_raw = get_image("sad.png")

    def calculate_population(self):
        """ calculates population"""
        if self.production["food"] > 0:
            self.population_grow = self.population_grow_factor * self.production[
                "food"] * global_params.time_factor

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
        if self.population_limit > self.population and self.production_food > 0:
            self.population += self.population_grow * global_params.game_speed
        if self.production_food < 0 and self.population > 0:
            self.population += self.production_food
