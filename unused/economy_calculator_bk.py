from pprint import pprint

from source.factories.building_factory import building_factory


class EconomyCalculator:
    def calculate_score(
            self, building: str, current_dict: dict, goal_dict: dict, key: str
            ) -> dict:  # should not be used!
        """ returns a dict of the score for the building based on:
        - building:     str representing the building
        - current_dict: dict representing production or price
        - goal_dict:    dict representing production or price to achieve
        - key:          str representing either 'production' or 'prices'
        """
        # error check
        assert key in ["production", "prices"], print(f"key must be either 'production' or 'prices'! not {key}")

        # get the dict representing the building scores
        building_dict = getattr(building_factory, f"get_{key}_from_buildings_json")(building)

        # set all values to minus for prices
        if key == "prices":
            building_dict = {key: value * -1 for key, value in building_dict.items()}

        # calculate new_dict
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            new_dict[key] = value + current_dict[key]

        # calculate building_scores
        building_scores = {
            key: abs(goal_dict[key] - new_dict[key]) for key in
            goal_dict.keys()}

        return building_scores

    def calculate_production_score__(self, building: str, current_dict: dict, goal_dict: dict) -> dict:# original dont touch!!!
        """ returns a dict of the score for the building based on:
        - building:     str representing the building
        - current_dict: dict representing production or price
        - goal_dict:    dict representing production or price to achieve

        """
        # get the dict representing the building scores
        building_dict = building_factory.get_production_from_buildings_json(building)

        # calculate new_dict
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            new_dict[key] = value + current_dict[key]

        # calculate building_scores
        building_scores = {
            key: abs(goal_dict[key] - new_dict[key]) for key in
            goal_dict.keys()}

        return building_scores

    def calculate_production_score(self, building: str, current_dict: dict, goal_dict: dict, resources:dict, resource_goal:dict) -> dict:
        """ returns a dict of the score for the building based on:
        - building:     str representing the building
        - current_dict: dict representing production or price
        - goal_dict:    dict representing production or price to achieve

        """
        # get the dict representing the building scores
        building_dict = building_factory.get_production_from_buildings_json(building)

        # calculate resources into production
        resource_min = min(resources.values())
        resource_min_keys = [i for i in resources if resources[i] == resource_min]

        resource_differ = self.get_resource_difference(resources, resource_goal)
        resource_differ_max = max(resource_differ.values())
        resource_differ_max_keys = [i for i in resources if resource_differ[i] == resource_differ_max]

        # calculate new_dict
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            if key in resource_differ_max_keys:
                new_dict[key] = (value + current_dict[key]) / resource_differ_max
            else:
                new_dict[key] = value + current_dict[key]

        # calculate building_scores
        building_scores = {
            key: abs(goal_dict[key] - new_dict[key]) for key in
            goal_dict.keys()}

        return building_scores

    def get_production_sum_score__(self, building: str, population: int, scores: dict, building_dict: dict) -> float:# original!! dont touch !!!
        """ returns a dict of the sum of all scores based on:
        - building:         str representing the building

        - population        int representing the population
        - scores:           dict representing production or price
        - building_dict:    dict representing production or price of the building
        - resources:        dict representing resources of the player

        the lower the score, the better
        """

        # get sum
        sum_ = 0
        for key, value in scores.items():
            sum_ += value

        # limit sum to population, buildings that cannot be built because the population is not sufficient
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +1000000

        # limit unproductive buildings
        if all(value == 0 for value in building_dict.values()):
            sum_ = +1000000
        return sum_

    def get_production_sum_score(self, building: str, population: int, scores: dict, building_dict: dict, resources:dict, resource_goal:dict) -> float:# touch !!!
        """ returns a dict of the sum of all scores based on:
        - building:         str representing the building

        - population        int representing the population
        - scores:           dict representing production or price
        - building_dict:    dict representing production or price of the building
        - resources:        dict representing resources of the player

        the lower the score, the better
        """


        # get sum
        sum_ = 0
        for key, value in scores.items():
            sum_ += value

        # limit sum to population, buildings that cannot be built because the population is not sufficient
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +1000000

        # limit unproductive buildings
        if all(value == 0 for value in building_dict.values()):
            sum_ = +1000000
        return sum_

    def calculate_resource_score(self, building: str, current_dict: dict, goal_dict: dict) -> dict:
        """ returns a dict of the score for the building based on:
        - building:     str representing the building
        - current_dict: dict representing production or price
        - goal_dict:    dict representing production or price to achieve

        """
        # get the dict representing the building scores
        building_dict = building_factory.get_prices_from_buildings_json(building)

        # calculate new_dict
        new_dict = {}
        # add both, current_dict and building_dict
        # this will be the actual values if the building is built
        for key, value in building_dict.items():
            new_dict[key] =  current_dict[key] - value

        # calculate building_scores
        building_scores = {
            key: abs(goal_dict[key] + new_dict[key]) for key in
            goal_dict.keys()}

        return building_scores

    def get_resource_sum_score(self, building: str, population: int, scores: dict, building_dict: dict) -> float:
        """ returns a dict of the sum of all scores based on:
        - building:         str representing the building
        - population        int representing the population
        - scores:           dict representing production or price
        - building_dict:    dict representing production or price of the building

        the lower the score, the better
        """

        # get sum
        sum_ = 0
        for key, value in scores.items():
            sum_ += value

        # limit sum to population, buildings that cannot be built because the population is not sufficient
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = +1000000

        # limit unproductive buildings
        if all(value == 0 for value in building_dict.values()):
            sum_ = +1000000
        return sum_

    def get_lowest_score_keys(self, building_score_sums: dict) -> list:
        """ returns a list of all keys from building_score_sums that have the lowest value
        """
        min_value = min(building_score_sums.values())

        # get the lowest valued buildings == the best one
        min_value_list = []
        for key, value in building_score_sums.items():
            if value == min_value:
                min_value_list.append(key)
        return min_value_list

    def get_best_fitting_building__(self, population: int, production: dict, production_goal: dict) -> list:# original, dont touch !!
        """ return a list of the best fitting bildings based on:
        - population        int representing the population
        - production        dict representing the current production
        - production_goal:  dict representing the production to achieve
        """
        # get production scores
        building_production_scores = {}
        building_production_scores_sums = {}

        # calculate all buildings scores and store thm to a tmp dict
        for building in building_factory.get_all_building_names():
            building_production_score = economy_calculator.calculate_production_score(
                    building=building,
                    current_dict=production,
                    goal_dict=production_goal)

            building_production_scores[building] = building_production_score

            # calculate the sum of all buildings score values and store to tmp dict
            building_production_score_sum_ = economy_calculator.get_production_sum_score(
                    building=building,
                    population=population,
                    scores=building_production_score,
                    building_dict=building_factory.get_production_from_buildings_json(building))
            building_production_scores_sums[building] = building_production_score_sum_

        # get lowest valued key from the scores
        lowest_production_score_keys = economy_calculator.get_lowest_score_keys(building_production_scores_sums)
        return lowest_production_score_keys

    def get_best_fitting_building(self, population: int, production: dict, production_goal: dict, resources:dict, resource_goal:dict) -> list:# touch !!
        """ return a list of the best fitting bildings based on:
        - population        int representing the population
        - production        dict representing the current production
        - production_goal:  dict representing the production to achieve
        """
        # get production scores
        building_production_scores = {}
        building_production_scores_sums = {}

        # calculate all buildings scores and store thm to a tmp dict
        for building in building_factory.get_all_building_names():
            building_production_score = economy_calculator.calculate_production_score(
                    building=building,
                    current_dict=production,
                    goal_dict=production_goal,
                    resources=resources,
                    resource_goal=resource_goal
                    )

            building_production_scores[building] = building_production_score

            # calculate the sum of all buildings score values and store to tmp dict
            building_production_score_sum_ = economy_calculator.get_production_sum_score(
                    building=building,
                    population=population,
                    scores=building_production_score,
                    building_dict=building_factory.get_production_from_buildings_json(building),
                    resources= resources,
                    resource_goal= resource_goal)
            building_production_scores_sums[building] = building_production_score_sum_

        # get lowest valued key from the scores
        lowest_production_score_keys = economy_calculator.get_lowest_score_keys(building_production_scores_sums)
        return lowest_production_score_keys
    def get_resource_difference(self, resources:dict, resource_goal:dict):
        differ = {}
        for key, value in resources.items():
            differ[key] = resource_goal[key] - resources[key]
        return differ



