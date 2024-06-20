from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file


def get_percentage(current, goal):
    if goal == 0:
        return 100
    return (current / goal) * 100


class EconomyCalculator:
    """ this calculates the best fitting building to the economy of the player
    TODO: handle specials cases:
    - if the player runs out of planets
    - population grow optimizations
    - upgrade of buildings
    """

    def __init__(self):
        self.settings = load_file("auto_economy_calculator_settings.json", "config")

    def calculate_production_score(
            self, population_limit: int, population: int, building: str, current_production: dict,
            production_goal: dict, current_resources: dict, resource_goal: dict
            ) -> dict:
        building_dict = building_factory.get_production_from_buildings_json(building)
        production_scores = {}

        for resource, value in production_goal.items():
            current_value = current_production.get(resource, 0)
            production_percentage = get_percentage(current_value, value)
            production_scores[resource] = 100 - production_percentage

        for resource, value in resource_goal.items():
            current_value = current_resources.get(resource, 0)
            resource_percentage = get_percentage(current_value, value)
            production_scores[resource] += (100 - resource_percentage)

        population_differ = abs(population_limit - population)
        population_factor = 1.0
        if population > population_limit:
            population_factor = 1 + (population_differ / population_limit)

        return {k: max(0, min(100, v * population_factor)) for k, v in production_scores.items()}

    def get_production_sum_score(
            self, building: str, population_limit: int, population: int, scores: dict, building_dict: dict
            ) -> float:
        """ returns a dict of the sum of all scores based on:
        - building: str representing the building
        - population int representing the population
        - scores: dict representing production or price
        - building_dict: dict representing production or price of the building
        the lower the score, the better
        """
        # get sum
        sum_ = sum(value for value in scores.values())

        # limit sum to population, buildings that cannot be built because the population is not sufficient
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = 1000000

        # limit unproductive buildings
        if all(value == 0 for value in building_dict.values()):
            sum_ = 1000000

        return sum_

    def get_lowest_score_keys(self, building_score_sums: dict) -> list:
        """ returns a list of all keys from building_score_sums that have the lowest value """
        min_value = min(building_score_sums.values())
        # get the lowest valued buildings == the best one
        lowest_score_keys = [key for key, value in building_score_sums.items() if value == min_value]
        return lowest_score_keys

    def get_resource_difference(self, resources: dict, resource_goal: dict) -> dict:
        """ returns the difference between resources and resource_goal as dict """
        differ = {}
        for key, value in resources.items():
            differ[key] = resource_goal[key] - resources[key]
        return differ

    def calculate_building_production_scores(
            self, population_limit: int, population: int, production: dict, production_goal: dict, resources: dict,
            resource_goal: dict
            ) -> dict:
        building_production_scores = {}
        for building in building_factory.get_all_building_names():
            building_production_score = self.calculate_production_score(
                    population_limit=population_limit,
                    population=population,
                    building=building,
                    current_production=production,
                    production_goal=production_goal,
                    current_resources=resources,
                    resource_goal=resource_goal
                    )
            building_production_scores[building] = building_production_score
        return building_production_scores

    def calculate_building_scores_sums(
            self, building_production_scores: dict, population_limit: int, population: int
            ) -> dict:
        building_production_scores_sums = {}
        for building, scores in building_production_scores.items():
            building_production_score_sum_ = self.get_production_sum_score(
                    building=building,
                    population_limit=population_limit,
                    population=population,
                    scores=scores,
                    building_dict=building_factory.get_production_from_buildings_json(building)
                    )
            building_production_scores_sums[building] = building_production_score_sum_
        return building_production_scores_sums

    def get_best_fitting_building(
            self, all_buildings: int, all_building_slots: int, population_limit: int, population: int, production: dict,
            production_goal: dict, resources: dict, resource_goal: dict
            ) -> list:
        building_production_scores = self.calculate_building_production_scores(population_limit, population, production, production_goal, resources, resource_goal)
        building_production_scores_sums = self.calculate_building_scores_sums(building_production_scores, population_limit, population)

        # implement population weight
        population_differ = abs(population_limit - population)
        for key, value in building_production_scores_sums.items():
            if not key in building_factory.get_building_names("population"):
                if population > population_limit:
                    building_production_scores_sums[key] *= population_differ

        lowest_production_score_keys = self.get_lowest_score_keys(building_production_scores_sums)
        return lowest_production_score_keys


economy_calculator = EconomyCalculator()


def main():
    resources = {
        "energy": 100,
        "food": 1000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 0
        }
    resource_goal = {
        "energy": 10000,
        "food": 10000,
        "minerals": 10000,
        "water": 10000,
        "technology": 10000,
        "population": 0
        }
    production = {
        "energy": 1,
        "food": 11,
        "minerals": 1,
        "water": 1,
        "technology": 1,
        "population": 0
        }
    production_goal = {
        "energy": 1,
        "food": 1,
        "minerals": 1,
        "water": 1,
        "technology": 1,
        "population": 0
        }
    population = 120
    population_limit = 1000
    all_buildings = 200
    all_building_slots = 200

    get_best_fitting_building = economy_calculator.get_best_fitting_building(all_buildings, all_building_slots, population_limit, population, production, production_goal, resources, resource_goal)
    print(f"get_best_fitting_building: {get_best_fitting_building}")


if __name__ == "__main__":
    main()
