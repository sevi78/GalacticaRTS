class EconomyParams:
    def __init__(self):
        # buildings,resources
        self.singleton_buildings_images = {}
        self.singleton_buildings = []

        # all possible buildings and resources
        self.resources = ["water", "energy", "food", "minerals", "technology", "population"]
        self.water_buildings = ["spring", "water treatment", "terra former"]
        self.energy_buildings = ["solar panel", "wind mill", "power plant"]
        self.food_buildings = ["farm", "ranch", "agriculture complex"]
        self.mineral_buildings = ["mine", "open pit", "mineral complex"]
        self.technology_buildings = ["university", "space harbor", "particle accelerator"]
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings = ["town", "city", "metropole"]

        self.buildings = {"water": self.water_buildings,
                          "energy": self.energy_buildings,
                          "food": self.food_buildings,
                          "minerals": self.mineral_buildings,
                          "technology": self.technology_buildings,
                          "population": self.population_buildings
                          }

        self.buildings_list = self.water_buildings + self.energy_buildings + self.food_buildings + \
                              self.mineral_buildings + self.technology_buildings + self.population_buildings

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

        # prices/production
        # self.prices = prices
        # self.production = production
