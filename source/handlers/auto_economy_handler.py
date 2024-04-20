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

    def set_preferred_building_key(self):
        if self.min_keys_resources:
            self.preferred_building_key = random.choice(self.min_keys_resources) if len(self.min_keys_resources) > 1 else \
                self.min_keys_resources[0]
        else:
            self.preferred_building_key = random.choice(building_factory.get_all_possible_categories())

    def set_preferred_delete_key(self):
        self.preferred_delete_key = random.choice(self.max_keys_all) if len(self.max_keys_all) > 1 else \
            self.max_keys_all[0]

    def set_min_keys_resources(self):
        self.min_keys_resources = [key for key, value in self.combined_production.items() if
                                   value == min(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                   and not key in ["technology", "population"]]

    def set_max_keys_resources(self):
        self.max_keys_resources = [key for key, value in self.combined_production.items() if
                                   value == max(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                   and not key in ["technology", "population"]]

    def set_min_keys_all(self):
        self.max_keys_all = [key for key, value in self.combined_production.items() if
                             value == min(self.combined_production.values())]

    def set_max_keys_all(self):
        self.max_keys_all = [key for key, value in self.combined_production.items() if
                             value == max(self.combined_production.values())]

    def set_current_production(self):
        self.current_production = self.player.production

    def set_combined_production(self):
        self.current_production = {}
        if self.building_widget_list:
            for i in self.building_widget_list:
                if i.receiver.owner == self.player.owner:
                    self.current_production[i] = building_factory.get_production_from_buildings_json(i)

            # add the current production to the player's production
            self.combined_production = building_factory.add_production(self.current_production, self.player.production)
        else:
            self.combined_production = self.player.production

    def set_all_buildings(self):
        """ sets self.buildings to a list of all buildings in all valid planets"""
        self.all_buildings = [i.buildings for i in sprite_groups.planets if i.owner == self.player.owner]

    def set_building_cue_max(self):
        self.building_cue_max = random.randint(1, BUILDING_CUE_MAX)

    def set_building_widget_list(self):
        building_widget_list_all = config.app.building_widget_list
        building_widget_list = [i for i in building_widget_list_all if i.receiver.owner == self.player.owner]
        self.building_widget_list = building_widget_list

    def set_resource_buildings(self):
        self.resource_buildings = [i for i in [item for sublist in self.all_buildings for item in sublist]
                                   if i in building_factory.get_all_resource_buildings()]

    def set_planetary_defence_buildings(self):
        self.planetary_defence_buildings = [i for i in
                                            [item for sublist in self.all_buildings for item in sublist]
                                            if i in building_factory.get_building_names("planetary_defence")]

    def set_population_buildings(self):
        self.population_buildings = [i for i in [item for sublist in self.all_buildings for item in sublist] if
                                     i in building_factory.get_building_names("population")]

    def set_fit_building(self):
        self.fit_building = building_factory.get_fitting_building(self.planet, self.preferred_building_key)

    def set_most_consuming_building(self):
        if self.min_keys_resources:
            self.most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, random.choice(self.min_keys_resources))

    def set_buildings_to_delete(self):
        self.buildings_to_delete = building_factory.get_building_names(self.preferred_delete_key)

    def set_economy_values(self):
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
        AutoEconomyHandlerSetters.__init__(self, player)

        self.building = None
        self.build_start_time = time.time()
        self.random_factor = RANDOM_FACTOR
        self.update_cycles = 0

    def reset_start_time(self):
        # pprint (f"reset start time: interval: {self.build_change_interval}")
        self.build_start_time = time.time()

    def update_time_reached(self):
        if time.time() - self.build_start_time > self.build_change_interval:
            # pprint(f"update_time_reached")
            return True
        return False

    def delete_buildings(self):
        # delete buildings
        # slots = self.player.get_all_building_slots()

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
        highest_value = max(stock.values())
        highest_key = None
        for key, value in stock.items():
            if value == highest_value:
                highest_key = key
        return highest_key

    def get_lowest_value_key(self, stock: dict) -> str:
        lowest_value = min(stock.values())
        lowest_key = None
        for key, value in stock.items():
            if value == lowest_value:
                lowest_key = key
        return lowest_key

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
        for planet in self.planets:
            self.set_planet(planet)
            self.set_building_widget_list()
            self.set_building_cue_max()

            if len(self.building_widget_list) >= self.building_cue_max:
                return

            # if any(building_factory.get_building_names("population") in self.planet.buildings) and self.planet.population >= self.planet.population_limit:
            #     continue

            # if "food" not in self.planet.possible_resources:
            #     continue
            #
            # if "population" not in self.planet.possible_resources or self.planet.population >= self.planet.population_limit:
            #     continue

            self.build_population_buildings()

            self.set_fit_building()
            if self.fit_building:
                self.building = self.fit_building
                building_factory.build(self.building, self.planet)

        resource_stock = self.player.get_resource_stock()

        if resource_stock[self.get_lowest_value_key(resource_stock)] < DELETE_BUILDING_THRESHOLD:
            self.delete_buildings()
            config.app.deal_manager.add_fitting_deal(
                self.player,
                self.get_lowest_value_key(self.player.get_resource_stock()),
                self.get_highest_value_key(self.player.get_resource_stock())
                )

    def update(self):
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
