from pprint import pprint

from source.auto_economy_rebuild.player import Player


def main():
    # player data
    player = Player()

    # planet data
    planet = player.economy_agents[0]
    planet.population = 0
    planet.population_limit = 0
    planet.possible_resources = ["food", "energy", "water", "population"]

    resource_goal = {
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
        "population": 1
        }

    planet.implement_production_scores(player, production_goal)
    planet.implement_production_scores_sum()

    planet.implement_production_scores_percent()
    planet.implement_production_scores_sum_percent()
    planet.implement_production_penalties(player, planet)


    # planet.implement_resource_scores(player, resource_goal)
    # planet.implement_resource_scores_sum()
    pprint (planet.economy_scores)
    print(planet.get_highest_production_sum_percent())

    # new_dict = calculate_sconomy_scores(player, planet, production_goal, resource_goal)
    # # pprint(new_dict)
    # pprint({key:value["scores"]["total_scores_percent"] for key,value in new_dict.items() if not value["scores"]["total_scores_percent"] == 100})
    #
    # total_scores = [value["scores"]["total_scores_percent"] for key, value in new_dict.items()]
    # min_scores = min(total_scores)
    # max_scores = max(total_scores)
    #
    # min_keys = [key for key, value in new_dict.items() if value["scores"]["total_scores_percent"] == min_scores]
    # max_keys = [key for key, value in new_dict.items() if value["scores"]["total_scores_percent"] == max_scores]
    # print(f"most probable: {min_keys}, most unlikely: {max_keys}")


if __name__ == "__main__":
    main()
