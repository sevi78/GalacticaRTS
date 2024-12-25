import copy
from pprint import pprint

from source.economy.EconomyAgent import EconomyAgent
from source.factories.building_factory import building_factory


class Player:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "population": 0
            }

        self.population_limit = 0
        self.buildings = []
        self.stock = {
            "energy": 1000,
            "food": 1000,
            "minerals": 1000,
            "water": 1000,
            "technology": 1000,
            "population": 1000
            }

        self.economy_agents = [EconomyAgent(self), EconomyAgent(self), EconomyAgent(self)]
        self.ships = []

    def get_stock(self) -> dict:
        return self.stock

    def get_all_buildings(self) -> list:
        buildings = []
        for i in self.economy_agents:
            buildings += i.buildings
        return buildings

    def get_all_building_slots(self) -> int:
        """
        returns the sum of all buildings_slots of all planets of the player:
        - the maximum of buildings can be built
        """
        slots = sum([i.buildings_max for i in self.economy_agents])
        return slots

    def set_population_limit(self) -> None:
        population_buildings = ["town", "city", "metropole"]
        population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        self.population_limit = sum([population_buildings_values[i] for i in self.buildings if
                                     i in population_buildings])

    def get_population_limit(self):
        self.set_population_limit()
        return self.population_limit

    def set_global_population(self) -> None:
        self.stock["population"] = int(sum([i.population for i in self.economy_agents]))


# class EconomyScore:
#     def __init__(self, maximum: float, value: float):
#         self.maximum = maximum
#         self.value = value
#
#         if (not self.maximum == 0) and (not self.value == 0):
#             self.percentage = 100 / maximum * value
#         else:
#             self.percentage = 0
#
#     def __repr__(self):
#         return str(self.percentage)


def sort_dict_by_key(data, key_: str) -> dict:
    def calculate_total_price(item):
        return sum(value for key, value in item.items() if key.startswith(key_))

    sorted_items = sorted(data.items(), key=lambda x: calculate_total_price(x[1]), reverse=True)
    return dict(sorted_items)


# production
def add_score(dict_, key_):
    sorted_dict = sort_dict_by_key(dict_, key_)
    scored_dict = copy.deepcopy(sorted_dict)
    for k_, value in sorted_dict.items():
        scored_dict[k_]["total_" + key_] = sum(v for k, v in value.items() if k.startswith(key_))

    return scored_dict


"""
"mine": {
      "name": "mine",
      "category": "minerals",
      "production_energy": -2,
      "production_food": -1,
      "production_minerals": 1,
      "production_water": -1,
      "production_technology": 0,
      "production_population": 0,
      "price_energy": 10,
      "price_food": 5,
      "price_minerals": 10,
      "price_water": 5,
      "price_technology": 0,
      "price_population": 0,
      "build_population_minimum": 0,
      "building_production_time_scale": 5,
      "building_production_time": 25,
      "population_buildings_value": 0,
      "technology_upgrade": {}
    },
"""

# def implement_production_score(player, planet, production_goal, resource_goal) -> dict:
#     dict_ = building_factory.get_all_building_dicts()
#     scores = {}
#
#     for building_name, building_dict in new_dict.items():