economy_calculator = EconomyCalculator()


def main():
    resources = {
        "energy": 100,
        "food": 10000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 1000
        }
    resource_goal = {
        "energy": 10000,
        "food": 10000,
        "minerals": 10000,
        "water": 10000,
        "technology": 10000,
        "population": 10000
        }

    production = {
        "energy": 0,
        "food": 1,
        "minerals": 0,
        "water": 0,
        "technology": 0,
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

    population = 800

    task = "production"#"resources"
    if task == "production":
        lowest_production_score_keys = economy_calculator.get_best_fitting_building(population, production, production_goal, resources, resource_goal)
        print(f"lowest_production_score_keys: {lowest_production_score_keys}")
        resource_differ = economy_calculator.get_resource_difference(resources, resource_goal)
        # print (f"resource_differ: {resource_differ}")
    else:
        # resources
        # get resources scores
        building_resources_scores = {}
        building_resources_scores_sums = {}

        # calculate all buildings scores and store thm to a tmp dict
        for building in building_factory.get_all_building_names():
            building_resources_score = economy_calculator.calculate_resource_score(
                    building=building,
                    current_dict=resources,
                    goal_dict=resource_goal)

            building_resources_scores[building] = building_resources_score

            # calculate the sum of all buildings score values and store to tmp dict
            building_resources_score_sum_ = economy_calculator.get_resource_sum_score(
                    building=building,
                    population=population,
                    scores=building_resources_score,
                    building_dict=building_factory.get_prices_from_buildings_json(building))

            building_resources_scores_sums[building] = building_resources_score_sum_

        # get lowest valued key from the scores
        lowest_resource_score_keys = economy_calculator.get_lowest_score_keys(building_resources_scores_sums)

        pprint(f"building_resources_scores: {building_resources_scores}")
        pprint(f"lowest_resource_score_keys: {lowest_resource_score_keys}")


if __name__ == "__main__":
    main()
