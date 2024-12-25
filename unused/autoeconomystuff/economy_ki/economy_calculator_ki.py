from typing import Dict, List

from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file


class Player:
    def __init__(self, production: Dict[str, int], resources: Dict[str, int], population_limit: int):
        self.production = production
        self.stock = resources
        self.population = resources['population']
        self.population_limit = population_limit
        self.buildings = []

    def get_stock(self) -> dict:
        return self.stock


class EconomyAgent:
    def __init__(
            self, population: int, population_limit: int, production: Dict[str, int],
            buildings: List[str], buildings_max: int, population_grow_factor: float,
            building_slot_amount: int, possible_resources: List[str]
            ):
        self.population = population
        self.population_limit = population_limit
        self.production = production
        self.buildings = buildings
        self.buildings_max = buildings_max
        self.population_grow_factor = population_grow_factor
        self.building_slot_amount = building_slot_amount
        self.possible_resources = possible_resources
        print(f"EconomyAgent initialized with population: {population}, population_limit: {population_limit}, "
              f"production: {production}, buildings: {buildings}, buildings_max: {buildings_max}, "
              f"population_grow_factor: {population_grow_factor}, building_slot_amount: {building_slot_amount}, "
              f"possible_resources: {possible_resources}")


class Goal:
    def __init__(self, production: Dict[str, int], resources: Dict[str, int]):
        self.production = production
        self.resources = resources
        print(f"Goal initialized with production: {production}, resources: {resources}")

    def __repr__(self):
        return f"production: {self.production}, resources:{self.resources}"


