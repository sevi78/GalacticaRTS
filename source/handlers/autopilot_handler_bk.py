import copy
import math
import random
import time

import pygame.sprite

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups, PanZoomLayeredUpdates

TASK_CHANGE_INTERVAL = 45


class AutopilotHandler:
    def __init__(self, parent):
        self.reachable_planets = []
        self.parent = parent
        self.last_task_time = time.time()
        self.task_change_interval_raw = TASK_CHANGE_INTERVAL
        self.task_change_interval = copy.copy(TASK_CHANGE_INTERVAL)
        self.tasks = ["set_random_target"]
        self.task = ""

    def set_random_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = random.choice(targets)
        self.parent.orbit_object = None

    def get_nearest_target(self, targets: PanZoomLayeredUpdates):
        nearest_target = None
        nearest_distance = float('inf')  # Initialize with infinity

        for target in targets:
            distance = math.dist(self.parent.rect.center, target.rect.center)  # Replace with actual positions
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_target = target

        return nearest_target

    def set_nearest_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = self.get_nearest_target(targets)
        self.parent.orbit_object = None

    def create_economy(self, strategy):
        player = config.app.player

        for i in config.app.explored_planets:
            if strategy == "random":
                building_factory.build(random.choice(building_factory.get_all_building_names()), i)

            elif strategy == "clever":
                # extract "population" from dict
                d_raw = player.get_stock()
                d = {key: max(0, value) for key, value in d_raw.items() if key != "population"}

                # get key with lowest value
                lowest_value_key = min(d, key=d.get)
                prior_buildings = building_factory.json_dict.get(lowest_value_key, [])
                prior_buildings_list = list(prior_buildings.keys())
                building = random.choice(prior_buildings_list)
                building_factory.build(building, i)

            elif strategy == "cleverer":
                pop_limit = i.population_limit
                possible_buildings = building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(i.population)
                possible_population_buildings = [_ for _ in possible_buildings if _ in i.population_buildings]

                # if planet can build population:
                if "food" in i.possible_resources and "population" in i.possible_resources:
                    if not "town" in i.buildings:
                        building_factory.build("town", i)
                    elif i.population > i.population_limit:
                        building_factory.build(random.choice(possible_population_buildings), i)

                # get key with lowest production
                r = random.randint(0, 2)
                if r == 0:
                    d_raw = player.production
                    d = {key: max(0, value) for key, value in d_raw.items() if key != "energy"}
                else:
                    d = player.production

                lowest_production_key = min(d, key=player.production.get)
                prior_buildings = building_factory.json_dict.get(lowest_production_key, [])
                prior_buildings_list = list(prior_buildings.keys())
                building = random.choice(prior_buildings_list)

                random_list = [building, building, building, building, building,
                               random.choice(building_factory.get_all_building_names())]
                building_factory.build(random.choice(random_list), i)

    def set_target(self):

        target = None

        reachable_unexplored_planets = []
        if random.randint(0,6) == 0:
            self.set_random_target(sprite_groups.ships.sprites())
            return
        self.reachable_planets = [_ for _ in config.app.sprite_groups.planets.sprites()
                                  if
                                  self.parent.get_max_travel_range() > math.dist(self.parent.rect.center, _.rect.center) / pan_zoom_handler.zoom]

        if self.parent.target:
            if self.parent.target in self.reachable_planets:
                if not self.parent.target == self.get_nearest_target(self.reachable_planets):
                    self.parent.target = self.get_nearest_target(self.reachable_planets)
                    return
                return
            else:
                self.parent.target = self.get_nearest_target(self.reachable_planets)
        if self.parent.energy > self.parent.energy_max / 2:

            if self.reachable_planets:
                reachable_unexplored_planets = [_ for _ in self.reachable_planets if _.explored]
                if not reachable_unexplored_planets:
                    self.parent.target = random.choice(self.reachable_planets)

            else:
                self.parent.target = random.choice(config.app.sprite_groups.planets.sprites())

        else:
            # set reloader target if energy is low
            reloaders = [_ for _ in sprite_groups.planets.sprites() if _.type == "sun"]
            if reloaders:
                self.set_nearest_target(reloaders)
            else:
                reloaders = [_ for _ in sprite_groups.planets.sprites() if _.production["energy"] > 0]
                if reloaders:
                    self.set_nearest_target(reloaders)
                else:
                    reloaders = [_ for _ in sprite_groups.ships.sprites() if _.energy > self.parent.energy]
                    if reloaders:
                        self.set_nearest_target(reloaders)
                    else:
                        self.set_random_target(sprite_groups.ships.sprites())

        # # set random target if enough energy
        # if self.parent.energy > self.parent.energy_max / 2:
        #     r = random.randint(0, 2)
        #     self.set_nearest_target(sprite_groups.planets.sprites())
        # else:
        #     # set reloader target if energy is low
        #     reloaders = [_ for _ in sprite_groups.planets.sprites() if _.type == "sun"]
        #     if len(reloaders) > 0:
        #         self.parent.target = self.set_nearest_target(sprite_groups.planets.sprites())
        #     else:
        #         self.set_random_target(sprite_groups.ships.sprites())

    def play(self):
        self.set_target()
        self.create_economy("cleverer")
        player = config.app.player

        # # economy
        # for i in config.app.explored_planets:
        #     # extract "population" from dict
        #     stock = player.get_stock()
        #     d = {key: max(0, value) for key, value in stock.items() if key != "population"}
        #
        #     lowest_production = min(player.production.values())
        #     # get key with lowest value
        #     lowest_value_key = min(d, key=d.get)
        #     prior_buildings = building_factory.json_dict.get(lowest_value_key, [])
        #     prior_buildings_list = list(prior_buildings.keys())
        #     building = random.choice(prior_buildings_list)
        #
        #     random_list = [building, building, building, building, building, building,
        #                    random.choice(building_factory.get_all_building_names())]
        #     building_factory.build(random.choice(random_list), i)

    def update(self):
        for i in self.reachable_planets:
            pygame.draw.line(self.parent.win, (255, 0, 0), self.parent.rect.center, i.rect.center)

        nearest = self.get_nearest_target(self.reachable_planets)
        if nearest:
            pygame.draw.line(self.parent.win, (0, 255, 0), self.parent.rect.center, nearest.rect.center)

        actual_time = time.time()
        self.task_change_interval = self.task_change_interval_raw / config.game_speed

        if actual_time - self.last_task_time > self.task_change_interval + random.randint(-10, 10):
            self.last_task_time = actual_time
            if config.enable_autopilot:
                self.play()
            # self.create_economy("random")
            # self.create_economy("clever")
            # self.create_economy("clever")
            # print("autopilot.update:")