def calculate_score(player, planet, production_goal, resource_goal, new_dict) -> dict:

    """
    the lower the values, the more probable is the building for the goal:
    possible variables:
    planet.population
    planet.population_limit
    planet.buildings
    planet.buildings_max
    planet.possible_resources

    player.population
    player.population_limit
    player.buildings
    player.building_slots

    possible scores:

    """
    tmp_dict = copy.deepcopy(new_dict)

    # implement scores
    for building_name, building_dict in new_dict.items():
        for key, value in building_dict.items():
            if not "scores" in tmp_dict[building_name].keys():
                tmp_dict[building_name]["scores"] = {}
                tmp_dict[building_name]["scores"]["production_goal"] = production_goal
                tmp_dict[building_name]["scores"]["resource_goal"] = resource_goal

            # implement production score
            if key.startswith("production_"):
                # implement build_population_minimum
                if planet.population < building_dict["build_population_minimum"]:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = 100

                # implement category penalty
                elif not building_dict["category"] in planet.possible_resources:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = 100
                else:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = production_goal[
                                                                                 key.split("production_")[1]] - value
            # implement resource_score
            if key.startswith("price_"):
                # implement build_population_minimum
                if planet.population < building_dict["build_population_minimum"]:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = 100

                # implement category penalty
                elif not building_dict["category"] in planet.possible_resources:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = 100
                else:
                    tmp_dict[building_name]["scores"][f"difference_{key}"] = resource_goal[
                                                                                 key.split("price_")[1]] + value
            # implement planet_population_score
            tmp_dict[building_name]["scores"]["planet_population_score"] = planet.population_limit - planet.population

    # get the max values
    for building_name, building_dict in tmp_dict.items():
        # production_max
        production_values = [value for key, value in building_dict["scores"].items() if
                             key.startswith("difference_production_")]
        production_values_max = max(production_values)
        tmp_dict[building_name]["scores"][f"difference_production_max"] = production_values_max
        tmp_dict[building_name]["scores"][f"production_difference_sum"] = sum(production_values)

        # resource_max
        resource_values = [value for key, value in building_dict["scores"].items() if
                           key.startswith("difference_price_")]
        resource_values_max = max(resource_values)
        tmp_dict[building_name]["scores"][f"difference_price_max"] = resource_values_max
        tmp_dict[building_name]["scores"][f"resource_difference_sum"] = sum(resource_values)

    # implement percentage score
    percentage_dict = copy.deepcopy(tmp_dict)

    for building_name, building_dict in tmp_dict.items():
        # total score
        percentage_dict[building_name]["scores"]["total_scores_percent"] = 0
        score_count = 0

        for key, value in building_dict["scores"].items():
            # production
            if key.startswith("difference_production"):
                if not key == "difference_production_max":
                    # implement category penalty
                    if not building_dict["category"] in planet.possible_resources:
                        percentage_dict[building_name]["scores"][f"{key}_percentage"] = 100
                    else:

                        percentage_dict[building_name]["scores"][f"{key}_percentage"] = 100 / tmp_dict[building_name][
                            "scores"][
                            "difference_production_max"] * value if not value == 0 else 1
                        percentage_dict[building_name]["scores"]["total_scores_percent"] += \
                            percentage_dict[building_name]["scores"][f"{key}_percentage"]
                    score_count += 1

            # resources
            if key.startswith("difference_price"):
                if not key == "difference_price_max":
                    # implement category penalty
                    if not building_dict["category"] in planet.possible_resources:
                        percentage_dict[building_name]["scores"][f"{key}_percentage"] = 100
                    else:
                        percentage_dict[building_name]["scores"][f"{key}_percentage"] = 100 / tmp_dict[building_name][
                            "scores"][
                            "difference_price_max"] * value
                        percentage_dict[building_name]["scores"]["total_scores_percent"] += \
                            percentage_dict[building_name]["scores"][f"{key}_percentage"]
                    score_count += 1

        # total score
        percentage_dict[building_name]["scores"]["total_scores_percent"] /= score_count

    new_dict = percentage_dict
    return new_dict


def calculate_sconomy_scores(player, planet, production_goal, resource_goal) -> dict:
    # building dict
    factory = building_factory
    all_buildings_dict = factory.get_all_building_dicts()

    # implement scores
    new_dict = calculate_score(player, planet, production_goal, resource_goal, all_buildings_dict)
    return new_dict


def main():
    # test case


    # player data
    player = Player()
    player_production = {
        "energy": 0,
        "food": 0,
        "minerals": 0,
        "water": 0,
        "technology": 0,
        "population": 0
        }

    player_resources = {
        "energy": 1000,
        "food": 1000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 1000
        }

    # planet data
    planet = player.economy_agents[0]
    planet.population = 0
    planet.population_limit = 0


    planet.possible_resources = ["food", "energy", "water", "population"]

    planet_production = {
        "energy": 0,
        "food": 0,
        "minerals": 0,
        "water": 0,
        "technology": 0,
        "population": 0
        }

    resource_goal = {
        "energy": 1000,
        "food": 1000,
        "minerals": 1000,
        "water": 1000,
        "technology": 1000,
        "population": 1000
        }

    production_goal = {
        "energy": 3,
        "food": 3,
        "minerals": 3,
        "water": 3,
        "technology": 3,
        "population": 3
        }

    new_dict = calculate_sconomy_scores(player, planet, production_goal, resource_goal)
    # pprint(new_dict)
    pprint({key:value["scores"]["total_scores_percent"] for key,value in new_dict.items() if not value["scores"]["total_scores_percent"] == 100})

    total_scores = [value["scores"]["total_scores_percent"] for key, value in new_dict.items()]
    min_scores = min(total_scores)
    max_scores = max(total_scores)

    min_keys = [key for key, value in new_dict.items() if value["scores"]["total_scores_percent"] == min_scores]
    max_keys = [key for key, value in new_dict.items() if value["scores"]["total_scores_percent"] == max_scores]
    print(f"most probable: {min_keys}, most unlikely: {max_keys}")


if __name__ == "__main__":
    main()
