import random
from pprint import pprint

from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file
from source.math.math_handler import get_sum_up_to_n


class EconomyAgent:
    def __init__(self, **kwargs):
        # self.player = config.app.players[self.planet.owner] if self.planet.owner in config.app.players else None
        self.building_scores = {}
        self.population_special = None
        self.technology_special = None
        self.minerals_special = None
        self.food_special = None
        self.energy_special = None
        self.water_special = None
        self.population_grow_factor = 0.1
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}

        self.buildings = kwargs.get("buildings", [])
        self.buildings_max = kwargs.get("buildings_max", 10)
        self.population = kwargs.get("population", 0)
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = kwargs.get("alien_population", 0)
        self.alien_attitude = kwargs.get("alien_attitude", random.randint(0, 100))

        self.building_slot_amount = kwargs.get("building_slot_amount", 3)
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0: 500, 1: 750, 2: 1250, 3: 2500, 4: 5000, 5: 25000, 6: 100000}
        self.building_slot_upgrade_energy_consumption = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 25}
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

        self.building_cue = 0
        self.specials = kwargs.get("specials", [])
        self.specials_dict = {
            "energy": {"operator": "", "value": 0},
            "food": {"operator": "", "value": 0},
            "minerals": {"operator": "", "value": 0},
            "water": {"operator": "", "value": 0},
            "population": {"operator": "", "value": 0},
            "technology": {"operator": "", "value": 0},
            "population_grow_factor": {"operator": "", "value": 0}
            }
        self.possible_resources = kwargs.get("possible_resources")

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "population": 0.0,
            "technology": 0
            }

        # population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # production score
        self.production_scores = {}
        self.production_scores_sums = {}
        self.lowest_production_score_keys = []
        self.highest_production_score_keys = []


        # resource score
        self.resource_scores = {}
        self.resource_scores_sums = {}
        self.lowest_resource_score_keys = []
        self.highest_resource_score_keys = []


        # combined score
        self.combined_scores = {}
        self.combined_scores_sums = {}
        self.lowest_combined_score_keys = []
        self.highest_combined_score_keys = []

    def __repr__(self):
        # return f"production_scores: {self.production_scores}\nself.production_scores_sums: {self.production_scores_sums}\nself.lowest_production_score_keys: {self.lowest_score_keys}\n\n "


        str_ = ""

        str_ += f"self.production_scores: {self.production_scores}\n"
        str_ += f"self.lowest_production_score_keys: {self.lowest_production_score_keys}\n"
        str_ += f"self.lowest_resource_score_keys: {self.lowest_resource_score_keys}\n"
        str_ += f"self.lowest_combined_score_keys: {self.lowest_combined_score_keys}\n"

        str_ += f"self.highest_production_score_keys: {self.highest_production_score_keys}\n"
        str_ += f"self.highest_resource_score_keys: {self.highest_resource_score_keys}\n"
        str_ += f"self.highest_combined_score_keys: {self.highest_combined_score_keys}\n"

        return str_

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value
        if self._population < 1:
            self._population = 0

    def update_planet_resources(self, checkbox_values):
        # get new values
        resources = ["water", "energy", "food", "minerals", "technology", "population"]
        self.possible_resources = [i for i in checkbox_values if i in resources]

    def calculate_production(self):
        self.production = economy_handler.calculate_planet_production(self)
        self.production["energy"] -= get_sum_up_to_n(
                self.building_slot_upgrade_energy_consumption,
                self.building_slot_upgrades + 1)

        self.calculate_population()

        # self.update_displays()

    # def update_displays(self):
    #     if hasattr(self.planet, "set_thumpsup_status"):
    #         self.planet.set_thumpsup_status()
    #         self.planet.set_smiley_status()
    #         self.planet.set_technology_level_status()
    #         self.planet.set_overview_images()

    def calculate_population(self):
        """ calculates population"""
        # if self.production["food"] > 0:
        self.population_grow = self.population_grow_factor * self.production["food"]  # * config.game_speed

        if self.population < 0:
            self.population = 0

        # danger!!! might destroy everything
        self.production["population"] = self.population_grow  # * config.game_speed

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildings:
        "town":1000,  "city":10000, "metropole":100000
        """
        self.population_limit = sum([self.population_buildings_values[i] for i in self.buildings if
                                     i in self.population_buildings])

    def set_technology_upgrades(self, building):
        upgrade = building_factory.get_technology_upgrade(building)
        for key, value in upgrade.items():
            setattr(self, key, getattr(self, key) + value)

    def add_population(self):
        if self.population_limit > self.population and self.production["food"] > 0:
            self.population += self.production["population"] * config.game_speed

    def calculate_percentage(self, base_value, value):
        """
        Calculate the percentage of a value relative to a base value.

        :param base_value: The value representing 100%
        :param value: The value to calculate the percentage for
        :return: The calculated percentage as a float
        """
        if value == 0:
            value = 100
        if base_value == 0:
            base_value = 100

        return (value / base_value) * 100

    def get_dict_difference(self, dict_: dict, dict_1: dict) -> dict:
        """ returns the difference between dict_ and dict_1 as dict
        """
        differ = {}
        for key, value in dict_.items():
            differ[key] = dict_1[key] - dict_[key]
        return differ

    def update_scores(
            self,
            resources: dict,
            resource_goal: dict,
            production: dict,
            production_goal: dict,
            population: int,
            population_limit: int,
            all_buildings: list,
            all_building_slots: int
            ) -> None:

        # get all stuff
        resource_differ = self.get_dict_difference(resources, resource_goal)
        resource_differ_max = max(resource_differ.values())
        resource_differ_max_keys = [i for i in resources if resource_differ[i] == resource_differ_max]

        production_differ = self.get_dict_difference(production, production_goal)
        production_differ_max = max(production_differ.values())
        production_differ_max_keys = [i for i in production if production_differ[i] == production_differ_max]

        population_limit = 1 if self.population_limit == 0 else self.population_limit
        population = 1 if self.population == 0 else self.population

        space_harbor_count = len([i for i in self.buildings if i == "space harbor"])
        ships_count = len([i for i in self.buildings if i in ["spaceship", "cargoloader", "spacehunter"]])

        # calculate every buildings score
        for building in building_factory.get_all_building_names():
            # get all buildings dicts
            building_production_dict = building_factory.get_production_from_buildings_json(building)

            # create tmp dict
            tmp_production_scores = {}
            tmp_resource_scores = {}
            tmp_combined_scores = {}
            for key, value in building_production_dict.items():
                resource_differ_current = resource_differ[key]
                resource_differ_current_percent = self.calculate_percentage(resource_differ_max, resource_differ_current)

                production_differ_current = value + production[key]
                production_differ_current_percent = self.calculate_percentage(production_differ_max, production_differ_current)

                tmp_production_scores[key] = production_differ_current_percent
                tmp_resource_scores[key] = resource_differ_current_percent
                tmp_combined_scores[key] = (resource_differ_current_percent + production_differ_current_percent) / 2

                # self.production_scores[building][key] = (resource_differ_current_percent + production_differ_current_percent)/2
                # print (f"key:{key}: resource_differ_current: {resource_differ_current}, resource_differ_current_percent: {resource_differ_current_percent},production_differ_current: {production_differ_current},production_differ_current_percent:{production_differ_current_percent}  ")

            # set scores
            self.production_scores[building] = tmp_production_scores
            self.resource_scores[building] = tmp_resource_scores
            self.combined_scores[building] = tmp_combined_scores

            # set sums
            self.production_scores_sums = self.update_sums(self.production_scores)
            self.resource_scores_sums = self.update_sums(self.resource_scores)
            self.combined_scores_sums = self.update_sums(self.combined_scores)

            # set lowest_keys
            self.lowest_production_score_keys = self.update_lowest_score_keys(self.production_scores_sums)
            self.lowest_resource_score_keys = self.update_lowest_score_keys(self.resource_scores_sums)
            self.lowest_combined_score_keys = self.update_lowest_score_keys(self.combined_scores_sums)

            # set highest_keys
            self.highest_production_score_keys= self.update_highest_score_keys(self.production_scores_sums)
            self.highest_resource_score_keys = self.update_highest_score_keys(self.resource_scores_sums)
            self.highest_combined_score_keys = self.update_highest_score_keys(self.combined_scores_sums)


    def update_sums(self, scores: dict):
        # get sums
        sums_ = {}
        len_ = len(scores.keys())
        for building, score in scores.items():
            sums_[building] = {}
            for key, value in score.items():
                if not key in sums_[building].keys():
                    sums_[building][key] = 0
                sums_[building][key] += value / len_
        return sums_



    def update_lowest_score_keys(self, sums_:dict):
        # get min_value
        min_value = 10000.0
        min_keys = []
        for building, scores in sums_.items():
            for key, value in scores.items():
                if value < min_value:
                    min_value = value

        # get min_value_keys
        for building, scores in sums_.items():
            for key, value in scores.items():
                if value == min_value:
                    if not key in min_keys:
                        min_keys.append(key)
        return min_keys

    def update_highest_score_keys(self, sums_: dict):
        # get min_value
        max_value = 0.0
        max_keys = []
        for building, scores in sums_.items():
            for key, value in scores.items():
                if value > max_value:
                    max_value = value

        # get min_value_keys
        for building, scores in sums_.items():
            for key, value in scores.items():
                if value == max_value:
                    if not key in max_keys:
                        max_keys.append(key)
        return max_keys


class EconomyCalculator:

    def __init__(self):
        self.settings = load_file("auto_economy_calculator_settings.json", "config")
        self.building_scores = None
        self.sum_ = None
        self.lowest_score_keys = None
        self.building_production_scores = None
        self.building_production_scores_sums = None
        self.building_score_sums = None

    def __repr__(self):
        str_ = "EconomyCalculator :\n\n"
        for key, value in self.__dict__.items():
            str_ += f"  key: {key}, value: {value}\n"

        return str_

    def calculate_percentage(self, base_value, value):
        """
        Calculate the percentage of a value relative to a base value.

        :param base_value: The value representing 100%
        :param value: The value to calculate the percentage for
        :return: The calculated percentage as a float
        """
        return (value / base_value) * 100

    def calculate_production_score(self, economy_agent, building) -> dict:
        player = config.app.players[economy_agent.planet.owner]
        production_goal = {key.split("production_")[1]: value for key, value in economy_calculator.settings.items()
                           if key.startswith("production")}
        resource_goal = {key.split("resource_")[1]: value for key, value in economy_calculator.settings.items()
                         if key.startswith("resource")}

        # get all buildings dicts
        building_dict = building_factory.get_production_from_buildings_json(building)
        resource_differ = self.get_dict_difference(player.get_stock(), resource_goal)
        resource_differ_max = max(resource_differ.values())
        resource_differ_max_keys = [i for i in player.get_stock() if resource_differ[i] == resource_differ_max]

        production_differ = self.get_dict_difference(economy_agent.production, production_goal)
        production_differ_max = max(production_differ.values())
        production_differ_max_keys = [i for i in economy_agent.production if
                                      production_differ[i] == production_differ_max]

        population_limit = 1 if economy_agent.population_limit == 0 else economy_agent.population_limit
        population = 1 if economy_agent.population == 0 else economy_agent.population

        space_harbor_count = len([i for i in economy_agent.buildings if i == "space harbor"])
        ships_count = len([i for i in economy_agent.buildings if i in ["spaceship", "cargoloader", "spacehunter"]])
        new_dict = {}

        for key, value in building_dict.items():
            if key in resource_differ_max_keys:
                current_production_value = player.production[key]
                production_to_goal_differ = value + current_production_value
                category = building_factory.get_category_by_building(building)
                category_buildings = building_factory.get_building_names(category)
                new_dict[
                    key] = self.calculate_percentage(100, production_to_goal_differ / resource_differ_max if resource_differ_max != 0 else 1)
            else:
                new_dict[key] = self.calculate_percentage(100, value + player.production[key])

        # calculate building_scores
        building_scores = {
            key: abs(production_goal[key] - new_dict[key]) for key in
            production_goal.keys()}

        self.building_scores = building_scores
        # print (f"building: {building}, building_scores: {building_scores}")
        return building_scores

    def get_production_sum_score(
            self,
            building: str,
            population_limit: int,
            population: int,
            scores: dict,
            building_dict: dict
            ) -> float:

        # get sum
        sum_ = sum(value for value in scores.values())

        # limit sum to population, buildings that cannot be built because the population is not sufficient
        if building_factory.get_build_population_minimum(building) > population:
            sum_ = 100

        # limit unproductive buildings
        if all(value == 0 for value in building_dict.values()):
            sum_ = 90

        self.sum_ = sum_
        return sum_

    def get_lowest_score_keys(self, economy_agent) -> list:
        """ returns a list of all keys from building_score_sums that have the lowest value
        """

        min_value = min(economy_agent.building_production_scores_sums.values())

        # get the lowest valued buildings == the best one
        lowest_score_keys = [key for key, value in economy_agent.building_production_scores_sums.items() if
                             value == min_value]
        self.lowest_score_keys = lowest_score_keys
        return lowest_score_keys

    def get_dict_difference(self, dict_: dict, dict_1: dict) -> dict:
        """ returns the difference between dict_ and dict_1 as dict
        """
        differ = {}
        for key, value in dict_.items():
            differ[key] = dict_1[key] - dict_[key]
        return differ

    def calculate_building_production_scores(self, economy_agent) -> dict:
        building_production_scores = {}
        for building in building_factory.get_all_building_names():
            building_production_score = self.calculate_production_score(economy_agent, building)

            building_production_scores[building] = building_production_score

        self.building_production_scores = building_production_scores
        return building_production_scores

    def calculate_building_scores_sums(self, economy_agent) -> dict:
        building_production_scores_sums = {}

        for building, scores in economy_agent.building_production_scores.items():
            building_production_score_sum_ = self.get_production_sum_score(
                    building=building,
                    population_limit=economy_agent.population_limit,
                    population=economy_agent.population,
                    scores=scores,
                    building_dict=building_factory.get_production_from_buildings_json(building))
            building_production_scores_sums[building] = building_production_score_sum_
        self.building_production_scores_sums = building_production_scores_sums
        economy_agent.building_production_scores_sums = building_production_scores_sums
        return building_production_scores_sums

    def calculate_lowest_production_score_keys(
            self,
            economy_agent,
            ) -> list:

        economy_agent.building_production_scores = self.calculate_building_production_scores(economy_agent)
        economy_agent.building_production_scores_sums = self.calculate_building_scores_sums(economy_agent)
        economy_agent.lowest_score_keys = self.get_lowest_score_keys(economy_agent)
        return economy_agent.lowest_score_keys


economy_calculator = EconomyCalculator()


def main():
    resources = {
        "energy": 1000,
        "food": 1000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 1000
        }
    resource_goal = {
        "energy": 1000,
        "food": 1000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 1000
        }

    production = {
        "energy": 1,
        "food": 1,
        "minerals": 1,
        "water": 1,
        "technology": 1,
        "population": 1
        }
    production_goal = {
        "energy": 1,
        "food": 2,
        "minerals": 1,
        "water": 1,
        "technology": 1,
        "population": 1
        }

    population = 129
    population_limit = 1000
    all_buildings = 190
    all_building_slots = 200

    economy_agent = EconomyAgent()

    economy_agent.update_scores(resources, resource_goal, production, production_goal, population, population_limit, all_buildings, all_building_slots)
    # pprint(economy_agent.__repr__())

    # get_best_fitting_building = economy_calculator.calculate_lowest_production_score_keys(economy_agent)
    # print(f"get_best_fitting_building: {get_best_fitting_building}")

    print (f"economy_agent.production_scores['farm']: {economy_agent.production_scores['farm']}")
    print(f"economy_agent.production_scores_sums['farm']: {economy_agent.production_scores_sums['farm']}")
    print(f"economy_agent.lowest_production_score_keys: {economy_agent.lowest_production_score_keys}")
    print(f"economy_agent.highest_production_score_keys: {economy_agent.highest_production_score_keys}")


    print (f"economy_agent.resource_scores['farm']: {economy_agent.resource_scores['farm']}")
    print(f"economy_agent.resource_scores_sums['farm']: {economy_agent.resource_scores_sums['farm']}")

    print(f"economy_agent.combined_scores['farm']: {economy_agent.combined_scores['farm']}")
    print(f"economy_agent.combined_scores_sums['farm']: {economy_agent.combined_scores_sums['farm']}")


if __name__ == "__main__":
    main()
