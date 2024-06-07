import random
import sys
from pprint import pprint

import pygame.event

from source.factories.building_factory import building_factory
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet_economy import PanZoomPlanetEconomy


class BuildPlan:
    def __init__(self):
        self.plan_default = {key: 0 for key in building_factory.get_all_building_names()}
        self.plans = {
            "stable_1000": {
                'agriculture complex': 0,
                'cannon': 0,
                'cargoloader': 0,
                'city': 0,
                'electro magnetic impulse': 0,
                'energy blast': 0,
                'farm': 5,
                'laser': 0,
                'metropole': 0,
                'mine': 2,
                'mineral complex': 0,
                'missile': 0,
                'open pit': 0,
                'particle accelerator': 0,
                'phaser': 0,
                'power plant': 0,
                'ranch': 0,
                'rescue drone': 0,
                'rocket': 0,
                'solar panel': 2,
                'space harbor': 0,
                'spacehunter': 0,
                'spaceship': 0,
                'spacestation': 0,
                'spring': 3,
                'terra former': 0,
                'town': 1,
                'university': 0,
                'water treatment': 0,
                'wind mill': 0,
                'worm hole': 0
                },
            "stable_10000": {
                'agriculture complex': 0,
                'cannon': 0,
                'cargoloader': 0,
                'city': 1,
                'electro magnetic impulse': 0,
                'energy blast': 0,
                'farm': 0,
                'laser': 0,
                'metropole': 0,
                'mine': 0,
                'mineral complex': 0,
                'missile': 0,
                'open pit': 1,
                'particle accelerator': 0,
                'phaser': 0,
                'power plant': 0,
                'ranch': 4,
                'rescue drone': 0,
                'rocket': 0,
                'solar panel': 0,
                'space harbor': 0,
                'spacehunter': 0,
                'spaceship': 0,
                'spacestation': 0,
                'spring': 0,
                'terra former': 0,
                'town': 0,
                'university': 0,
                'water treatment': 2,
                'wind mill': 3,
                'worm hole': 0
                }
            }

    def get_plan(self, plan_name: str) -> dict:
        """ return a dict from the plan_name"""
        return self.plans[plan_name]

    def get_buildings_list_from_plan_name(self, plan_name: str) -> list:
        """returns a list from plan_name"""
        return self.convert_plan_to_list(self.plans[plan_name])

    def get_fitting_buildplan(self, population: int) -> list:
        if population in range(0, 999):
            return self.get_buildings_list_from_plan_name("stable_1000")
        if population in range(1000, 10000):
            return self.get_buildings_list_from_plan_name("stable_10000")

    def calc_production(self, buildings: [dict, list]) -> [dict, None]:
        """ returns a dict of the production based on buildings:
            buildings can either be a plan(dict) or a buildings_list(list)
        """
        if buildings.__class__ is list:
            buildings_dict = self.convert_list_to_plan(buildings)
        elif buildings.__class__ is dict:
            buildings_dict = buildings
        else:
            print("buildings must be either list or dict ! ")
            return None

        d = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        for key, value in buildings_dict.items():
            for i in range(value):
                for resource_key in d.keys():
                    production = building_factory.get_production_from_buildings_json(key)[resource_key]
                    d[resource_key] += production
        return d

    def convert_plan_to_list(self, plan: dict) -> list:
        buildings_list = []
        for key, value in plan.items():
            for i in range(value):
                buildings_list.append(key)

        return buildings_list

    def convert_list_to_plan(self, buildings_list: list) -> dict:
        plan = {key: 0 for key in building_factory.get_all_building_names()}
        for i in buildings_list:
            plan[i] += 1
        return plan


build_plan = BuildPlan()


