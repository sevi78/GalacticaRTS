from source.configuration.config import *


class Building:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name

        # production
        self.production_energy = 0
        self.production_food = 0
        self.production_minerals = 0
        self.production_water = 0
        self.production_technology = 0
        self.production_city = 0

        # prices
        self.price_energy = 0
        self.price_food = 0
        self.price_minerals = 0
        self.price_water = 0
        self.price_technology = 0
        self.price_city = 0

        # others
        self.build_population_minimum = 0
        self.building_production_time_scale = 5
        self.building_production_time = 0

        # register
        self.parent.add(self.name, self)

    def get_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if not key == "parent":
                d[key] = value
        return d


class Buildings:
    def __init__(self):
        self.buildings = {}
        self.create_buildings()
        self.fill_buildings()

    def create_buildings(self):
        for building_name, dict in production.items():
            building = Building(building_name, self)

    def fill_buildings(self):

        for building_name, building in self.buildings.items():
            building.production_energy = production[building_name]["energy"]
            building.production_food = production[building_name]["food"]
            building.production_minerals = production[building_name]["minerals"]
            building.production_water = production[building_name]["water"]
            building.production_technology = production[building_name]["technology"]
            building.production_city = production[building_name]["city"]

            # prices
            building.price_energy = prices[building_name]["energy"]
            building.price_food = prices[building_name]["food"]
            building.price_minerals = prices[building_name]["minerals"]
            building.price_water = prices[building_name]["water"]

            # others
            building.build_population_minimum = build_population_minimum[building_name]
            building.building_production_time_scale = building_production_time_scale
            building.building_production_time = building_production_time[building_name]

    def add(self, key, value):
        self.buildings[key] = value

    def get_building(self, key):
        return self.buildings[key]


buildings = Buildings()
