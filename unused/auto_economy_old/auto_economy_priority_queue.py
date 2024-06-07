from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file

PARTICLE_ACCELERATOR_BUILD_THRESHOLD = 10000
PARTICLE_ACCELERATOR_AMOUNT = 1
SPACE_HARBOR_AMOUNT = 1
PLANETARY_DEFENCE_AMOUNT = 1
MIN_TECH_PRODUCTION_THRESHOLD = 0


class PriorityQueueConditions:
    def __init__(self, player):
        self.player = player
        # planet specific conditions
        self.planet_has_any_buildings = False
        self.planet_has_buildings_max_reached = False
        self.planet_has_population_max_reached = False
        self.planet_population_is_min_1000 = False
        self.planet_population_is_min_10000 = False
        self.planet_population_is_min_100000 = False
        self.planet_has_space_harbor = False
        self.planet_has_particle_accelerator = False

        self.planet_can_build_energy = False
        self.planet_can_build_food = False
        self.planet_can_build_minerals = False
        self.planet_can_build_technology = False
        self.planet_can_build_population = False
        # self.planet_can_build_particle_accelerator = False

        # player specific conditions
        self.negative_stock = False
        self.negative_production = False
        self.average_stock_is_min_1000 = False
        self.average_stock_is_min_10000 = False
        self.technology_is_min_1 = False
        self.player_population_is_min_1000 = False
        self.player_population_is_min_10000 = False
        self.player_population_is_min_100000 = False
        self.player_has_buildings_max_reached = False
        self.player_has_population_max_reached = False
        self.player_average_production_is_min_0 = False
        self.player_average_production_is_min_3 = False
        self.player_average_production_is_min_5 = False
        self.player_average_production_is_min_10 = False

    def __str__(self):
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()])

    def update_planet_conditions(self, planet):
        # planet specific conditions
        self.planet_has_any_buildings = bool(planet.buildings)
        self.planet_has_buildings_max_reached = len(planet.buildings) >= planet.buildings_max
        self.planet_has_population_max_reached = planet.population >= planet.population_limit
        self.planet_population_is_min_1000 = planet.population >= 1000
        self.planet_population_is_min_10000 = planet.population >= 10000
        self.planet_population_is_min_100000 = planet.population >= 100000
        self.planet_has_space_harbor = "space harbor" in planet.buildings
        self.planet_has_particle_accelerator = "particle accelerator" in planet.buildings

        self.planet_can_build_energy = "energy" in planet.possible_resources
        self.planet_can_build_food = "food" in planet.possible_resources
        self.planet_can_build_minerals = "minerals" in planet.possible_resources
        self.planet_can_build_technology = "technology" in planet.possible_resources
        self.planet_can_build_population = "population" and "food" in planet.possible_resources
        # self.planet_can_build_particle_accelerator =

    def update_player_conditions(self):
        production = {key: value for key, value in self.player.production.items() if key != "population"}
        resource_stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        negative_stock_resources = [key for key, value in resource_stock.items() if value < 0]
        negative_production_resources = [key for key, value in self.player.production.items() if value < 0]

        # player specific conditions
        self.negative_stock = any(value < 0 for value in resource_stock.values())
        self.negative_production = any(value < 0 for value in production.values())
        self.average_stock_is_min_1000 = all(value >= 1000 for value in resource_stock.values())
        self.average_stock_is_min_10000 = all(value >= 10000 for value in resource_stock.values())
        self.technology_is_min_1 = self.player.get_resource_stock()["technology"] > 0

        self.player_population_is_min_1000 = self.player.population >= 1000
        self.player_population_is_min_10000 = self.player.population >= 10000
        self.player_population_is_min_100000 = self.player.population >= 100000
        self.player_has_buildings_max_reached = len(self.player.get_all_buildings()) >= self.player.get_all_building_slots()
        self.player_has_population_max_reached = self.player.population >= self.player.get_population_limit()

        self.player_average_production_is_min_0 = all(value >= 0 for value in production.values())
        self.player_average_production_is_min_3 = all(value >= 3 for value in production.values())
        self.player_average_production_is_min_5 = all(value >= 5 for value in production.values())
        self.player_average_production_is_min_10 = all(value >= 10 for value in production.values())


