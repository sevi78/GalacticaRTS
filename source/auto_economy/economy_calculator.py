from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file


class EconomyCalculator:
    """
    this calculates the best fitting building to the economy of the player
    TODO: handle specials cases:
    - if the player runs out of planets
    - population grow optimizations
    - upgrade of buildings


    The EconomyCalculator class is designed to determine the most suitable building for a player's economy in a game.
    It evaluates buildings based on current production, resource levels, and goals, and calculates scores to identify
    the best building to construct.

    Example Usage
    from source.factories.building_factory import building_factory

    building_factory = BuildingFactory()
    economy_calculator = EconomyCalculator()

    population = 100
    production = {'food': 50, 'wood': 30}
    production_goal = {'food': 100, 'wood': 50}
    resources = {'gold': 200, 'stone': 150}
    resource_goal = {'gold': 300, 'stone': 200}

    best_buildings = economy_calculator.get_best_fitting_building(
        population=population,
        production=production,
        production_goal=production_goal,
        resources=resources,
        resource_goal=resource_goal
    )
    print(best_buildings)

    Main functionalities
    Calculate the production score for a building based on current and goal production and resources.
    Sum the production scores to determine the overall suitability of a building.
    Identify the building(s) with the lowest score, indicating the best fit for the player's economy.

    Methods
    calculate_production_score: Computes the score for a building based on production and resource differences.
    get_production_sum_score: Sums the scores and applies constraints based on population and productivity.
    get_lowest_score_keys: Finds the buildings with the lowest scores.
    get_resource_difference: Calculates the difference between current resources and resource goals.
    calculate_building_production_scores: Generates production scores for all buildings.
    calculate_building_scores_sums: Sums the production scores for all buildings.
    get_best_fitting_building: Determines the best building(s) to construct based on scores.

    Fields
    building_factory: An instance of BuildingFactory used to retrieve building data and requirements.
    """

    def __init__(self):
        self.settings = load_file("auto_economy_calculator_settings.json", "config")

    def calculate_production_score(
            self,
            population_limit: int,
            population: int,
            building: str,
            current_production_dict: dict,
            production_goal_dict: dict,
            current_resources_dict: dict,
            resource_goal_dict: dict
            ) -> dict:

        """ returns a dict of the score for the building based on:
        - building:         str representing the building
        - current_dict:     dict representing production
        - goal_dict:        dict representing production
        - resources:        dict representing teh resources of the player
        - resource_goal:    dict representing teh resources of the player
        """
        # get the dict representing the building scores
        building_dict = building_factory.get_production_from_buildings_json(building)
        # print (f"building_dict: {building_dict}")
        # building_dict: {'energy': 0, 'food': -1, 'minerals': 0, 'water': 3, 'technology': 0, 'population': 0}

        # calculate resources into production
        resource_differ = self.get_resource_difference(current_resources_dict, resource_goal_dict)
        # print (f"resource_differ: {resource_differ}")
        # resource_differ: {'energy': 9900, 'food': 9000, 'minerals': 9000, 'water': 9000, 'technology': 9000, 'population': 0}

        resource_differ_max = max(resource_differ.values()) if max(resource_differ.values()) != 0.0 else 1
        resource_differ_max_keys = [i for i in current_resources_dict if resource_differ[i] == resource_differ_max]
        # population_differ = population_limit - population

        # print (f"population_differ: {population_differ}")
        # # print (f"population_limit: {population_limit},population:{population}, population_differ: {population_differ}")
        #
        # population_factor = 1
        # if population_differ < 0.0:
        #     population_factor = abs(population_differ)

        # calculate new_dict
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            # calculate into the score: if key is the lowest stock value, then divide the value through the difference
            # between the resources and the resource goal
            # this ensures that the lower the stock value is, the higher its key gets prioritized

            # if the resource(key) is in the list of the highest values from the list
            if key in resource_differ_max_keys:
                # calculate the score by adding the production to the value (default=0)
                # then divide through the value of the highest differences from any resources
                # to include the resources to the score
                # divide through the amount of available building slots

                production_to_goal_differ = value + current_production_dict[key]
                new_dict[key] = production_to_goal_differ / resource_differ_max

            # if not key is the highest stock value
            else:
                new_dict[key] = value + current_production_dict[key]

        # implement population into calculation
        # if population_factor > 1.0:
        #     for key, value in new_dict.items():
        #         if key == "population":
        #             new_dict[key] /= population_factor
        #         else:
        #             new_dict[key] *= population_factor

        # calculate building_scores
        building_scores = {
            key: abs(production_goal_dict[key] - new_dict[key]) for key in
            production_goal_dict.keys()}

        # print (building_scores)
        return building_scores

    def get_production_sum_score(
            self,
            building: str,
            population_limit: int,
            population: int,
            scores: dict,
            building_dict: dict
            ) -> float:

        """ returns a dict of the sum of all scores based on:
        - building:         str representing the building

        - population        int representing the population
        - scores:           dict representing production or price
        - building_dict:    dict representing production or price of the building

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

        # weight population buildings
        # if population_limit < population:
        #     category = building_factory.get_category_by_building(building)
        #     if category != "population":
        #         sum_ = 1000000

        return sum_

    def get_lowest_score_keys(self, building_score_sums: dict) -> list:
        """ returns a list of all keys from building_score_sums that have the lowest value
        """
        min_value = min(building_score_sums.values())

        # get the lowest valued buildings == the best one
        lowest_score_keys = [key for key, value in building_score_sums.items() if value == min_value]
        return lowest_score_keys

    def get_resource_difference(self, resources: dict, resource_goal: dict) -> dict:
        """ returns the difference between resources and resource_goal as dict
        """
        differ = {}
        for key, value in resources.items():
            differ[key] = resource_goal[key] - resources[key]
        return differ

    def calculate_building_production_scores(
            self,
            population_limit: int,
            population: int,
            production: dict,
            production_goal: dict,
            resources: dict,
            resource_goal: dict
            ) -> dict:
        building_production_scores = {}
        for building in building_factory.get_all_building_names():
            building_production_score = self.calculate_production_score(
                    population_limit=population_limit,
                    population=population,
                    building=building,
                    current_production_dict=production,
                    production_goal_dict=production_goal,
                    current_resources_dict=resources,
                    resource_goal_dict=resource_goal
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
                    building_dict=building_factory.get_production_from_buildings_json(building))
            building_production_scores_sums[building] = building_production_score_sum_
        return building_production_scores_sums

    def get_best_fitting_building(
            self,
            all_buildings: int,
            all_building_slots: int,
            population_limit: int,
            population: int,
            production: dict,
            production_goal: dict,
            resources: dict,
            resource_goal: dict
            ) -> list:

        building_production_scores = self.calculate_building_production_scores(population_limit, population, production, production_goal, resources, resource_goal)
        building_production_scores_sums = self.calculate_building_scores_sums(building_production_scores, population_limit, population)

        # print(f"lowest_production_score_keys: {lowest_production_score_keys}")

        # implement population weight
        population_differ = abs(population_limit - population)
        for key, value in building_production_scores_sums.items():
            if not key in building_factory.get_building_names("population"):
                if population > population_limit:
                    building_production_scores_sums[key] *= population_differ

        # # implement university weight
        building_slot_to_all_buildings_differ = abs(all_building_slots - all_buildings if all_building_slots - all_buildings != 0 else 1)

        for key, value in building_production_scores_sums.items():
            if not key == "university":
                building_production_scores_sums[key] *= 1 / building_slot_to_all_buildings_differ
            # else:
            #     building_production_scores_sums[key] /= 1/building_slot_to_all_buildings_differ

            print(f"key: {key}, value: {value}")
        # print (f"building_production_scores_sums: {building_production_scores_sums}")

        lowest_production_score_keys = self.get_lowest_score_keys(building_production_scores_sums)
        return lowest_production_score_keys


economy_calculator = EconomyCalculator()


def main():
    resources = {
        "energy": 1000,
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
        "food": 1,
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

    population = 129
    population_limit = 1000
    all_buildings = 200
    all_building_slots = 200

    get_best_fitting_building = economy_calculator.get_best_fitting_building(all_buildings, all_building_slots, population_limit, population, production, production_goal, resources, resource_goal)
    print(f"get_best_fitting_building: {get_best_fitting_building}")


if __name__ == "__main__":
    main()
