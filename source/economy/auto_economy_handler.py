import random
import time

from source.configuration.game_config import config
from source.economy.auto_economy_setters import AutoEconomyHandlerSetters
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups

RANDOM_FACTOR = 50
MIN_FOOD_PRODUCTION = 2
DELETE_BUILDING_THRESHOLD = 500
SHIP_MAXIMUM = 15
SPACESHIP_MAXIMUM = 5
SPACEHUNTER_MAXXIMUM = 5
CARGO_LOADER_MAXIMUM = 3
SPACESTATION_MAXIMUM = 2


class AutoEconomyHandler(AutoEconomyHandlerSetters):
    def __init__(self, player):
        """
        Initializes an instance of the AutoEconomyHandler class.

        Parameters:
            player (Player): The player object associated with the AutoEconomyHandler instance.

        Returns:
            None
        """
        super().__init__(player)

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
                building_factory.build("farm", self.planet)
                building_factory.build("farm", self.planet)

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
                            building_factory.build("city", self.planet)

                            # upgrade farm
                            if "farm" in self.planet.buildings:
                                building_factory.destroy_building("farm", self.planet)
                            building_factory.build("ranch", self.planet)

                    # check if population is between 10000 and 100000
                    if population in range(10000, 100000):
                        # upgrade population building
                        if not "metropole" in self.planet.buildings:
                            if "city" in self.planet.buildings:
                                # delete city
                                building_factory.destroy_building("city", self.planet)
                            building_factory.build("metropole", self.planet)

                            if "ranch" in self.planet.buildings:
                                building_factory.destroy_building("ranch", self.planet)
                            building_factory.build("metropole", self.planet)

                    # build more metropoles
                    if population in range(100000, 1000000):
                        building_factory.build("metropole", self.planet)
                        building_factory.destroy_building("agriculture complex", self.planet)

    def get_current_production(self):
        return self.current_production

    def get_valid_planet(self, player):
        """returns a random valid planet, means a planet with the player owns """
        planets = [i for i in sprite_groups.planets if i.owner == player.owner]
        planet = random.choice(planets)
        return planet

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

    def build_food_buildings(self, planet):
        """
        builds population buildings to planet
        checks for fitting building based on population of the planet
        """
        building = building_factory.get_fitting_building(planet.population, "food")
        building_factory.build(building, planet)

    def build_space_harbour(self):
        """ builds a space harbour if not found on any planet"""
        production = {key: value for key, value in self.player.production.items() if key != "population"}
        if self.player.population > 1000:
            if not any(value < 0 for value in production.values()):
                if not "space harbor" in self.all_buildings:
                    building_factory.build("space harbor", self.planet)

    def build_ship(self):
        """
        builds ships if possible and send rescue drones
        """
        space_harbour_planet = [i for i in self.planets if "space harbor" in i.buildings]

        if space_harbour_planet:
            ships = self.player.get_all_ships()
            if not len(ships) > SHIP_MAXIMUM:
                spaceships = len([i for i in ships if i.name == "spaceship"])
                spacehunters = len([i for i in ships if i.name == "spacehunter"])
                cargoloaders = len([i for i in ships if i.name == "cargoloader"])
                spacestations = len([i for i in ships if i.name == "spacestation"])
                rescue_drones = len([i for i in ships if i.name == "rescue drone"])

                # build rescue drone
                lost_ships = [ship for ship in ships if ship.state_engine.state == "move_stop"]
                if lost_ships:
                    if rescue_drones > 0:
                        [i for i in ships if i.name == "rescue drone"][0].set_target(target=lost_ships[0])
                    else:
                        building_factory.build("rescue drone", space_harbour_planet[0])

                # build spaceships
                if spaceships < SPACESHIP_MAXIMUM:
                    building_factory.build("spaceship", space_harbour_planet[0])
                elif spacehunters < SPACEHUNTER_MAXXIMUM:
                    building_factory.build("spacehunter", space_harbour_planet[0])
                elif cargoloaders < CARGO_LOADER_MAXIMUM:
                    building_factory.build("cargoloader", space_harbour_planet[0])
                elif spacestations < SPACESTATION_MAXIMUM:
                    building_factory.build("spacestation", space_harbour_planet[0])

    def build_ship_weapons(self):
        ships = self.player.get_all_ships()
        weaponised_ships = [i for i in ships if i.name in ["spaceship", "spacehunter", "cargoloader"]]
        if weaponised_ships:
            print(f"build_ship_weapons:{weaponised_ships[0].weapon_handler.weapons}")

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

                self.build_food_buildings(self.planet)

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
            r = random.randint(0, int(len(self.building_widget_list) / 3))
            for i in self.building_widget_list:
                if self.building_widget_list.index(i) == r:
                    if i.immediately_build_cost < self.player.technology and i.receiver.owner == self.player.owner:
                        i.build_immediately()
                        # print(f"building immediately !: {self.player.technology}")

    def handle_infinte_loops(self):
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
        if zero_production:
            for i in zero_production:
                most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, i)
                for p in self.planets:
                    if most_consuming_building in p.buildings:
                        building_factory.destroy_building(most_consuming_building, p)
                        print(f"handle_infinte_loops: \nplayer: {self.player.name}\nzero_production:{zero_production}\ndestroyed building:{most_consuming_building} on {p}")

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

            # build space harbour
            self.build_space_harbour()
            self.build_ship()
            self.build_ship_weapons()

            # check if any building is building cue
            if len(self.building_widget_list) >= self.building_cue_max:
                return
            else:
                # build immediately if possible and some random factor
                self.build_immediately()

            self.maximize_population_grow()
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

        # add deals
        config.app.deal_manager.add_fitting_deal(self.player.trade_assistant.generate_fitting_deal())

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

            self.handle_infinte_loops()

        # print (config.app.deal_manager.get_deals_from_player(self.player))

        pass
