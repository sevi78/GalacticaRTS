import random

from source.auto_economy.auto_economy_builder import AutoEconomyBuilder
from source.auto_economy.auto_economy_setters import AutoEconomyHandlerSetters
from source.auto_economy.economy_calculator import economy_calculator
from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.file_handler import load_file
from source.handlers.time_handler import time_handler
from source.trading.market import market

RANDOM_FACTOR = 50
MIN_FOOD_PRODUCTION = 2


class AutoEconomyHandler(AutoEconomyHandlerSetters, AutoEconomyBuilder):  # original
    def __init__(self, player):
        """
        Initializes an instance of the AutoEconomyHandler class.

        Parameters:
            player (Player): The player object associated with the AutoEconomyHandler instance.

        Returns:
            None
        """
        # super().__init__(player)
        self.player = player
        AutoEconomyHandlerSetters.__init__(self, self.player)
        AutoEconomyBuilder.__init__(self)
        self.build_plan = None

        buildings_raw = load_file("buildings.json", "config")
        buildings = {}
        for category in buildings_raw.keys():
            for key, value in buildings_raw[category].items():
                buildings[value["name"]] = value

        self.building_dict = buildings
        self.build_start_time = time_handler.time
        self.random_factor = RANDOM_FACTOR
        self.update_cycles = 0
        # self.economy_calculator_ki = EconomyCalculatorKI()

    def reset_start_time(self) -> None:
        # pprint (f"reset start time: interval: {self.build_change_interval}")
        self.build_start_time = time_handler.time

    def update_time_reached(self) -> bool:
        if time_handler.time - self.build_start_time > self.build_change_interval:
            # pprint(f"update_time_reached")
            return True
        return False

    def delete_buildings(self) -> None:
        """
        Deletes a building from the player's planets based on the preferred delete key.

        This function first sets the preferred delete key by calling the `set_preferred_delete_key` method.
        Then, it retrieves all the buildings related to the preferred delete key by calling the
        `set_buildings_to_delete` method.
        Finally, it iterates through all the buildings and deletes the first building from the given category
        that is also in the buildings to delete list. The building is deleted from th first planet associated with the
        player that has the building.

        Returns:
            None
        """

        # choose the first building to delete from given category
        # if len(self.all_buildings) >= slots:
        all_buildings = [i for i in [item for sublist in self.all_buildings for item in sublist]]
        for i in all_buildings:
            if i in self.buildings_to_delete:
                # delete building
                for p in self.planets:
                    if i in p.economy_agent.buildings:
                        building_factory.destroy_building(i, p)
                        return

    def get_current_production(self):
        return self.current_production

    # def get_valid_planet(self, player):
    #     """returns a random valid planet, means a planet with the player owns """
    #     planets = [i for i in sprite_groups.planets if i.owner == player.owner]
    #     planet = random.choice(planets)
    #     return planet

    # !!! this might be wrong, maybe we need random choice of all lowest keys?
    def get_highest_value_key(self, stock: dict) -> str:
        """
        Returns the key with the highest value in the given stock dictionary.

        Parameters:
            stock (dict): A dictionary representing a stock, where the keys are the stock names and the values are their corresponding prices.

        Returns:
            str: The key with the highest value in the stock dictionary.
        """
        highest_value = max(stock.values())
        highest_key = None
        for key, value in stock.items():
            if value == highest_value:
                highest_key = key
        return highest_key

    # !!! this might be wrong, maybe we need random choice of all lowest keys?
    def get_lowest_value_key(self, stock: dict) -> str:
        """
        Returns the key with the lowest value in the given stock dictionary.

        Parameters:
            stock (dict): A dictionary representing a stock, where the keys are the stock names and the values are their corresponding prices.

        Returns:
            str: The key with the lowest value in the stock dictionary.
        """
        lowest_value = min(stock.values())
        lowest_key = None
        for key, value in stock.items():
            if value == lowest_value:
                lowest_key = key
        return lowest_key

    def get_peak_value_keys(self, stock: dict, peak: str = "max") -> list:
        """ returns a list of the lowest/highest values in stock """

        if peak == "max":
            highest = max(stock.values())
            highest_keys = []

            for key, value in stock.items():
                if value == highest:
                    highest_keys.append(key)

            return highest_keys

        if peak == "max":
            lowest = min(stock.values())
            lowest_keys = []

            for key, value in stock.items():
                if value == lowest:
                    lowest_keys.append(key)

            return lowest_keys

    def maximize_population_grow__(self):
        # check if planet is able to grow population
        if "food" in self.planet.possible_resources and "population" in self.planet.possible_resources:

            # check if planets food production is negative
            if self.planet.production["food"] < 2:
                # create a list of all buildings that can beleted on this planet,
                # because they do not support population growth:
                buildings_to_delete = []

                # check all buildings if they support population growth:
                for building in self.planet.economy_agent.buildings:
                    building_category = building_factory.get_category_by_building(building)
                    if building_category not in ["food", "population"]:
                        buildings_to_delete.append(building)

                # delete a random building
                if buildings_to_delete:
                    building_factory.destroy_building(random.choice(buildings_to_delete), self.planet)

                self.build_food_buildings()

    # def handle_infinite_loops__(self):
    #     zero_production = self.get_zero_productions()
    #     if zero_production:
    #         self.deal_with_the_bank()
    #         self.optimize_planets()
    #         self.destroy_most_consuming_building()

    # def handle_infinite_loops(self):
    #     zero_production = self.get_zero_productions()
    #     loop_counter = 0
    #     max_loops = 10  # Set a maximum number of iterations to prevent infinite loops
    #
    #     while zero_production and loop_counter < max_loops:
    #         self.deal_with_the_bank()
    #         self.optimize_planets()
    #         self.destroy_most_consuming_building()
    #         zero_production = self.get_zero_productions()
    #         loop_counter += 1
    #
    #     if loop_counter >= max_loops:
    #         print("Warning: Infinite loop detected and stopped.")

    def destroy_most_consuming_building__(self):
        # destroy most consuming building
        zero_production = self.get_zero_productions()
        for i in zero_production:
            most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, i)
            for p in self.planets:
                if most_consuming_building in p.economy_agent.buildings:
                    building_factory.destroy_building(most_consuming_building, p)

    def deal_with_the_bank(self):
        # deal with the bank
        deal = self.player.trade_assistant.generate_fitting_deal()
        player_index = self.player.owner
        stock = self.player.remove_population_key_from_stock(self.player.get_resource_stock())
        highest_value = max(stock.values())
        highest_key = None
        for key, value in stock.items():
            if value == highest_value:
                highest_key = key
        offer_value = self.player.stock[highest_key] * .2
        request_resource = list(deal.request.keys())[0]
        request_value = int(offer_value / 2)
        self.player.trade_assistant.trade_technology_to_the_bank(offer_value, request_resource, request_value, player_index)

    def add_deal(self):
        trade = self.player.trade_assistant.generate_fitting_deal()
        market.add_deal(trade, from_server=False)

    def get_zero_productions__(self):
        # handle the case when a resource is producing 0 and the stock of this resource is negative
        production = {key: value for key, value in self.player.production.items() if key != "population"}
        stock = self.player.get_resource_stock()
        negative_stock_resources = []
        # get all negative resources from stock
        for key, value in stock.items():
            if value < 0:
                negative_stock_resources.append(key)
        # if some negative values are there, check if any production is 0
        zero_production = []
        if negative_stock_resources:
            for key, value in production.items():
                if key in negative_stock_resources:
                    if value == 0:
                        zero_production.append(key)
        # if found the condition when a resource is producing 0 and the stock of this resource is negative, then
        # delete any building that consumes this resource
        return zero_production

    def optimize_planets(self, categories=building_factory.get_resource_categories_except_technology_and_population()):
        for planet in self.planets:
            for building in planet.economy_agent.buildings:
                next_level_building_category = building_factory.get_category_by_building(building)
                if next_level_building_category in categories:
                    next_level_building = building_factory.get_next_level_building(building)

                    if next_level_building:
                        if building_factory.get_build_population_minimum(building) < planet.population:
                            if not building in building_factory.get_building_names("population"):
                                building_factory.destroy_building(building, planet)
                                building_factory.build(next_level_building, planet)
                            else:
                                building_factory.destroy_building(building, planet)

                            text = f"optimize_planets: destroy: {building} and build: {next_level_building} on {planet}"
                            return

    def trade(self):
        if any(value < 700 for key, value in self.player.get_resource_stock().items() if not key == "population"):
            self.deal_with_the_bank()

        self.add_deal()
        market.get_fitting_deal(self.player)

    def replace_production_building_with_tech_building(self):
        # get all stuff
        space_harbor_amount = len([i for i in self.player.get_all_buildings() if i == "space harbor"])

        # if no building slots left
        if len(self.player.get_all_buildings()) == self.player.get_all_building_slots():
            highest_production_keys = self.get_peak_value_keys(self.player.production, 'max')

            # find planet to optimize
            if len(self.planets) > 0:
                planet = random.choice(self.planets)
            else:
                return

            # for planet in self.planets:
            highest_production_buildings = [i for i in planet.economy_agent.buildings if
                                            building_factory.get_category_by_building(i) in highest_production_keys]

            # if any buildings with highest production, then delete one and place a tech building
            if highest_production_buildings:
                chosen_highest_production_building = random.choice(highest_production_buildings)

                # keep space harbor
                if not chosen_highest_production_building == "space harbor":
                    building_factory.destroy_building(chosen_highest_production_building, planet)
                else:

                    building_factory.destroy_building(random.choice(planet.economy_agent.buildings), planet)

                # build space harbor if possible and no space harbor in any planet
                if "technology" in planet.economy_agent.possible_resources:
                    if space_harbor_amount == 0:
                        building_factory.build("space harbor", planet)
                        return
                    else:
                        self.build_ship()
                        return

            r = random.randint(0, 5)
            if r == 0:
                if len(planet.economy_agent.buildings) > 0:
                    building_factory.destroy_building(random.choice(planet.economy_agent.buildings), planet)

    def upgrade_buildings(self, planet):
        if len(planet.economy_agent.buildings) >= planet.economy_agent.buildings_max:
            for building in planet.economy_agent.buildings:
                if not building in building_factory.get_building_names("population"):
                    # find obsolete buildings
                    next_level_building = building_factory.get_next_level_building(building)
                    if next_level_building:
                        if building_factory.get_build_population_minimum(next_level_building) <= planet.economy_agent.population:
                            building_factory.destroy_building(building, planet)
                            building_factory.build(next_level_building, planet)
                            return

    def update(self):  # original, working 90 %

        """
        Updates the state of the object based on the current game state.

        This function checks if the game is paused and returns early if it is.
        It then sets the build change interval and checks if the update time has been reached.
        If it has, the function increments the update cycles, resets the start time,
        sets the economy values, and builds buildings.
        Finally, it gets a fitting deal from the deal manager for the player.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if config.game_paused:
            return
        self.set_build_change_interval()

        if not self.update_time_reached():
            return

        self.update_cycles += 1
        self.reset_start_time()
        self.set_economy_values()

        # get goals
        production_goal = {key.split("production_")[1]: value for key, value in economy_calculator.settings.items()
                           if key.startswith("production")}
        resource_goal = {key.split("resource_")[1]: value for key, value in economy_calculator.settings.items()
                         if key.startswith("resource")}
        calculation = economy_calculator.settings.get("calculation")

        # build on every planet
        average_lowest_production_score_keys = []
        average_lowest_production_score_sums = {}

        for planet in self.planets:
            if planet.type == "sun":
                continue

            self.set_building_widget_list()

            # this gets the lowest production score form original code
            lowest_production_score_keys = economy_calculator.get_best_fitting_building(
                    planet=planet,
                    buildings=self.player.get_all_buildings(),
                    all_buildings=len(self.player.get_all_buildings()),
                    all_building_slots=self.player.get_all_building_slots(),
                    population_limit=planet.economy_agent.population_limit,
                    population=planet.economy_agent.population,
                    production=planet.economy_agent.production,
                    production_goal=production_goal,
                    resources=self.player.get_stock(),
                    resource_goal=resource_goal)

            planet.economy_agent.lowest_production_score_keys = lowest_production_score_keys
            # print(f"lowest_production_score_keys_old:{lowest_production_score_keys} ")

            # check if not too much widgets are build at the same time
            if len(self.building_widget_list) >= self.building_cue_max:
                self.build_immediately()
            else:
                # check if any building slots are left
                if len(self.player.get_all_buildings()) < self.player.get_all_building_slots():
                    building_factory.build(random.choice(planet.economy_agent.lowest_production_score_keys), planet)
                elif len(self.player.get_all_buildings()) > self.player.get_all_building_slots() - 2:
                    # upgrade
                    pass
                    # self.upgrade_buildings(planet)

        # optimizing economy
        self.replace_production_building_with_tech_building()

        # trading
        self.trade()

        # ship
        if len(self.player.get_all_ships()) > 0:
            for ship in self.player.get_all_ships():
                ship.autopilot = True

            self.build_ship_weapons()

    # def update_new(self):  # new, uses score_calculator %
    #     """
    #     Updates the state of the object based on the current game state.
    #
    #     This function checks if the game is paused and returns early if it is.
    #     It then sets the build change interval and checks if the update time has been reached.
    #     If it has, the function increments the update cycles, resets the start time,
    #     sets the economy values, and builds buildings.
    #     Finally, it gets a fitting deal from the deal manager for the player.
    #
    #     Parameters:
    #         self (object): The instance of the class.
    #
    #     Returns:
    #         None
    #     """
    #     if config.game_paused:
    #         return
    #     self.set_build_change_interval()
    #
    #     if not self.update_time_reached():
    #         return
    #
    #     self.update_cycles += 1
    #     self.reset_start_time()
    #
    #     # get goals
    #     production_goal = {key.split("production_")[1]: value for key, value in economy_calculator.settings.items()
    #                        if key.startswith("production")}
    #     resource_goal = {key.split("resource_")[1]: value for key, value in economy_calculator.settings.items()
    #                      if key.startswith("resource")}
    #
    #     # build on every planet
    #     average_lowest_production_score_keys = []
    #     average_lowest_production_score_sums = {}
    #
    #     self.planets = [i for i in sprite_groups.planets if i.owner == self.player.owner]
    #     building_widget_list_all = building_widget_handler.building_widget_list
    #     building_widget_list = [i for i in building_widget_list_all if i.receiver.owner == self.player.owner]
    #     self.building_widget_list = building_widget_list
    #     for planet in self.planets:
    #         if planet.type == "sun":
    #             continue
    #
    #         # this is the new version
    #         average_lowest_production_score_keys += planet.economy_agent.lowest_production_score_keys
    #
    #         planet.economy_agent.score_calculator.implement_production_scores(self.player, production_goal)
    #         planet.economy_agent.score_calculator.implement_production_scores_sum()
    #         planet.economy_agent.score_calculator.implement_production_scores_percent()
    #         planet.economy_agent.score_calculator.implement_production_scores_sum_percent()
    #         planet.economy_agent.score_calculator.implement_production_penalties(self.player, planet.economy_agent)
    #         highest_production_score_keys_new = planet.economy_agent.score_calculator.get_highest_production_sum_percent()
    #         planet.economy_agent.lowest_production_score_keys = highest_production_score_keys_new
    #
    #         # check if not too much widgets are build at the same time
    #         if len(self.building_widget_list) >= self.building_cue_max:
    #             self.build_immediately()
    #         else:
    #             # check if any building slots are left
    #             if len(self.player.get_all_buildings()) < self.player.get_all_building_slots():
    #                 building_factory.build(random.choice(planet.economy_agent.lowest_production_score_keys), planet)
    #             elif len(self.player.get_all_buildings()) > self.player.get_all_building_slots() - 2:
    #                 # upgrade
    #                 pass
    #                 # self.upgrade_buildings(planet)
    #
    #     # optimizing economy
    #     self.replace_production_building_with_tech_building()
    #
    #     # trading
    #     self.trade()
    #
    #     # ship weapons
    #     if len(self.player.get_all_ships()) > 0:
    #         self.build_ship_weapons()