class EconomyCalculatorKI:
    def __init__(self):
        self.buildings_file = load_file("buildings.json", "config")
        self.buildings = self.decategorize_buildings_file(self.buildings_file)
        self.building_scores = {}

    def decategorize_buildings_file(self, buildings_file) -> Dict[str, Dict]:
        """ returns a dict from the buildings.py file without any categories for better handling.
            Note categories are still stored in the values
        """
        buildings_raw = buildings_file
        buildings = {}
        for category in buildings_raw.keys():
            for key, value in buildings_raw[category].items():
                buildings[value["name"]] = value

        return buildings

    def calculate_percentage(self, maximum: float, value: float) -> float:
        """
        Calculate the percentage of a value relative to a base value.

        :param maximum: The value representing 100%
        :param value: The value to calculate the percentage for
        :return: The calculated percentage as a float
        """
        if value == 0.0:
            return 0.0
        if maximum == 0.0:
            return 0.0

        return (value / maximum) * 100

    def calculate_absolute_difference(self, goal, value):
        return abs(goal - value)
    def calculate_production_difference(self, goal: Goal, player: Player, building:dict) -> Dict[str, int]:
        diff = {}
        for key, value in goal.production.items():
            diff[key] = self.calculate_absolute_difference(goal.production[key], building["production_" + key])


        return diff

    def calculate_resource_difference(self, goal: Goal, player: Player, building:dict) -> Dict[str, int]:
        diff = {}
        for key, value in goal.resources.items():
            diff[key] = self.calculate_absolute_difference(goal.resources[key] + building["price_" + key], player.get_stock()[key])

        return diff

    def calculate_space_harbor_score(self, building_name, player, penalty):
        space_harbor_penalty = -penalty if (
                'space harbor' in player.buildings and building_name == 'space harbor') else 0
        return space_harbor_penalty

    def calculate_university_score(self, building_name, player, economy_agent, penalty):
        university_score = 0
        return university_score
        if "technology" in economy_agent.possible_resources and building_name == 'university':
            university_score = player.get_all_building_slots() - len(player.get_all_buildings())
            # university_score = 100 / economy_agent.buildings_max * len(economy_agent.buildings)
        else:
            university_score = -penalty

        return university_score

    def calculate_population_score(self, building_name, player, economy_agent):
        category = building_factory.get_category_by_building(building_name)
        population_score = 0
        if category == "population":
            if player.stock["population"] > player.population_limit:
                population_score += player.population - player.population_limit
            if economy_agent.population > economy_agent.population_limit:
                population_score += economy_agent.population - economy_agent.population_limit

        return population_score

    def calculate_category_penalty(self, building, economy_agent, penalty):
        category_penalty = -penalty if building.get('category') not in economy_agent.possible_resources else 0
        return category_penalty

    def calculate_build_population_minimum_penalty(self, building, economy_agent, penalty):
        build_population_minimum = building.get('build_population_minimum')
        build_population_minimum_penalty = 0
        if build_population_minimum > economy_agent.population:
            build_population_minimum_penalty = -penalty

        # build_population_minimum_penalty = -penalty if building.get('build_population_minimum', 0) > economy_agent.population else 0
        return build_population_minimum_penalty

    def calculate_resource_score(self, building, resource_diff):
        resource_score = sum(
                (resource_diff.get(resource, 0) - building.get(f'price_{resource}', 0)) for resource in resource_diff) / len(resource_diff.keys())
        return resource_score

    def calculate_food_score(self, building: dict, economy_agent):
        food_production = economy_agent.production.get("food")
        food_score = 0
        if 'population' in economy_agent.possible_resources and "food" in economy_agent.possible_resources:
            if building.get("category") == "food":
                food_score = food_production * -1

        return food_score

    def calculate_production_score(self, building, production_diff):
        production_score = sum(
                building.get(f'production_{resource}', 0) * production_diff.get(resource, 0) for resource in
                production_diff)
        return production_score

    def calculate_building_score(
            self, building_name: str, building: Dict, goal: Goal, player: Player, economy_agent: EconomyAgent,production_differs_percentage, resource_differ_percentage
            ) -> float:
        name = building_name
        penalty = 100

        production_diff_ = self.calculate_production_difference(goal, player, building)
        resource_diff_ = self.calculate_resource_difference(goal, player, building)

        production_diff = production_differs_percentage[building_name]
        resource_diff = resource_differ_percentage[building_name]

        # scores = {
        #     "production_score": self.calculate_production_score(building, production_diff),
        #     "resource_score": self.calculate_resource_score(building, resource_diff),
        #     "build_population_minimum_penalty": self.calculate_build_population_minimum_penalty(building, economy_agent, penalty),
        #     "category_penalty": self.calculate_category_penalty(building, economy_agent, penalty),
        #     "population_score": self.calculate_population_score(building_name, player, economy_agent),
        #     "university_score": self.calculate_university_score(building_name, player, economy_agent, penalty),
        #     "space_harbor_penalty": self.calculate_space_harbor_score(building_name, economy_agent, penalty),
        #     "food_score": self.calculate_food_score(building, economy_agent)
        #     }

        # scores = {
        #     "production_score": self.calculate_production_score(building, production_diff),
        #     "resource_score": self.calculate_resource_score(building, resource_diff),
        #     "build_population_minimum_penalty": self.calculate_build_population_minimum_penalty(building, economy_agent, penalty),
        #     "category_penalty": self.calculate_category_penalty(building, economy_agent, penalty),
        #     "population_score": self.calculate_population_score(building_name, player, economy_agent),
        #     "university_score": self.calculate_university_score(building_name, player, economy_agent, penalty),
        #     "space_harbor_penalty": 0,
        #     "food_score": 0
        #     }

        scores = {
            "production_score": self.calculate_production_score(building, production_diff),
            "resource_score": 0,#self.calculate_resource_score(building, resource_diff),
            "build_population_minimum_penalty":self.calculate_build_population_minimum_penalty(building, economy_agent, penalty),
            "category_penalty": 0,
            "population_score": 0,
            "university_score": 0,
            "space_harbor_penalty": 0,
            "food_score": 0
            }

        total_score = self.calculate_total_score(scores)

        return total_score

    def calculate_total_score(
            self,
            scores
            ):
        total_score = 0
        for key, value in scores.items():
            total_score += value

        return total_score

    def find_best_building(
            self, buildings: Dict[str, Dict], goal: Goal, player: Player, economy_agent: EconomyAgent
            ) -> str:
        print("\nFinding best building...")

        production_differs_percentage = self.calculate_all_production_scores_in_percent(buildings, goal, player)
        resource_differ_percentage = self.calculate_all_resource_scores_in_percent(buildings, goal, player)

        building_scores = {name: self.calculate_building_score(name, building, goal, player, economy_agent, production_differs_percentage, resource_differ_percentage)
                           for name, building in buildings.items()}
        best_building = max(building_scores, key=building_scores.get)

        # print ("building_scores: ", building_scores)
        # print(f"Best building found: {best_building} with score: {building_scores[best_building]}")
        return best_building

    def calculate_all_production_scores_in_percent(self, buildings, goal, player):
        # get all production differs form all buildings
        production_differs_raw = {name: self.calculate_production_difference(goal, player, building) for name, building
                                  in buildings.items()}
        # get the highest value
        all_values = []
        for building_name, value_dict in production_differs_raw.items():
            for key, value in value_dict.items():
                all_values.append(value)

        max_value = max(all_values)
        # level the values to percentage
        production_differs_percentage = {}
        for building_name, value_dict in production_differs_raw.items():
            production_differs_percentage[building_name] = {key: 100-self.calculate_percentage(max_value, value) for
                                                            key, value in value_dict.items()}

        return production_differs_percentage

    def calculate_all_resource_scores_in_percent(self, buildings, goal, player):
        # get all production differs form all buildings
        differs_raw = {name: self.calculate_resource_difference(goal, player, building) for name, building
                                  in buildings.items()}
        # get the highest value
        all_values = []
        for building_name, value_dict in differs_raw.items():
            for key, value in value_dict.items():
                all_values.append(value)
        max_value = max(all_values)
        # level the values to percentage
        resource_differs_percentage = {}
        for building_name, value_dict in differs_raw.items():
            resource_differs_percentage[building_name] = {key: 100-self.calculate_percentage(max_value, value) for
                                                            key, value in value_dict.items()}

        return resource_differs_percentage
