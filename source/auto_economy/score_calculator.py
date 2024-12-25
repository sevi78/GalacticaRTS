from source.factories.building_factory import building_factory


class ScoreCalculator:
    def __init__(self, economy_agent):
        self.economy_agent = economy_agent
        self.building_dicts = building_factory.get_all_building_dicts()
        self.economy_scores = {}
        self.lowest_production_score_keys = []
        self.building_production_scores_sums = {key: 100 for key in building_factory.get_all_building_names()}

    def __repr____(self):
        str_ = ""
        for building_name, building_dict in self.economy_scores.items():
            str_ += f"{building_name}:{self.economy_scores[building_name]['production_sum_percent']}\n"

        return str_

    def __repr__(self):
        sorted_items = sorted(
                self.economy_scores.items(),
                key=lambda x: x[1]['production_sum_percent'],
                reverse=True
                )

        str_ = ""
        for building_name, building_dict in sorted_items:
            str_ += f"{building_name}: {building_dict['production_sum_percent']}{building_dict}\n"

        return str_

    def calculate_percentage(self, maximum, value):
        """
        Calculate the percentage of a value relative to a base value.

        :param base_value: The value representing 100%
        :param value: The value to calculate the percentage for
        :return: The calculated percentage as a float
        """
        if value == 0:
            return 0
        if maximum == 0:
            return 0

        return (value / maximum) * 100

    def implement_production_scores(self, player, production_goal):
        production = player.production
        # implement scores
        for building_name, building_dict in self.building_dicts.items():
            for key, value in building_dict.items():
                if key.startswith("production_"):
                    key_ = key.split("production_")[1]
                    if not building_name in self.economy_scores.keys():
                        self.economy_scores[building_name] = {"production": {}}

                    self.economy_scores[building_name]["production"][key_] = production_goal[key_] - production[
                        key_] + value

    def implement_production_scores_sum(self):
        # implement scores
        for building_name, building_dict in self.economy_scores.items():
            self.economy_scores[building_name]["production_sum"] = sum(
                    self.economy_scores[building_name]["production"].values())

    def implement_production_penalties(self, player, planet):

        # print (f"planet.population_buildings: {[i for i in planet.buildings if building_factory.get_category_by_building(i) == 'population']}")
        # print (planet.population_limit)
        categories = ["planetary_defence", "ship", "weapons"]
        # implement penalties
        for building_name, building_dict in self.building_dicts.items():
            # university
            if building_name == "university":
                differ = player.get_all_building_slots() - len(player.get_all_buildings())
                self.economy_scores[building_name]["production_sum_percent"] /= differ if differ > 0 else 1

            # build_population_minimum or category penalty
            if building_dict["build_population_minimum"] > planet.population:
                # del (building_name, building_dict)
                self.economy_scores[building_name]["production_sum_percent"] = 0

            # category penalty
            if not building_dict["category"] in planet.possible_resources + categories:
                self.economy_scores[building_name]["production_sum_percent"] = 0

            # population
            if building_dict["category"] == "population":
                if planet.population < 1000:
                    if building_name in ["city", "metropole"]:
                        self.economy_scores[building_name]["production_sum_percent"] = 0

                if planet.population < 10000:
                    if building_name in ["metropole"]:
                        self.economy_scores[building_name]["production_sum_percent"] = 0

                # population buildings limitation
                if planet.population_limit != 0:
                    if planet.population <= planet.population_limit:
                        if building_name in building_factory.get_building_names("population"):
                            self.economy_scores[building_name]["production_sum_percent"] = 0

                if player.population_limit > player.stock["population"]:
                    self.economy_scores[building_name]["production_sum_percent"] = 0

            # space harbor
            if building_name == "space harbor":
                if "space harbor" in player.get_all_buildings():
                    self.economy_scores[building_name]["production_sum_percent"] = 0

            # food penalty/boost
            if building_dict["category"] == "population":

                # self.economy_scores[building_name]["production_sum_percent"] = 0
                if not "food" in planet.possible_resources:
                    self.economy_scores[building_name]["production_sum_percent"] = 0
                    if not "population" in planet.possible_resources:
                        self.economy_scores[building_name]["production_sum_percent"] = 0

            if building_dict["category"] == "food":
                if ("food" in planet.possible_resources) and ("population" in planet.possible_resources):
                    self.economy_scores[building_name]["production_sum_percent"] *= 1.2

            # ship
            if building_dict["category"] == "ship":
                if len([i for i in player.get_all_buildings() if i == "space harbor"]) == 0:
                    self.economy_scores[building_name]["production_sum_percent"] = 0

            # planetary defence
            if building_dict["category"] == "planetary_defence":
                if len([i for i in player.get_all_buildings() if i == "particle accelerator"]) == 0:
                    self.economy_scores[building_name]["production_sum_percent"] = 0

            # weapon
            if building_dict["category"] == "weapons":
                all_ships = player.get_all_ships()
                if len(all_ships) > 0:
                    # if len([i for i in all_ships if i.energy <=0]) > 0:
                    pass

                else:
                    self.economy_scores[building_name]["production_sum_percent"] = 0

    def implement_production_scores_percent(self):
        for building_name, building_dict in self.economy_scores.items():
            max_ = max(building_dict["production"].values())
            self.economy_scores[building_name]["production_percent"] = {
                key: 100 - self.calculate_percentage(max_, abs(value)) for key, value in
                building_dict["production"].items()}

    def implement_production_scores_sum_percent(self):
        for building_name, building_dict in self.economy_scores.items():
            self.economy_scores[building_name]["production_sum_percent"] = sum(
                    self.economy_scores[building_name]["production_percent"].values()) / len(
                    self.economy_scores[building_name]["production_percent"].keys())

    def get_highest_production_sum_percent(self):
        max_value = 0
        max_buildings = []
        for building_name, building_dict in self.economy_scores.items():
            if building_dict["production_sum_percent"] > max_value:
                max_value = building_dict["production_sum_percent"]

        for building_name, building_dict in self.economy_scores.items():
            if building_dict["production_sum_percent"] == max_value:
                max_buildings.append(building_name)

        return max_buildings

    def get_highest_total_sum_percent(self):
        max_value = 0
        max_buildings = []
        for building_name, building_dict in self.economy_scores.items():
            if building_dict["total_sum_percent"] > max_value:
                max_value = building_dict["total_sum_percent"]

        for building_name, building_dict in self.economy_scores.items():
            if building_dict["total_sum_percent"] == max_value:
                max_buildings.append(building_name)

        return max_buildings

    def get_lowest_production_sum_percent(self):
        min_value = float("inf")
        mim_buildings = []
        for building_name, building_dict in self.economy_scores.items():
            if building_dict["production_sum_percent"] < min_value:
                min_value = building_dict["production_sum_percent"]

        for building_name, building_dict in self.economy_scores.items():
            if building_dict["production_sum_percent"] == min_value:
                mim_buildings.append(building_name)

        return mim_buildings

    def implement_total_score(self):
        for building_name, building_dict in self.economy_scores.items():
            self.economy_scores[building_name]["total_sum_percent"] = (building_dict["production_sum_percent"] +
                                                                       building_dict["resource_sum_percent"]) / 2

            # self.economy_scores[building_name]["total_sum_percent"] = building_dict["production_sum_percent"]

    def implement_resource_scores(self, player, resource_goal):

        # implement scores
        for building_name, building_dict in self.building_dicts.items():
            for key, value in building_dict.items():
                if key.startswith("price_"):
                    key_ = key.split("price_")[1]
                    if not building_name in self.economy_scores.keys():
                        self.economy_scores[building_name] = {"resource": {}}
                    if not "resource" in self.economy_scores[building_name].keys():
                        self.economy_scores[building_name]["resource"] = {}

                    self.economy_scores[building_name]["resource"][key_] = resource_goal[key_] + value

    def implement_resource_scores_percent(self):
        for building_name, building_dict in self.economy_scores.items():
            max_ = max(building_dict["resource"].values())
            self.economy_scores[building_name]["resource_percent"] = {
                key: 100 - self.calculate_percentage(max_, abs(value)) for key, value in
                building_dict["resource"].items()}

    def implement_resource_scores_sum(self):
        # implement scores
        for building_name, building_dict in self.economy_scores.items():
            self.economy_scores[building_name]["resource_sum"] = sum(
                    self.economy_scores[building_name]["resource"].values())

    def implement_resource_scores_sum_percent(self):
        for building_name, building_dict in self.economy_scores.items():
            self.economy_scores[building_name]["resource_sum_percent"] = sum(
                    self.economy_scores[building_name]["resource_percent"].values()) / len(
                    self.economy_scores[building_name]["resource_percent"].keys())