class EconomyAgent(PanZoomPlanetEconomy):
    def __init__(self, **kwargs):
        PanZoomPlanetEconomy.__init__(self, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.production_score = {}
        self.production_score_average = 0

    def __str__(self):
        # return f"Eco agent: {self.production}, population: {self.population}, score:{self.production_score}, sCore_average: {self.production_score_average}"
        return f"Eco agent:  sCore_average: {self.production_score_average}"




class EconomySimulator:
    def __init__(self):
        self.resource_goal = {}
        self.simulation_cycles = {}
        self.agents = []
        self.agents = [EconomyAgent(population=100, id=len(self.agents)) for i in range(1)]
        self.cycles = 0
        self.production_goal = {
            "energy": 1,
            "food": 1,
            "minerals": 1,
            "water": 1,
            "technology": 1,
            "population": 0
            }

    def set_random_building(self, agent):
        building = random.choice(building_factory.get_all_building_names())
        agent.buildings.append(building)
        agent.calculate_production()
        agent.add_population()

    def run_simulation_(self):
        for i in self.agents:
            self.set_random_building(i)
            i.calculate_production()
            i.population += (i.production["food"] if i.production["food"] > 0 else 0 and any(["town", "city",
                                                                                              "metropole"]) in i.possible_resources) / 100
            self.calculate_production_score(i)

        self.simulation_cycles[self.cycles] = self.agents

        print(str(self.simulation_cycles[0][0]))

    def calculate_score(self, building:str, current_dict:dict, goal_dict:dict, population:int, key:str)->float:
        """ returns a float of the score for the building based on:
        - building:     str representing the building
        - current_dict: dict representing production or prize
        - goal_dict:    dict representing production or prize to achieve
        - population:   int representing the population
        - key:          str representing either 'production' or 'prizes'
        """
        assert key in ["production", "prices"], print ("key must be either 'production' or 'prices'!")

        building_dict = getattr(building_factory, f"get_{key}_from_buildings_json({building})")()

        # calculate new_production
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            new_dict[key] = value + current_dict[key]

        scores = {
            key: (goal_dict[key] - new_dict[key]) / len(goal_dict.keys()) for key in
            goal_dict.keys()}

        scores = {
            key: abs(goal_dict[key] - new_dict[key]) for key in
            goal_dict.keys()}

        sum_ = 0
        for key, value in scores.items():
            sum_ += value

        # print (f"building : {building}, production_score: {production_score}, sum_ {sum_}")
        # ensure only producing buildings are valid
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +100
        if all(value == 0 for value in building_dict.values()):
            sum_ = +100
        return sum_

    def calculate_production_score(self, building, current_production, goal_production, population):
        # get production of the building
        building_production = building_factory.get_production_from_buildings_json(building)

        # calculate new_production
        new_production = {}
        # add both, current_production and building_production
        # this will be the production if the building is built
        for key, value in building_production.items():
            new_production[key] = value + current_production[key]

        # print (f"building: {building},current_production:{current_production},building_production: {building_production},  new_production: {new_production}")

        production_score = {
            key: (goal_production[key] - new_production[key]) / len(goal_production.keys()) for key in goal_production.keys()}

        production_score = {
            key: abs(goal_production[key] - new_production[key]) for key in
            goal_production.keys()}

        sum_ = 0
        for key, value in production_score.items():
            sum_ += value

        # print (f"building : {building}, production_score: {production_score}, sum_ {sum_}")
        # ensure only producing buildings are valid
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +100
        if all(value == 0 for value in building_production.values()):
            sum_ = +100
        return sum_

    def calculate_resource_score(self, building, current_resources, goal_resources, population):
        # get building_resources
        building_resources = building_factory.get_prices_from_buildings_json(building)

        # calculate new_resources
        new_production = {}
        # add both, current_resources and building_resources
        # this will be the production if the building is built
        for key, value in building_resources.items():
            new_production[key] = value + current_resources[key]

        resources_score = {
            key: (goal_resources[key] - new_production[key]) / len(goal_resources.keys()) for key in
            goal_resources.keys()}

        production_score = {
            key: abs(goal_resources[key] - new_production[key]) for key in
            goal_resources.keys()}

        sum_ = 0
        for key, value in production_score.items():
            sum_ += value

        # print (f"building : {building}, production_score: {production_score}, sum_ {sum_}")
        # ensure only costly buildings are valid
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +100
        if all(value == 0 for value in building_resources.values()):
            sum_ = +100
        return sum_


    def get_best_fitting_buildings_to_goal__(self)->list:
        # get building scores for every building
        production = {
            "energy": -2,
            "food": -1,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        self.production_goal = {
            "energy": 1,
            "food": 1,
            "minerals": 1,
            "water": 1 ,
            "technology": 1,
            "population": 0
            }
        # setup building_scores dict
        building_scores = {}
        for i in building_factory.get_all_building_names():
            building_scores[i] = self.calculate_production_score(
                    building=i,
                    current_production=production,
                    goal_production=self.production_goal,
                    population=100)

        # find the highest value in buildings_score
        max_value = max(building_scores.values())
        min_value = min(building_scores.values())

        # get the most/lowest valued buildings
        max_value_list = []
        min_value_list = []
        for key, value in building_scores.items():
            if value == max_value:
                max_value_list.append(key)

            if value == min_value:
                min_value_list.append(key)

        # pprint(building_scores)

        # best buildings = min_value_list
        best_fitting_buildings = min_value_list
        # print(f"min_value_list:{min_value_list}")
        # print (f"max_value_list:{max_value_list}")
        return best_fitting_buildings

    def get_best_fitting_buildings_to_goals(self,production, resources, population,  production_goal, resource_goal)->list:
        # setup building_scores dict

        # production
        production_scores = {}
        for i in building_factory.get_all_building_names():
            production_scores[i] = self.calculate_production_score(
                    building=i,
                    current_production=production,
                    goal_production=self.production_goal,
                    population=population)

        # find the highest value in buildings_score
        production_max_value = max(production_scores.values())
        production_min_value = min(production_scores.values())

        # get the most/lowest valued buildings
        production_max_value_list = []
        production_min_value_list = []
        for key, value in production_scores.items():
            if value == production_max_value:
                production_max_value_list.append(key)

            if value == production_min_value:
                production_min_value_list.append(key)

        # resources
        resources_scores = {}
        for i in building_factory.get_all_building_names():
            resources_scores[i] = self.calculate_resource_score(
                    building=i,
                    current_resources=resources,
                    goal_resources=self.resource_goal,
                    population=population)

        # find the highest value in buildings_score
        resources_max_value = max(resources_scores.values())
        resources_min_value = min(resources_scores.values())

        # get the most/lowest valued buildings
        resources_max_value_list = []
        resources_min_value_list = []
        for key, value in resources_scores.items():
            if value == resources_max_value:
                resources_max_value_list.append(key)

            if value == resources_min_value:
                resources_min_value_list.append(key)






        # pprint(building_scores)

        # best buildings = min_value_list
        best_fitting_buildings = production_min_value_list
        # print(f"min_value_list:{min_value_list}")
        # print (f"max_value_list:{max_value_list}")






        return best_fitting_buildings


economy_sim = EconomySimulator()


def main():
    run = True
    pygame.display.set_mode((800, 600))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # economy_sim.run_simulation()

                    production = {
                        "energy": -2,
                        "food": -1,
                        "minerals": 0,
                        "water": 0,
                        "technology": 0,
                        "population": 0
                        }

                    resources = {
                        "energy": 1000,
                        "food": 1000,
                        "minerals": 1000,
                        "water": 1000,
                        "technology": 1000,
                        "population": 1000
                        }

                    production_goal = {
                        "energy": 1,
                        "food": 1,
                        "minerals": 1,
                        "water": 1,
                        "technology": 1,
                        "population": 0
                        }

                    resource_goal = {
                        "energy": 10000,
                        "food": 10000,
                        "minerals": 10000,
                        "water": 10000,
                        "technology": 10000,
                        "population": 10000
                        }
                    population = 800
                    best_fitting_building = economy_sim.get_best_fitting_buildings_to_goals(production, resources, population, production_goal, resource_goal)
                    print (best_fitting_building)


if __name__ == "__main__":
    main()