def test_find_best_building():
    print("Starting test_find_best_building")
    economy_calculator = EconomyCalculatorKI()
    buildings = economy_calculator.buildings

    goal = Goal(
            production={'energy': 1, 'food': 2, 'minerals': 1, 'water': 1, 'technology': 1, 'population': 0},
            resources={'energy': 1000, 'food': 1000, 'minerals': 1000, 'water': 1000, 'technology': 1000, 'population': 1000}
            )

    player = Player(
            production={'energy': 0, 'food': 0, 'minerals': 0, 'water': 0, 'technology': 0, 'population': 0},
            resources={'energy': 1000, 'food': 1000, 'minerals': 1000, 'water': 1000, 'technology': 10000, 'population': 1000},
            population_limit=100
            )

    economy_agent = EconomyAgent(
            population=50,
            population_limit=100,
            production={'energy': 0, 'food': 0, 'minerals': 0, 'water': 0, 'technology': 0, 'population': 0},
            buildings=[],
            buildings_max=10,
            population_grow_factor=0.1,
            building_slot_amount=5,
            possible_resources=['energy', 'food', 'minerals', 'water', 'technology']
            )

    best_building = economy_calculator.find_best_building(buildings, goal, player, economy_agent)
    print(f"\nThe best building to construct is: {best_building}")

    building_scores = {name: economy_calculator.calculate_building_score(name, building, goal, player, economy_agent)
                       for name, building in buildings.items()}
    sorted_scores = sorted(building_scores.items(), key=lambda x: x[1], reverse=True)

    print("sorted_scores:", sorted_scores)


if __name__ == "__main__":
    test_find_best_building()
