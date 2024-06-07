import random
import time

from source.auto_economy.auto_economy_builder import AutoEconomyBuilder
from source.auto_economy.auto_economy_setters import AutoEconomyHandlerSetters
from source.auto_economy.economy_calculator import economy_calculator
from source.configuration.game_config import config
from source.factories.building_factory import building_factory

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
        self.building = None
        self.build_start_time = time.time()
        self.random_factor = RANDOM_FACTOR
        self.update_cycles = 0

    def reset_start_time(self) -> None:
        # pprint (f"reset start time: interval: {self.build_change_interval}")
        self.build_start_time = time.time()

    def update_time_reached(self) -> bool:
        if time.time() - self.build_start_time > self.build_change_interval:
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
                    if i in p.buildings:
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
        Returns the key with the lowest value in the given stock dictionary.

        Parameters:
            stock (dict): A dictionary representing a stock, where the keys are the stock names and the values are their corresponding prices.

        Returns:
            str: The key with the lowest value in the stock dictionary.
        """
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

    def maximize_population_grow(self):
        # check if planet is able to grow population
        if "food" in self.planet.possible_resources and "population" in self.planet.possible_resources:

            # check if planets food production is negative
            if self.planet.production["food"] < 2:
                # create a list of all buildings that can beleted on this planet,
                # because they do not support population growth:
                buildings_to_delete = []

                # check all buildings if they support population growth:
                for building in self.planet.buildings:
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

    def destroy_most_consuming_building(self):
        # destroy most consuming building
        zero_production = self.get_zero_productions()
        for i in zero_production:
            most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, i)
            for p in self.planets:
                if most_consuming_building in p.buildings:
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
        offer_value = getattr(self.player, highest_key) * .2
        request_resource = list(deal["request"].keys())[0]
        request_value = int(offer_value / 2)
        self.player.trade_assistant.trade_technology_to_the_bank(offer_value, request_resource, request_value, player_index)

    def add_deal(self):
        config.app.deal_manager.add_fitting_deal(self.player.trade_assistant.generate_fitting_deal())

    def get_zero_productions(self):
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
            population = planet.population
            for building in planet.buildings:
                next_level_building_category = building_factory.get_category_by_building(building)
                if next_level_building_category in categories:
                    next_level_building = building_factory.get_next_level_building(building)

                    if next_level_building:
                        if building_factory.get_build_population_minimum(building) < population:
                            building_factory.destroy_building(building, planet)
                            building_factory.build(next_level_building, planet)
                            text = f"optimize_planets: destroy: {building} and build: {next_level_building} on {planet}"

    # def get_best_population_planets(self):
    #     max_ = 0
    #
    #     for i in self.planets:
    #         if i.build_priorities["population"] > max_:
    #             max_ = i.build_priorities["population"]
    #
    #     best_population_planets = [i for i in self.planets if i.build_priorities["population"] == max_]
    #     return best_population_planets

    def update(self):
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
        if self.update_time_reached():
            self.update_cycles += 1
            self.reset_start_time()
            self.set_economy_values()

            # get goals
            production_goal = {key.split("production_")[1]: value for key, value in economy_calculator.settings.items()
                               if key.startswith("production")}
            resource_goal = {key.split("resource_")[1]: value for key, value in economy_calculator.settings.items()
                             if key.startswith("resource")}

            # build on every planet
            all_buildings = self.player.get_all_buildings()
            all_building_slots = self.player.get_all_building_slots()

            for planet in self.planets:
                self.set_building_widget_list()

                # check if not too much widgets are build at the same time
                if len(self.building_widget_list) >= self.building_cue_max:
                    config.app.deal_manager.get_fitting_deal(self.player)
                    self.add_deal()
                    self.build_immediately()
                else:
                    # get best fitting building
                    lowest_production_score_keys = economy_calculator.get_best_fitting_building(
                            population=planet.population,
                            production=planet.production,
                            production_goal=production_goal,
                            resources=self.player.get_stock(),
                            resource_goal=resource_goal)

                    # check if any building slots are left
                    if len(all_buildings) < all_building_slots:
                        building_factory.build(random.choice(lowest_production_score_keys), planet)

            # otherwise optimize planets
            if len(all_buildings) >= all_building_slots:
                self.optimize_planets()