class AutoEconomyHandlerPriorityQueue:# original
    def __init__(self, player):
        self.planet = None
        self.player = player
        self.auto_economy_handler = None
        self.conditions = PriorityQueueConditions(self.player)
        self.planet_task_priorities = {}
        self.player_task_priorities = load_file("economy_queue_settings.json", "config")

        self.highest_priority_key = self.get_highest_priority_keys(self.planet_task_priorities)
        self.priority_values = load_file("economy_queue_settings.json", "config")

    def __repr__(self):
        return str(self.get_highest_priority_keys(
                self.planet_task_priorities[self.planet.id])) if self.planet else "None"

    def update_priorities(self, planets):
        """
        this sets the task priorities for the planets:
        """
        self.conditions.update_player_conditions()
        self.set_player_task_priorities()

        for planet in planets:
            self.conditions.update_planet_conditions(planet)
            self.set_planet_task_priorities(planet)

        # pprint(str(self.conditions))

    def init_planet_priorities(self, planet):
        if not planet.id in self.planet_task_priorities.keys():
            self.planet_task_priorities[planet.id] = {}
            for key, value in self.priority_values.items():
                self.planet_task_priorities[planet.id][key] = 0

    def set_player_task_priorities(self):
        """ this is the sum of all planet_task_priorities"""
        len_ = len(self.planet_task_priorities.keys())
        for key, value in self.player_task_priorities.items():
            self.player_task_priorities[key] = 0

        for id_ in self.planet_task_priorities.keys():
            for key, value in self.planet_task_priorities[id_].items():
                self.player_task_priorities[key] += int(value / len_)

    def set_planet_task_priorities__(self, planet):
        self.planet = planet
        self.player = config.app.players[planet.owner]
        self.auto_economy_handler = self.player.auto_economy_handler

        production = {key: value for key, value in self.player.production.items() if key != "population"}
        resource_stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        negative_stock = any(value < 0 for value in resource_stock.values())
        negative_production = any(value < 0 for value in production.values())
        negative_stock_resources = [key for key, value in resource_stock.items() if value < 0]
        negative_production_resources = [key for key, value in self.player.production.items() if value < 0]

        self.init_planet_priorities(planet)

        # handle negative_stock/negative_production
        if negative_stock:
            for resource in negative_stock_resources:
                self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values[
                    "destroy_most_consuming_building"]
                self.planet_task_priorities[self.planet.id]["delete_buildings"] += self.priority_values[
                    "delete_buildings"]
                self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values[
                    "deal_with_the_bank"]
                # self.planet_task_priorities[self.planet.id]["optimize_planets"] -= 1
        else:
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] -= self.priority_values[
                "destroy_most_consuming_building"]
            self.planet_task_priorities[self.planet.id]["delete_buildings"] -= self.priority_values["delete_buildings"]
            self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] -= self.priority_values[
                "deal_with_the_bank"]

        if negative_production:
            for resource in negative_production_resources:
                self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values[
                    "destroy_most_consuming_building"]
                self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values[
                    "optimize_planets"]
                self.planet_task_priorities[self.planet.id]["build_fitting_building"] += self.priority_values[
                    "build_fitting_building"]
        else:
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] -= self.priority_values[
                "destroy_most_consuming_building"]
            self.planet_task_priorities[self.planet.id]["delete_buildings"] -= self.priority_values["delete_buildings"]
            self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] -= self.priority_values[
                "deal_with_the_bank"]

        if negative_stock_resources and negative_production_resources:
            if self.player.get_resource_stock()["technology"] > 0:
                self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values[
                    "deal_with_the_bank"]
            else:
                self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] -= self.priority_values[
                    "deal_with_the_bank"]

        # handle zero production
        zero_productions = self.auto_economy_handler.get_zero_productions()
        if len(zero_productions) > 0:
            for building in self.planet.buildings:
                category = building_factory.get_category_by_building(building)
                if category in zero_productions:
                    self.planet_task_priorities[self.planet.id]["delete_buildings"] += self.priority_values[
                        "delete_buildings"]
                    self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += \
                        self.priority_values["destroy_most_consuming_building"]
                    self.planet_task_priorities[self.planet.id]["deal_with_the_bank"] += self.priority_values[
                        "deal_with_the_bank"]
                    self.planet_task_priorities[self.planet.id]["optimize_planets"] -= self.priority_values[
                        "optimize_planets"]

        # handle building logic
        if not self.planet.buildings:
            self.planet_task_priorities[self.planet.id]["build_fitting_building"] += self.priority_values[
                "build_fitting_building"]
            self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] -= self.priority_values[
                "destroy_most_consuming_building"]
        else:
            if len(self.planet.buildings) < self.planet.buildings_max:
                self.planet_task_priorities[self.planet.id]["build_fitting_building"] += self.priority_values[
                    "build_fitting_building"]
            else:
                self.planet_task_priorities[self.planet.id]["optimize_planets"] += self.priority_values[
                    "optimize_planets"]
                self.planet_task_priorities[self.planet.id]["delete_buildings"] += self.priority_values[
                    "delete_buildings"]
                self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] += self.priority_values[
                    "destroy_most_consuming_building"]
                self.planet_task_priorities[self.planet.id]["build_university"] += self.priority_values[
                    "build_university"]

        # if has population and food, prior food and population
        if "population" in planet.possible_resources and "food" in planet.possible_resources:
            if planet.population >= planet.population_limit:
                if self.player.population >= self.player.population_limit:
                    self.planet_task_priorities[self.planet.id]["build_population_buildings"] += self.priority_values[
                        "build_population_buildings"]
                    self.planet_task_priorities[self.planet.id]["maximize_population_grow"] += self.priority_values[
                        "maximize_population_grow"]

            else:
                self.planet_task_priorities[self.planet.id]["build_population_buildings"] -= self.priority_values[
                    "build_population_buildings"]
                self.planet_task_priorities[self.planet.id]["maximize_population_grow"] -= self.priority_values[
                    "maximize_population_grow"]

            if planet.production["food"] < 1:
                self.planet_task_priorities[self.planet.id]["build_food_buildings"] += self.priority_values[
                    "build_food_buildings"]
            elif planet.production["food"] < 3:
                self.planet_task_priorities[self.planet.id]["maximize_population_grow"] -= self.priority_values[
                    "maximize_population_grow"]
            else:
                self.planet_task_priorities[self.planet.id]["build_food_buildings"] -= self.priority_values[
                    "build_food_buildings"]
                self.planet_task_priorities[self.planet.id]["maximize_population_grow"] -= self.priority_values[
                    "maximize_population_grow"]

                # if it is possible to build tech buildings
                if "technology" in planet.possible_resources:
                    if not "particle_accelerator" in planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] += \
                            self.priority_values["build_particle_accelerator"]
                    elif not "planetary_defence" in planet.possible_resources:
                        self.planet_task_priorities[self.planet.id]["build_planetary_defence"] += self.priority_values[
                            "build_planetary_defence"]
                else:
                    self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] -= self.priority_values[
                        "build_particle_accelerator"]
                    self.planet_task_priorities[self.planet.id]["build_planetary_defence"] -= self.priority_values[
                        "build_planetary_defence"]

        # if it is possible to build tech buildings
        if "technology" in planet.possible_resources:
            # check for population greater than 10000
            if self.planet.population > PARTICLE_ACCELERATOR_BUILD_THRESHOLD:

                # only prior these building if player has a positive production
                if (not any(value < MIN_TECH_PRODUCTION_THRESHOLD for value in production.values()) or
                        min(value for value in production.values()) > 10000):

                    # space harbor
                    if self.player.get_all_buildings().count("space harbor") < SPACE_HARBOR_AMOUNT:
                        self.planet_task_priorities[self.planet.id]["build_space_harbour"] += self.priority_values[
                            "build_space_harbour"]
                    else:
                        self.planet_task_priorities[self.planet.id]["build_space_harbour"] -= self.priority_values[
                            "build_space_harbour"]

                    # particle accelerator
                    if not "particle accelerator" in self.planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] += \
                            self.priority_values["build_particle_accelerator"]

                    elif not "planetary_defence" in self.planet.buildings:
                        self.planet_task_priorities[self.planet.id]["build_planetary_defence"] += self.priority_values[
                            "build_planetary_defence"]
            else:
                self.planet_task_priorities[self.planet.id]["build_space_harbour"] += self.priority_values[
                    "build_space_harbour"]

        else:
            self.planet_task_priorities[self.planet.id]["build_space_harbour"] -= self.priority_values[
                "build_space_harbour"]
            self.planet_task_priorities[self.planet.id]["build_particle_accelerator"] -= self.priority_values[
                "build_particle_accelerator"]
            self.planet_task_priorities[self.planet.id]["build_planetary_defence"] -= self.priority_values[
                "build_planetary_defence"]

        # build ships
        if "space harbor" in self.planet.buildings:
            self.planet_task_priorities[self.planet.id]["build_ship"] += self.priority_values["build_ship"]
        else:
            self.planet_task_priorities[self.planet.id]["build_ship"] -= self.priority_values["build_ship"]

        # handle special cases
        if len(negative_stock_resources) != 0:
            for resource in negative_stock_resources:
                most_consuming_building = building_factory.get_most_consuming_building(self.auto_economy_handler.all_buildings, resource)
                if not most_consuming_building in self.planet.buildings:
                    self.planet_task_priorities[self.planet.id]["destroy_most_consuming_building"] -= \
                        self.priority_values["destroy_most_consuming_building"]

        # make shure only buildings are build that fit to the planet possible buildings
        if not self.auto_economy_handler.fit_building in self.planet.possible_resources:
            self.planet_task_priorities[self.planet.id]["build_fitting_building"] = 0

        for resource in ["energy", "food", "minerals", "water"]:
            if resource in self.planet.possible_resources:
                self.planet_task_priorities[self.planet.id][f"build_{resource}_buildings"] += self.priority_values[
                    f"build_{resource}_buildings"]
            else:
                self.planet_task_priorities[self.planet.id][f"build_{resource}_buildings"] = 0

        # limit all values to min(0):
        for key, value in self.planet_task_priorities[self.planet.id].items():
            if value < 0:
                value = 0
            if value > 100:
                value = 100

            self.planet_task_priorities[self.planet.id][key] = value

        # set highest_priority_key
        self.highest_priority_key = self.get_highest_priority_keys(self.planet_task_priorities[self.planet.id])

    def set_priority(self, priority, operand: any) -> None:
        if operand == "+":
            self.planet_task_priorities[self.planet.id][priority] += self.priority_values[priority]
        if operand == "-":
            self.planet_task_priorities[self.planet.id][priority] -= self.priority_values[priority]
        if operand == "*":
            self.planet_task_priorities[self.planet.id][priority] *= self.priority_values[priority]
        if operand == "/":
            self.planet_task_priorities[self.planet.id][priority] /= self.priority_values[priority]

        if type(operand) == int:
            self.planet_task_priorities[self.planet.id][priority] = operand

    def set_priorities(self, priorities: list[str], operand: any) -> None:
        for i in priorities:
            self.set_priority(i, operand)

    def set_planet_task_priorities(self, planet):
        self.planet = planet
        self.auto_economy_handler = self.player.auto_economy_handler

        production = {key: value for key, value in self.player.production.items() if key != "population"}
        resource_stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        negative_stock_resources = [key for key, value in resource_stock.items() if value < 0]
        negative_production_resources = [key for key, value in production.items() if value < 0]
        self.init_planet_priorities(self.planet)
        condition = self.conditions

        # handle negative_stock/negative_production
        if not condition.average_stock_is_min_1000:
            self.set_priority("add_deal", "+")
        else:
            self.set_priority("add_deal", "-")

        if condition.negative_stock:
            self.set_priority("add_deal", "+")
            for resource in negative_stock_resources:
                self.set_priorities(["destroy_most_consuming_building", "delete_buildings", "deal_with_the_bank"], "+")
        else:
            self.set_priorities(["destroy_most_consuming_building", "delete_buildings", "deal_with_the_bank"], 0)
            self.set_priority("add_deal", "-")

        if condition.negative_production:
            for resource in negative_production_resources:
                self.set_priorities(["destroy_most_consuming_building", "optimize_planets",
                                     "build_fitting_building"], "+")
        else:
            self.set_priority("destroy_most_consuming_building", 0)
            self.set_priorities(["optimize_planets", "build_fitting_building"], "-")

        if negative_stock_resources and negative_production_resources:
            self.set_priority("add_deal", "+")
            self.set_priorities(["destroy_most_consuming_building", "delete_buildings"], "+")
            if condition.technology_is_min_1:
                self.set_priority("deal_with_the_bank", "+")
            else:
                self.set_priority("deal_with_the_bank", 0)

        # handle zero production
        zero_productions = self.auto_economy_handler.get_zero_productions()
        if len(zero_productions) > 0:
            for building in self.planet.buildings:
                category = building_factory.get_category_by_building(building)
                if category in zero_productions:
                    self.set_priorities(["delete_buildings", "destroy_most_consuming_building",
                                         "deal_with_the_bank"], "+")
                    self.set_priority("optimize_planets", "-")

        # handle building logic
        if not condition.planet_has_any_buildings:
            self.set_priority("build_fitting_building", "+")
            self.set_priority("destroy_most_consuming_building", "-")
        else:
            if not condition.planet_has_buildings_max_reached:
                self.set_priority("build_fitting_building", "+")
            else:
                self.set_priorities([
                    "optimize_planets",
                    "delete_buildings",
                    "destroy_most_consuming_building",
                    "build_university"],
                        "+")

        # if has population and food, prior food and population
        if condition.planet_can_build_population:
            if condition.planet_has_population_max_reached:
                if condition.player_has_population_max_reached:
                    self.set_priorities([
                        "build_population_buildings",
                        "maximize_population_grow"],
                            "+")
            else:
                self.set_priorities([
                    "build_population_buildings",
                    "maximize_population_grow"],
                        "-")

            if planet.production["food"] < 1:
                self.set_priority("build_food_buildings", "+")
            elif planet.production["food"] < 3:
                self.set_priority("maximize_population_grow", "+")
            else:
                self.set_priorities([
                    "build_food_buildings",
                    "maximize_population_grow"],
                        "-")
        else:
            self.set_priorities([
                "build_population_buildings",
                "maximize_population_grow",
                "build_food_buildings"],
                    "-")

        # if it is possible to build tech buildings
        if condition.planet_can_build_technology:
            # check for population greater than 10000
            if condition.planet_population_is_min_1000:
                # only prior these building if player has a positive production
                if condition.average_stock_is_min_10000 and condition.player_average_production_is_min_0:
                    # space harbor
                    if self.player.get_all_buildings().count("space harbor") < SPACE_HARBOR_AMOUNT:
                        self.set_priority("build_space_harbour", "+")
                    else:
                        self.set_priority("build_space_harbour", 0)

                    # particle accelerator
                    if not "particle accelerator" in self.planet.buildings:
                        self.set_priority("build_particle_accelerator", "+")
                    # planetary_defence
                    elif not "planetary_defence" in self.planet.buildings:
                        self.set_priority("build_planetary_defence", "+")
            else:
                self.set_priority("build_space_harbour", 0)
        else:
            self.set_priorities([
                "build_space_harbour",
                "build_particle_accelerator",
                "build_planetary_defence"],
                    0)

        # build ships
        if condition.planet_has_space_harbor:
            self.set_priority("build_ship", "+")
        else:
            self.set_priority("build_ship", 0)

        # handle special cases
        if len(negative_stock_resources) != 0:
            for resource in negative_stock_resources:
                most_consuming_building = building_factory.get_most_consuming_building(self.auto_economy_handler.all_buildings, resource)
                if not most_consuming_building in self.planet.buildings:
                    self.set_priority("destroy_most_consuming_building",
                            "-")


        # make shure only buildings are build that fit to the planet possible buildings
        if not self.auto_economy_handler.fit_building in self.planet.possible_resources:
            self.planet_task_priorities[self.planet.id]["build_fitting_building"] = 0

        for resource in ["energy", "food", "minerals", "water"]:
            if resource in self.planet.possible_resources:
                if production[resource] < 3:
                    self.set_priority(f"build_{resource}_buildings", "+")
                else:
                    self.set_priority(f"build_{resource}_buildings", "-")
            else:
                self.set_priority(f"build_{resource}_buildings", 0)

        # limit all values to min(0):
        for key, value in self.planet_task_priorities[self.planet.id].items():
            if value < 0:
                value = 0
            if value > 100:
                value = 100

            self.planet_task_priorities[self.planet.id][key] = value

        # set highest_priority_key
        self.highest_priority_key = self.get_highest_priority_keys(self.planet_task_priorities[self.planet.id])

    def get_highest_priority_keys(self, dict_: dict) -> list:
        highest_keys = []
        if not dict_:
            return highest_keys

        highest_value = max(dict_.values())

        for key, value in dict_.items():
            if value == highest_value:
                highest_keys.append(key)
        return highest_keys





