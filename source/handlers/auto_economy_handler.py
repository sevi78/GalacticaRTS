import copy
import random
import time
from pprint import pprint

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups

BUILD_CHANGE_INTERVAL = 120
BUILDING_CUE_MAX = 3
RANDOM_FACTOR = 50
MIN_FOOD_PRODUCTION = 5


class AutoEconomyHandler:
    def __init__(self, player):
        self.player = player
        self.planet = None
        self.planets = []
        self.buildings = []
        self.population_buildings = []
        self.resource_buildings = []
        self.planetary_defence_buildings = []
        self.building_cue_max = BUILDING_CUE_MAX
        self.fit_building = None
        self.most_consuming_building = None
        self.prefered_building_key = None
        self.prefered_delete_key = None

        self.max_keys_all = None
        self.min_keys_all = None
        self.max_keys_resources = None
        self.min_keys_resources = None

        self.buildings_to_delete = None
        self.all_buildings = None
        self.building_names = None
        self.building_widget_list = None
        self.current_production = None
        self.building = None

        self.combined_production = None

        self.player = player  # the Player() instance
        self.build_start_time = time.time()
        self.build_change_interval_raw = BUILD_CHANGE_INTERVAL
        self.build_change_interval = copy.copy(BUILD_CHANGE_INTERVAL)
        self.random_factor = RANDOM_FACTOR
        self.update_cycles = 0

    def set_player(self, player_index: int):
        self.player = config.app.players[player_index]

    def ensure_food_production(self, planet):
        """
        Ensure the planet has enough food production to support growth.
        """
        food_production = planet.production.get('food', 0)
        if food_production < MIN_FOOD_PRODUCTION:
            # Check if a food building can be built
            food_building = self.get_fitting_building_based_on_population_limit(planet, building_factory.get_building_names("food"))
            if food_building and not food_building in planet.buildings:
                building_factory.build(food_building, planet)
                print(f"Built {food_building} on planet {planet} to increase food production.")

    def avoid_redundant_cycles(self, planet, player):
        """
        Avoid redundant build and delete cycles by checking the history of actions.
        """
        # Implement a history tracking system for built and deleted buildings
        if not hasattr(self, 'build_history'):
            self.build_history = {}

        current_buildings = set(planet.buildings)
        history = self.build_history.get(planet, [])

        # Check if the current state matches any previous state in the history
        for past_buildings in history:
            if current_buildings == past_buildings:
                print("Detected a cycle, will not perform redundant actions.")
                return True
        # Update history
        history.append(current_buildings)
        if len(history) > 10:  # Keep only the last 10 states
            history.pop(0)
        self.build_history[planet] = history
        return False

    def set_buildings(self):
        """ sets self.buildings to a list of all buildings in all valid planets"""
        self.all_buildings = [i.buildings for i in sprite_groups.planets if i.owner == self.player.owner]

    def reset_start_time(self):
        # pprint (f"reset start time: interval: {self.build_change_interval}")
        self.build_start_time = time.time()

    def update_time_reached(self):
        if time.time() - self.build_start_time > self.build_change_interval:
            # pprint(f"update_time_reached")
            return True
        return False

    def get_fitting_building_based_on_population_limit(self, planet, prefered_building_key):
        fit_building = building_factory.get_a_list_of_building_names_from_category_with_build_population_minimum_bigger_than(planet.population_limit, prefered_building_key)
        # pprint(f"get_fitting_building_based_on_population_limit: planet: {planet.name}, prefered_building_key: {prefered_building_key}, fit_building: {fit_building}")
        return fit_building

    def get_building_names_by_key(self, prefered_building_key):
        building_names = building_factory.get_building_names(prefered_building_key)
        # pprint (f"get_building_names_by_key: prefered_building_key: {prefered_building_key}, building_names: {building_names}")
        return building_names

    def delete_buildings(self, combined_production, planet, player):
        # delete buildings
        all_buildings = player.get_all_buildings()
        slots = player.get_all_building_slots()

        # find the key that has the highest value key (resource to delete)
        max_keys = [key for key, value in combined_production.items() if
                    value == max(combined_production.values())]
        self.prefered_delete_key = random.choice(max_keys) if len(max_keys) > 1 else max_keys[0]

        # get all buildings related to this key
        self.buildings_to_delete = self.get_building_names_by_key(self.prefered_delete_key)

        # pprint (f"delete_buildings: prefered_delete_key: {self.prefered_delete_key}, buildings_to_delete: {self.buildings_to_delete}")
        # choose the first building to delete from given category
        if len(all_buildings) >= slots:
            for i in player.get_all_buildings():
                if i in self.buildings_to_delete:
                    # delete building
                    # pprint(f"delete_buildings: Deleting building {i} from planet {planet}")
                    for p in self.planets:
                        if i in p.buildings:
                            building_factory.destroy_building(i, p)
                            return

    def get_prefered_building_key(self, combined_production):

        if self.min_keys_resources:
            prefered_building_key = random.choice(self.min_keys_resources) if len(self.min_keys_resources) > 1 else \
                self.min_keys_resources[0]
            # pprint (f"get_prefered_building_key: prefered_building_key: {prefered_building_key}")
        else:
            prefered_building_key = random.choice(building_factory.get_all_possible_categories())
        return prefered_building_key

    def build_population_buildings(self, planet):
        # check if planet has the productions: food and population that it need to:
        # produce food
        # build population buildings needed to grow

        if "food" in planet.possible_resources and "population" in planet.possible_resources:
            # get population and population limit of the planet
            planet.set_population_limit()
            population = int(planet.population)

            # build the first population building

            # build a first town
            if not "town" in planet.buildings:
                building_factory.build("town", planet)

            # check if population is > 1000 to ensure it needs population building upgrades
            if population > 1000:
                # check if population is over the population limit
                if population > planet.population_limit:
                    # check if population is between 1000 and 10000
                    if population in range(1000, 10000):

                        # upgrade population building
                        if not "city" in planet.buildings:
                            if "town" in planet.buildings:
                                # delete town
                                building_factory.destroy_building("town", planet)
                            # build city
                            building_factory.build("city", planet)

                    # check if population is between 10000 and 100000
                    if population in range(10000, 100000):

                        # upgrade population building
                        if not "metropole" in planet.buildings:
                            if "city" in planet.buildings:
                                # delete city
                                building_factory.destroy_building("city", planet)
                            # build metropole
                            building_factory.build("metropole", planet)

                    # build more metropoles
                    if population in range(100000, 1000000):
                        building_factory.build("metropole", planet)

    def get_current_production(self):
        return self.current_production

    def add_building_widgets_production(self, building_widget_list, player):
        self.current_production = {}
        if building_widget_list:
            for i in building_widget_list:
                if i.receiver.owner == player.owner:
                    self.current_production[i] = building_factory.get_production_from_buildings_json(i)

            # add the current production to the player's production
            combined_production = building_factory.add_production(self.current_production, player.production)
            # pprint(f"add_building_widgets_production: combined_production: {combined_production},current_production: {current_production},player.production: {player.production}")
        else:
            combined_production = player.production
            # pprint (f"add_building_widgets_production: player.production: {player.production}")
        return combined_production

    def get_valid_planet(self, player):
        planets = [i for i in sprite_groups.planets if i.owner == player.owner]
        planet = random.choice(planets)
        # pprint (f"get_valid_planet: planet: {planet}, valid planets: {planets}")
        return planet

    def get_building_cue(self, player):
        building_widget_list_all = config.app.building_widget_list
        building_widget_list = [i for i in building_widget_list_all if i.receiver.owner == player.owner]
        # pprint (f"get_building_cue: building_widget_list: {building_widget_list}, building_widget_list_all: {building_widget_list_all}")
        return building_widget_list

    def _build(self):
        if self.update_time_reached():
            self.update_cycles += 1
            self.reset_start_time()

            # buildings (all valid buildings from all planets)
            self.set_buildings()

            # planets
            self.planets = [i for i in sprite_groups.planets if i.owner == self.player.owner]

            for planet in self.planets:
                self.planet = planet
                # Ensure food production after building population buildings
                self.ensure_food_production(self.planet)

                self.population_buildings = [i for i in [item for sublist in self.buildings for item in sublist] if
                                             i in building_factory.get_building_names("population")]

                self.planetary_defence_buildings = [i for i in [item for sublist in self.buildings for item in sublist]
                                                    if
                                                    i in building_factory.get_building_names("planetary_defence")]

                self.resource_buildings = [i for i in [item for sublist in self.buildings for item in sublist] if
                                           i in building_factory.get_resource_categories()]

                # Check for and avoid redundant build/delete cycles
                # if self.avoid_redundant_cycles(self.planet, self.player):
                #     if len(self.planet.buildings) > 0:
                #         self.planet.buildings.remove(random.choice(self.planet.buildings))

                # build population buildings if needed
                self.build_population_buildings(self.planet)

                # get building cue
                self.building_widget_list = self.get_building_cue(self.player)

                # get all building widget to find out what is currently producing
                self.combined_production = self.add_building_widgets_production(self.building_widget_list, self.player)

                # min_keys_resources
                self.min_keys_resources = [key for key, value in self.combined_production.items() if
                                           value == min(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                           and not key in ["technology", "population"]]

                # max_keys_resources
                self.max_keys_resources = [key for key, value in self.combined_production.items() if
                                           value == max(self.combined_production.values()) and key in building_factory.get_resource_categories()
                                           and not key in ["technology", "population"]]

                # min_keys_all
                self.min_keys_all = [key for key, value in self.combined_production.items() if
                                     value == min(self.combined_production.values())]

                # max_keys_all
                self.max_keys_all = [key for key, value in self.combined_production.items() if
                                     value == max(self.combined_production.values())]

                # most consumimg building
                if self.min_keys_resources:
                    self.most_consuming_building = building_factory.get_most_consuming_building(self.buildings, random.choice(self.min_keys_resources))

                # find the lowest value key (resource to build)
                self.prefered_building_key = self.get_prefered_building_key(self.combined_production)

                # get all buildings related to this key
                self.building_names = self.get_building_names_by_key(self.prefered_building_key)

                # get the building fitting to the population level of the planet
                self.fit_building = self.get_fitting_building_based_on_population_limit(self.planet, self.prefered_building_key)

                # choose a random building to build
                if len(self.fit_building) > 0:
                    self.building = random.choice(list(self.fit_building))
                else:
                    self.building = random.choice(list(self.building_names))

                # stopp if too many in cue:
                if len(self.building_widget_list) >= self.building_cue_max:
                    return

                # finally build the building
                building_factory.build(self.building, self.planet)

                # delete buildings
                self.delete_buildings(self.combined_production, self.planet, self.player)

                # build_stopp if not enough resources
                if any([self.player.stock[resource] < 250 for resource in self.player.stock]):
                    if self.most_consuming_building:
                        if self.most_consuming_building in planet.buildings:
                            building_factory.destroy_building(self.most_consuming_building, planet)
                            return
                        elif self.most_consuming_building in [i.buildings for i in self.planets]:
                            for planet_ in self.planets:
                                if self.most_consuming_building in planet_.buildings:
                                    building_factory.destroy_building(self.most_consuming_building, planet_)
                                    return
                    else:
                        print("possible endloop: not enough resources, and no building to delete found!")
                        # if len(self.planet.buildings) > 0:
                        #     if any([self.player.production[resource] < 0 for resource in self.player.production]):
                        #         self.planet.buildings.remove(random.choice(
                        #             [i for i in building_factory.get_all_building_names() if
                        #              not building_factory.get_category_by_building(i) in ["population"]]))

                # randomness
                r = random.randint(0, RANDOM_FACTOR)
                if r == 0:
                    for i in self.planets:
                        if len(i.buildings) > 0:
                            i.buildings.remove(random.choice(i.buildings))
                            building_factory.build(random.choice([i for i in building_factory.get_all_building_names()
                                                                  if
                                                                  not building_factory.get_category_by_building(i) in [
                                                                      "population"]]), self.planet)
                            return

    def update(self):
        if config.game_paused:
            return

        self.build_change_interval = self.build_change_interval_raw / config.game_speed
        self._build()
