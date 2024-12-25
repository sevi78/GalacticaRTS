from typing import Dict

from source.economy_ki.economy_calculator_ki import Goal, Player

class EconomyCalculatorFunctions:

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


    def calculate_production_difference(self,goal: Goal, player: Player) -> Dict[str, int]:
        diff = {resource: goal.production[resource] - player.production[resource]
                for resource in goal.production}

        return diff


    def calculate_resource_difference(self,goal: Goal, player: Player) -> Dict[str, int]:
        diff = {resource: abs(goal.resources[resource] - player.get_stock()[resource])
                for resource in goal.resources}
        # print(f"Resource difference: {diff}")
        return diff


    def calculate_space_harbor_score(self,building_name, player, penalty):
        space_harbor_penalty = -penalty if (
                'space harbor' in player.buildings and building_name == 'space harbor') else 0
        return space_harbor_penalty


    def calculate_university_score(self,building_name, economy_agent):
        university_score = 0
        if "technology" in economy_agent.possible_resources and building_name == 'university':
            university_score = 100 / economy_agent.buildings_max * len(economy_agent.buildings)
        else:
            university_score = -100

        return university_score


    def calculate_population_score(self,building_name, player):
        population_score = player.population - player.population_limit if building_name in ['town', 'city',
                                                                                            'metropole'] and player.population else 0
        return population_score


    def calculate_category_penalty(self,building, economy_agent, penalty):
        category_penalty = -penalty if building.get('category') not in economy_agent.possible_resources else 0
        return category_penalty


    def calculate_build_population_minimum_penalty(self,building, economy_agent, penalty):
        build_population_minimum_penalty = -penalty if building.get('build_population_minimum', 0) > economy_agent.population else 0
        return build_population_minimum_penalty


    def calculate_resource_score(self,building, resource_diff):
        resource_score = sum(
                (resource_diff.get(resource, 0) - building.get(f'price_{resource}', 0)) for resource in resource_diff)
        return resource_score


    def calculate_production_score(self,building, production_diff):
        production_score = sum(building.get(f'production_{resource}', 0) * production_diff.get(resource, 0) for resource in
                               production_diff)
        return production_score
