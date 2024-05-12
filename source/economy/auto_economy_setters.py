import copy
import random

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups

BUILD_CHANGE_INTERVAL = 60
BUILDING_CUE_MAX = 3


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
        self.resource_categories = building_factory.get_resource_categories()
        self.resource_categories_except_technology_and_population = building_factory.get_resource_categories_except_technology_and_population()

        # keys
        self.preferred_building_key = None
        self.preferred_delete_key = None
        self.min_keys_resources = None
        self.max_keys_resources = None

        self.lowest_key = None
        self.highest__key = None
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

        # print(f"resource_categories: {self.resource_categories}")
        # print(f"player.get_resource_stock:{self.player.get_resource_stock()}")
        # print(f"self.resource_categories_except_technology_and_population:  {self.resource_categories_except_technology_and_population}")

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



    def set_min_keys_resources(self) -> None:
        resource_stock = {key: value for key, value in self.player.get_resource_stock().items() if
                          key in self.resource_categories_except_technology_and_population}

        self.min_keys_resources = [key for key in resource_stock if
                                   all(resource_stock[temp] >= resource_stock[key] for temp in resource_stock)]

        # print(f"set_min_keys_resources:\n    self.player: {self.player.name}, resource_stock: {resource_stock}, self.min_keys_resources: {self.min_keys_resources}")

    def set_max_keys_resources(self) -> None:
        resource_stock = {key: value for key, value in self.player.get_resource_stock().items() if
                          key in self.resource_categories_except_technology_and_population}
        self.max_keys_resources = [key for key in resource_stock if
                                   all(resource_stock[temp] <= resource_stock[key] for temp in resource_stock)]

    def set_min_keys_all(self) -> None:
        stock = self.player.get_stock()
        self.min_keys_all = [key for key in stock if all(stock[temp] >= stock[key] for temp in stock)]
        # print (f"set_min_keys_all of {self.player.name}: stock: {stock}, self.min_keys_all: {self.min_keys_all}")

    def set_max_keys_all(self) -> None:
        stock = self.player.get_stock()
        self.max_keys_all = [key for key in stock if all(stock[temp] <= stock[key] for temp in stock)]

    def set_lowest_value_key(self):
        self.lowest_key = self.get_lowest_value_key(self.player.get_stock())

    def set_highest_value_key(self):
        self.highest_key = self.get_highest_value_key(self.player.get_stock())

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
        if self.planet:
            self.fit_building = building_factory.get_fitting_building(self.planet.population, self.preferred_building_key)

    def set_most_consuming_building(self) -> None:
        if self.min_keys_resources:
            self.most_consuming_building = building_factory.get_most_consuming_building(self.all_buildings, random.choice(self.min_keys_resources))

    def set_preferred_delete_key(self) -> None:
        self.preferred_delete_key = random.choice(self.max_keys_all) if len(self.max_keys_all) > 1 else \
            self.max_keys_all[0]

    def set_buildings_to_delete_(self) -> None:
        if self.preferred_delete_key == "population":
            if not self.most_consuming_building in building_factory.get_building_names("food"):
                self.buildings_to_delete = [self.most_consuming_building]
                return
        self.buildings_to_delete = building_factory.get_building_names(self.preferred_delete_key)

    def set_buildings_to_delete(self) -> None:
        # if self.preferred_delete_key == "population":
        #     if not self.most_consuming_building in building_factory.get_building_names("food"):
        #         self.buildings_to_delete = [self.most_consuming_building]
        #         return
        self.buildings_to_delete = building_factory.get_building_names(self.preferred_delete_key)
        self.buildings_to_delete.append(self.most_consuming_building)

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
        self.set_lowest_value_key()

        # max_keys_all
        self.set_max_keys_all()
        self.set_highest_value_key()

        # most consumimg building
        self.set_most_consuming_building()

        # find the key that has the highest value key (resource to delete)
        self.set_preferred_delete_key()

        # get all buildings related to this key
        self.set_buildings_to_delete()

        # find the lowest value key (resource to build)
        self.set_preferred_building_key()
        self.set_fit_building()
