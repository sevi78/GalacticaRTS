import copy
import random
import time
from pprint import pprint
from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups

BUILD_CHANGE_INTERVAL = 60
BUILDING_CUE_MAX = 3
RANDOM_FACTOR = 50
MIN_FOOD_PRODUCTION = 2
DELETE_BUILDING_THRESHOLD = 500


class AutoEconomyHandlerSetters:
    def __init__(self, player) -> None:
        """
        Initialize an instance of the AutoEconomyHandlerSetters class.

        Args:
            player (Player): The player object associated with this instance.

        Returns:
            None

        Initializes the following instance variables:
            - player (Player): The player object associated with this instance.
            - player_population_limit (None): The player's population limit.
            - build_change_interval_raw (int): The raw build change interval value.
            - build_change_interval (int): The build change interval value.
            - planets (list): A list of all planets associated with the player.
            - planet (None): The current planet.
            - preferred_building_key (None): The preferred building key.
            - preferred_delete_key (None): The preferred delete key.
            - min_keys_resources (None): The minimum keys for resources.
            - max_keys_resources (None): The maximum keys for resources.
            - max_keys_all (None): The maximum keys for all.
            - min_keys_all (None): The minimum keys for all.
            - current_production (None): The current production.
            - combined_production (None): The combined production.
            - all_buildings (None): All buildings associated with the player.
            - building_widget_list (None): The building widget list.
            - building_cue_max (int): The maximum value for the building cue.
            - population_buildings (list): A list of population buildings.
            - resource_buildings (list): A list of resource buildings.
            - planetary_defence_buildings (list): A list of planetary defence buildings.
            - fit_building (None): The building that fits the current production.
            - buildings_to_delete (None): The buildings to be deleted.
            - most_consuming_building (None): The most consuming building.
        """
        # vars
        self.player = player
        self.player_population_limit = None
        self.build_change_interval_raw = BUILD_CHANGE_INTERVAL
        self.build_change_interval = copy.copy(BUILD_CHANGE_INTERVAL)
        self.planets = []
        self.planet = None

        # keys
        self.preferred_building_key = None
        self.preferred_delete_key = None
        self.min_keys_resources = None
        self.max_keys_resources = None
        self.max_keys_all = None
        self.min_keys_all = None

        # productions
        self.current_production = None
        self.combined_production = None

        # buildings
        self.all_buildings = None
        # self.building_names = None
        self.building_widget_list = None
        self.building_cue_max = BUILDING_CUE_MAX
        self.population_buildings = []
        self.resource_buildings = []
        self.planetary_defence_buildings = []

        self.fit_building = None
        self.buildings_to_delete = None
        self.most_consuming_building = None

    def set_player(self, player_index: int) -> None:
        self.player = config.app.players[player_index]

    def set_player_population_limit(self) -> None:
        self.player_population_limit = self.player.population_limit

    def set_build_change_interval(self) -> None:
        self.build_change_interval = self.build_change_interval_raw / config.game_speed

    def set_planets(self):
        self.planets = [i for i in sprite_groups.planets if i.owner == self.player.owner]

    def set_planet(self, planet):
        self.planet = planet

    def set_preferred_building_key(self) -> None:
        if self.min_keys_resources:
            self.preferred_building_key = random.choice(self.min_keys_resources) if len(self.min_keys_resources) > 1 else \
                self.min_keys_resources[0]
        else:
            self.preferred_building_key = random.choice(building_factory.get_all_possible_categories())

    def set_preferred_delete_key(self) -> None:
        self.preferred_delete_key = random.choice(self.max_keys_all) if len(self.max_keys_all) > 1 else \
            self.max_keys_all[0]

    def set_min_keys_resources(self) -> None:
        self.min_keys_resources = [key for key, value in self.combined_production.items() if
                                   value == min(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                   and not key in ["technology", "population"]]

    def set_max_keys_resources(self) -> None:
        self.max_keys_resources = [key for key, value in self.combined_production.items() if
                                   value == max(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                   and not key in ["technology", "population"]]

    def set_min_keys_all(self) -> None:
        self.max_keys_all = [key for key, value in self.combined_production.items() if
                             value == min(self.combined_production.values())]

    def set_max_keys_all(self) -> None:
        self.max_keys_all = [key for key, value in self.combined_production.items() if
                             value == max(self.combined_production.values())]

    def set_current_production(self) -> None:
        self.current_production = self.player.production

    def set_combined_production(self) -> None:
        self.current_production = {}
        if self.building_widget_list:
            for i in self.building_widget_list:
                if i.receiver.owner == self.player.owner:
                    self.current_production[i] = building_factory.get_production_from_buildings_json(i)

            # add the current production to the player's production
            self.combined_production = building_factory.add_production(self.current_production, self.player.production)
        else:
            self.combined_production = self.player.production

    def set_all_buildings(self) -> None:
        """ sets self.buildings to a list of all buildings in all valid planets"""
        self.all_buildings = [i.buildings for i in sprite_groups.planets if i.owner == self.player.owner]

    def set_building_cue_max(self) -> None:
        self.building_cue_max = random.randint(1, BUILDING_CUE_MAX)

    def set_building_widget_list(self) -> None:
        building_widget_list_all = config.app.building_widget_list
        building_widget_list = [i for i in building_widget_list_all if i.receiver.owner == self.player.owner]
        self.building_widget_list = building_widget_list

    def set_resource_buildings(self) -> None:
        self.resource_buildings = [i for i in [item for sublist in self.all_buildings for item in sublist]
                                   if i in building_factory.get_all_resource_buildings()]

    def set_planetary_defence_buildings(self) -> None:
        self.planetary_defence_buildings = [i for i in
                                            [item for sublist in self.all_buildings for item in sublist]
                                            if i in building_factory.get_building_names("planetary_defence")]

    def set_population_buildings(self) -> None:
        self.population_buildings = [i for i in [item for sublist in self.all_buildings for item in sublist] if
                                     i in building_factory.get_building_names("population")]

    def set_fit_building(self) -> None:
        self.fit_building = building_factory.get_fitting_building(self.planet, self.preferred_building_key)

    def set_most_consuming_building(self) -> None:
        if self.min_keys_resources:
            self.most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, random.choice(self.min_keys_resources))

    def set_buildings_to_delete(self) -> None:
        self.buildings_to_delete = building_factory.get_building_names(self.preferred_delete_key)

    def set_economy_values(self) -> None:
        # buildings (all valid buildings from all planets)
        self.set_all_buildings()

        # planets
        self.set_planets()

        # buildings
        self.set_player_population_limit()
        self.set_population_buildings()
        self.set_planetary_defence_buildings()
        self.set_resource_buildings()

        # productiom
        self.set_current_production()
        self.set_combined_production()

        # min_keys_resources
        self.set_min_keys_resources()

        # max_keys_resources
        self.set_max_keys_resources()

        # min_keys_all
        self.set_min_keys_all()

        # max_keys_all
        self.set_max_keys_all()

        # most consumimg building
        self.set_most_consuming_building()

        # find the lowest value key (resource to build)
        self.set_preferred_building_key()


class AutoEconomyHandler(AutoEconomyHandlerSetters):
    def __init__(self, player):
        """
        Initializes an instance of the AutoEconomyHandler class.

        Parameters:
            player (Player): The player object associated with the AutoEconomyHandler instance.

        Returns:
            None
        """
        AutoEconomyHandlerSetters.__init__(self, player)

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
        # find the key that has the highest value key (resource to delete)
        self.set_preferred_delete_key()

        # get all buildings related to this key
        self.set_buildings_to_delete()

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

    def build_population_buildings(self):
        """
        Check if the planet has the necessary resources to produce food and build population buildings for growth.
        If the player's population is not greater than or equal to the population limit, return.
        If the planet has "food" and "population" in its possible resources, set the population limit of the planet and
        proceed to build population buildings.
        Build the first population building, a town, if it does not already exist.
        Upgrade population buildings based on population thresholds:
            - If population is >= 1000, upgrade to a city if not already present.
            - If population is between 1000 and 10000, upgrade to a city and then to a metropole.
            - If population is between 10000 and 100000, upgrade to a metropole.
            - If population is over 100000, build additional metropoles.
        """
        # check if planet has the productions: food and population that it need to:
        # produce food
        # build population buildings needed to grow
        if not self.player.population >= self.player.population_limit:
            return

        if "food" in self.planet.possible_resources and "population" in self.planet.possible_resources:
            # get population and population limit of the planet
            self.planet.set_population_limit()
            population = int(self.planet.population)

            # build the first population building
            # build a first town
            if not "town" in self.planet.buildings:
                building_factory.build("town", self.planet)

            # check if population is > 1000 to ensure it needs population building upgrades
            if population >= 1000:
                # check if population is over the population limit
                if population >= self.planet.population_limit:
                    # check if population is between 1000 and 10000
                    if population in range(1000, 10000):

                        # upgrade population building
                        if not "city" in self.planet.buildings:
                            if "town" in self.planet.buildings:
                                # delete town
                                building_factory.destroy_building("town", self.planet)
                            # build city
                            building_factory.build("city", self.planet)

                    # check if population is between 10000 and 100000
                    if population in range(10000, 100000):

                        # upgrade population building
                        if not "metropole" in self.planet.buildings:
                            if "city" in self.planet.buildings:
                                # delete city
                                building_factory.destroy_building("city", self.planet)
                            # build metropole
                            building_factory.build("metropole", self.planet)

                    # build more metropoles
                    if population in range(100000, 1000000):
                        building_factory.build("metropole", self.planet)

    def get_current_production(self):
        return self.current_production

    def get_valid_planet(self, player):
        """returns a random valid planet, means a planet with the player owns """
        planets = [i for i in sprite_groups.planets if i.owner == player.owner]
        planet = random.choice(planets)
        return planet

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

    def build_immediately(self) -> None:
        """
        Builds a building immediately if certain conditions are met.

        This function checks if there are any building widgets in the `building_widget_list` and if so, it randomly
        selects a building widget.
        If the selected building widget's `immediately_build_cost` is less than the player's technology and the owner
        of the building widget's receiver is the same as the player's owner,
        the building widget is built immediately and a message is printed indicating the player's technology.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        if len(self.building_widget_list) > 0:
            r = random.randint(0, len(self.building_widget_list) * 3)
            for i in self.building_widget_list:
                if self.building_widget_list.index(i) == r:
                    if i.immediately_build_cost < self.player.technology and i.receiver.owner == self.player.owner:
                        i.build_immediately()
                        print(f"building immediately !: {self.player.technology}")

    def build__(self):  # refactored
        if self.update_time_reached():
            self.update_cycles += 1
            self.reset_start_time()
            self.set_economy_values()

            for planet in self.planets:
                self.set_planet(planet)
                self.set_building_widget_list()

                if len(self.building_widget_list) >= self.building_cue_max:
                    return

                # Ensure food production after building population buildings
                # self.ensure_food_production(self.planet)

                # build population buildings if needed
                self.build_population_buildings()

                # get the building fitting to the population level of the planet
                # self.fit_building = self.get_fitting_building_based_on_population_limit(self.planet, self.prefered_building_key)

                self.set_fit_building()

                # choose a random building to build

                if self.fit_building:
                    self.building = self.fit_building
                else:
                    print("no fiiting building found, recommend to delete anything ! ")
                    # self.building = random.choice(self.building_names)
                # if len(self.fit_building) > 0:
                #     self.building = random.choice(list(self.fit_building))
                # else:
                #     self.building = random.choice(list(self.building_names))

                # finally build the building
                building_factory.build(self.building, self.planet)

                # delete buildings
                if self.combined_production:
                    stock = self.player.get_stock()
                    for key, value in stock.items():
                        if not key == "population":
                            if value < DELETE_BUILDING_THRESHOLD:
                                self.delete_buildings()

    def build(self):
        """
        Builds buildings on planets based on certain conditions.

        This function iterates over each planet in the `planets` list and performs the following actions:
        - Sets the current planet to the given planet.
        - Sets the building widget list for the current planet.
        - Sets the maximum building cue for the current planet.

        If any building in the building widget list is currently building, the function returns. Otherwise, the function
        proceeds to:
        - Build a building immediately if possible and a random factor is satisfied.
        - Build population buildings if needed.
        - Find the fitting building and build it.

        If a fitting building is found, the function sets the current building to the fitting building and calls the
        `build` function of the `building_factory` class, passing in the fitting building and the current planet.

        After iterating over all planets, the function checks if any resource stock is below the
        `DELETE_BUILDING_THRESHOLD`. If so, it deletes buildings and adds a fitting deal using the `deal_manager` class.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        for planet in self.planets:
            self.set_planet(planet)
            self.set_building_widget_list()
            self.set_building_cue_max()

            # check if any building is building cue
            if len(self.building_widget_list) >= self.building_cue_max:
                return
            else:
                # build immediately if possible and some random factor
                self.build_immediately()

            # build population buildings if needed
            self.build_population_buildings()

            # find fitting building and build it
            self.set_fit_building()
            if self.fit_building:
                self.building = self.fit_building
                building_factory.build(self.building, self.planet)

        # delete buildings if needed
        resource_stock = self.player.get_resource_stock()
        if resource_stock[self.get_lowest_value_key(resource_stock)] < DELETE_BUILDING_THRESHOLD:
            self.delete_buildings()

            # add deal
            config.app.deal_manager.add_fitting_deal(
                self.player,
                self.get_lowest_value_key(self.player.get_resource_stock()),
                self.get_highest_value_key(self.player.get_resource_stock())
                )

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
            self.build()
            config.app.deal_manager.get_fitting_deal(self.player)

        # print (config.app.deal_manager.get_deals_from_player(self.player))
