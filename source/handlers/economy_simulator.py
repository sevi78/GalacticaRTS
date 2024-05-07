import random
from pprint import pprint
import pygame.event
from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file


class EconomySimulator:
    def __init__(self):
        self.buildings = load_file("buildings.json", "config")
        self.all_building_names = building_factory.get_all_building_names()
        self.stock = {
            'energy': 1000,
            'food': 1000,
            'minerals': 1000,
            'water': 1000,
            'technology': 1000,
            'population': 1000
            }
        self.production = {
            'energy': 0,
            'food': 0,
            'minerals': 0,
            'water': 0,
            'technology': 0,
            'population': 0
            }
        self.population = 0
        self.cycle_count = 0

        # this is the generated list of buildings to use 
        self.building_plan = []
        self.simulations = {
            0: {
                "cycle_count": self.cycle_count,
                "production": self.production,
                "building_plan": self.building_plan,
                "population": self.population
                }
            }

    def __str__(self):
        return f"EconomySimulator:\n stock: {self.stock}\n self.production:{self.production}\n, building_plan: {self.building_plan}\n,population: {self.population}\n Cycle Count: {self.cycle_count}\n EconomySimulator:\n simulations: {self.simulations}\n"

    def reset_stock(self):
        self.stock = {
            'energy': 1000,
            'food': 1000,
            'minerals': 1000,
            'water': 1000,
            'technology': 1000,
            'population': 1000
            }

    def reset_production(self):
        self.production = {
            'energy': 0,
            'food': 0,
            'minerals': 0,
            'water': 0,
            'technology': 0,
            'population': 0
            }

    def reset(self):
        self.reset_stock()
        self.reset_production()
        self.building_plan = []
        self.cycle_count = 0
        self.population = 0

    def add_building(self, building):
        self.building_plan.append(building)

    def calculate_population(self):
        if self.production["food"] > 0:
            if "town" or "city" or "metropole" in self.building_plan:
                self.population += self.production["food"] * 1

    def calculate_stock(self):
        for key, value in self.production.items():
            self.stock[key] += value

    def calculate_production(self):
        self.reset_production()
        # Calculate production from buildings
        for i in self.building_plan:
            self.production = building_factory.add_production(self.production, building_factory.get_production_from_buildings_json(i))

    def get_building_fit_to_population(self):
        fit_buildings = []

        all = self.all_building_names
        limit_1000 = building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(1000)
        limit_10000 = building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(10000)

        weapons = building_factory.get_building_names("weapons")
        planetary_defence = building_factory.get_building_names("planetary_defence")
        ships = building_factory.get_building_names("ship")

        ignoreable = list(weapons) + list(planetary_defence) + list(ships)

        if self.population in range(0, 999):
            fit_buildings = [i for i in all if i not in ignoreable and i not in limit_1000 and i not in limit_10000]

        elif self.population in range(1000, 9999):
            fit_buildings = [i for i in all if i not in ignoreable and i not in limit_10000]

        else:
            fit_buildings = [i for i in all if i not in ignoreable]

        return fit_buildings

    def run_economy(self):
        self.cycle_count += 1
        building = random.choice(self.get_building_fit_to_population())
        if building in ["town", "city", "metropole"]:
            if self.population in range(0, 999):
                building = "town"
            elif self.population in range(1000, 9999):
                building = "city"
            else:
                building = "metropole"

        self.add_building(building)
        self.calculate_stock()
        self.calculate_production()
        self.calculate_population()

        # check if ruined
        ruined = False
        for key, value in self.stock.items():
            if value < 0:
                ruined = True

        # store simulation
        if ruined:
            self.simulations[self.cycle_count] = {
                "cycle_count": self.cycle_count,
                "production": self.production,
                "building_plan": self.building_plan,
                "stock": self.stock,
                "population": self.population
                }
            # reset
            self.reset()

        if self.population > 1000:
            self.simulations[self.cycle_count] = {
                "cycle_count": self.cycle_count,
                "production": self.production,
                "building_plan": self.building_plan,
                "stock": self.stock,
                "population": self.population
                }
            # reset
            self.reset()


def main():
    simulator = EconomySimulator()
    run = True
    while run:
        space = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True
            if event.type == pygame.KEYUP:
                space = False

        if space:
            pprint(simulator.simulations)

        simulator.run_economy()


if __name__ == "__main__":
    main()