class AutoEconomyHandlerPriorityQueue__:# perplexity
    def __init__(self, player):
        self.planet = None
        self.player = player
        self.auto_economy_handler = None
        self.conditions = PriorityQueueConditions(self.player)
        self.planet_task_priorities = {}
        self.player_task_priorities = load_file("economy_queue_settings.json", "config")
        self.priority_values = load_file("economy_queue_settings.json", "config")

    def __repr__(self):
        return str(self.get_highest_priority_keys(self.planet_task_priorities[self.planet.id])) if self.planet else "None"

    def update_priorities(self, planets):
        """Sets the task priorities for the planets."""
        self.conditions.update_player_conditions()
        self.set_player_task_priorities()
        for planet in planets:
            self.conditions.update_planet_conditions(planet)
            self.set_planet_task_priorities(planet)

    def init_planet_priorities(self, planet):
        if planet.id not in self.planet_task_priorities:
            self.planet_task_priorities[planet.id] = {key: 0 for key in self.priority_values.keys()}

    def set_player_task_priorities(self):
        """Sets the sum of all planet_task_priorities."""
        len_ = len(self.planet_task_priorities.keys())
        for key in self.player_task_priorities.keys():
            self.player_task_priorities[key] = sum(self.planet_task_priorities[id_][key] for id_ in self.planet_task_priorities.keys()) // len_

    def set_planet_task_priorities(self, planet):
        self.planet = planet
        self.player = config.app.players[planet.owner]
        self.auto_economy_handler = self.player.auto_economy_handler
        production = {key: value for key, value in self.player.production.items() if key != "population"}
        resource_stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        negative_stock_resources = [key for key, value in resource_stock.items() if value < 0]
        negative_production_resources = [key for key, value in production.items() if value < 0]

        self.init_planet_priorities(planet)
        condition = self.conditions

        # Handle negative stock/negative production
        if condition.negative_stock:
            self.set_priorities(["destroy_most_consuming_building", "delete_buildings", "deal_with_the_bank"], "+")
        else:
            self.set_priorities(["destroy_most_consuming_building", "delete_buildings", "deal_with_the_bank"], 0)

        if condition.negative_production:
            self.set_priorities(["destroy_most_consuming_building", "optimize_planets", "build_fitting_building"], "+")
        else:
            self.set_priority("destroy_most_consuming_building", 0)
            self.set_priorities(["optimize_planets", "build_fitting_building"], "-")

        if negative_stock_resources and negative_production_resources:
            self.set_priorities(["destroy_most_consuming_building", "delete_buildings"], "+")
        if condition.technology_is_min_1:
            self.set_priority("deal_with_the_bank", "+")
        else:
            self.set_priority("deal_with_the_bank", 0)

        # Handle zero production
        zero_productions = self.auto_economy_handler.get_zero_productions()
        if zero_productions:
            for building in self.planet.buildings:
                category = building_factory.get_category_by_building(building)
                if category in zero_productions:
                    self.set_priorities(["delete_buildings", "destroy_most_consuming_building", "deal_with_the_bank"], "+")
                    self.set_priority("optimize_planets", "-")

        # Handle building logic
        if not condition.planet_has_any_buildings:
            self.set_priority("build_fitting_building", "+")
            self.set_priority("destroy_most_consuming_building", "-")
        else:
            if not condition.planet_has_buildings_max_reached:
                self.set_priority("build_fitting_building", "+")
            else:
                self.set_priorities(["optimize_planets", "delete_buildings", "destroy_most_consuming_building", "build_university"], "+")

    def set_priorities(self, keys, value):
        for key in keys:
            self.set_priority(key, value)

    def set_priority(self, key, value):
        if value == "+":
            self.planet_task_priorities[self.planet.id][key] += self.priority_values[key]
        elif value == "-":
            self.planet_task_priorities[self.planet.id][key] -= self.priority_values[key]
        else:
            self.planet_task_priorities[self.planet.id][key] = 0

    def get_highest_priority_keys(self, task_priorities):
        highest_priority = max(task_priorities.values())
        return [key for key, value in task_priorities.items() if value == highest_priority]
