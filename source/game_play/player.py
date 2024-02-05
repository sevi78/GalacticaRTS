import time

import pygame

from source.configuration import global_params
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class Player:
    """
    this holds the players values like population, production, population_limit:
    Main functionalities:
    The Player class holds the values of a player in a game, such as population, production, and population limit. It also has methods to update the player's values, set the population limit, and produce resources.

    Methods:
    - __init__: initializes the player's values and sets the clock, wait time, and game start time.
    - get_stock: returns a dictionary of the player's current stock of resources.
    - set_population_limit: calculates and sets the player's population limit based on their buildings.
    - produce: updates the player's resources based on their production values.
    - update: updates the player's clock and wait time based on the game speed.

    Fields:
    - population: the player's current number of cities.
    - technology: the player's current level of technology.
    - water: the player's current amount of water resources.
    - minerals: the player's current amount of mineral resources.
    - food: the player's current amount of food resources.
    - energy: the player's current amount of energy resources.
    - clock_: the player's current clock time.
    - start_wait: the initial wait time for resource production.
    - wait: the current wait time for resource production.
    - start_time: the time when the wait time started.
    - game_start_time: the time when the game started.
    - production: a dictionary of the player's production values for each resource.
    - stock: a dictionary of the player's current stock of resources.
    - population: the player's current population.
    - population_limit: the maximum population the player can have based on their buildings.
    """

    def __init__(self, **kwargs):
        # self.population = kwargs.get("population", 0)
        # self.technology = kwargs.get("technology", 0)
        # self.water = kwargs.get("water", 0)
        # self.minerals = kwargs.get("minerals", 0)
        # self.food = kwargs.get("food", 0)
        # self.energy = kwargs.get("energy", 0)


        for key, value in kwargs.items():
            setattr(self, key, value)
        for key, value in self.stock.items():
            setattr(self, key, value)

        self.clock_ = 2367
        self.start_wait = kwargs.get("wait", 5.0)
        self.wait = kwargs.get("wait", 5.0)
        self.start_time = time.time()
        self.game_start_time = time.time()

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        #self.stock = None
        #self.get_stock()
        #self.population = self.stock["population"]
        self.population_limit = 0

    def reset(self, data):
        # self.__init__(
        #     name="zork",
        #     color=pygame.Color('red'),
        #     energy=data["stock"]["energy"],
        #     food=data["stock"]["food"],
        #     minerals=data["stock"]["minerals"],
        #     water=data["stock"]["water"],
        #     technology=data["stock"]["technology"],
        #     population=data["stock"]["population"],
        #     clock=0,
        #
        #     )
        self.__init__(
            name="zork",
            color=pygame.Color('red'),
            stock=data["stock"],
            clock=0,

            )

    def get_stock(self):
        stock = {"energy": self.energy,
                      "food": self.food,
                      "minerals": self.minerals,
                      "water": self.water,
                      "technology": self.technology,
                      "population": self.population
                      }
        return stock

    def get_all_buildings(self):
        buildings = []
        for i in sprite_groups.planets:
            buildings += i.buildings
        return buildings

    def set_population_limit(self):
        population_buildings = ["town", "city", "metropole"]
        population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        self.population_limit = sum([population_buildings_values[i] for i in self.buildings if
                                     i in population_buildings])

    def produce(self):
        current_time = time.time()
        if current_time > self.start_time + self.wait:
            self.start_time = current_time
            self.energy += self.production["energy"]
            self.food += self.production["food"]
            self.minerals += self.production["minerals"]
            self.water += self.production["water"]
            self.technology += self.production["technology"]
            self.population += self.production["population"]
            #print (f"population:{self.population}, population: {self.population}, self.stock: {self.stock}")

    def update(self):
        if global_params.game_speed == 0:
            return

        self.clock_ += 0.01 * global_params.game_speed
        self.clock = "Year: " + str(int(self.clock_))
        self.wait = self.start_wait / global_params.game_speed
        self.produce()
        # set global population

        self.population = int(sum([i.population for i in sprite_groups.planets]))

        # problem: this overwrites the population of player if set from data. but it also makes no sense to have any population if no planets has population.
        # solution: set population to the planets NOT to player itself!!!
