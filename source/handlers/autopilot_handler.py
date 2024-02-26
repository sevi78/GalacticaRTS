import copy
import math
import random
import time

import pygame.sprite

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import PanZoomLayeredUpdates
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet

TASK_CHANGE_INTERVAL = 220
BUILD_CHANGE_INTERVAL = 60


class AutopilotHandler:
    def __init__(self, parent):

        self.build_start_time = time.time() + random.randint(-BUILD_CHANGE_INTERVAL, BUILD_CHANGE_INTERVAL)

        self.build_change_interval_raw = BUILD_CHANGE_INTERVAL
        self.build_change_interval = copy.copy(BUILD_CHANGE_INTERVAL)
        self.reachable_planets = []
        self.parent = parent
        self.last_task_time = time.time() + random.randint(-TASK_CHANGE_INTERVAL, TASK_CHANGE_INTERVAL)
        self.task_change_interval_raw = TASK_CHANGE_INTERVAL
        self.task_change_interval = copy.copy(TASK_CHANGE_INTERVAL)

    def set_random_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = random.choice(targets)
        self.parent.orbit_object = None

    def get_nearest_target(self, targets: PanZoomLayeredUpdates):
        nearest_target = None
        nearest_distance = float("inf")  # Initialize with infinity

        for target in targets:
            distance = math.dist(self.parent.rect.center, target.rect.center)  # Replace with actual positions
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_target = target

        return nearest_target

    def set_nearest_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = self.get_nearest_target(targets)
        self.parent.orbit_object = None

    def build_based_on_strategy(self, planet: PanZoomPlanet, strategy):
        now = time.time()
        if not now - self.build_start_time < self.build_change_interval:
            return
        self.build_start_time = now

        player = config.app.player
        if strategy == "random":
            building_factory.build(random.choice(building_factory.get_all_building_names()), planet)
        elif strategy == "clever":
            stock = player.get_stock()
            stock_without_population = {key: max(0, value) for key, value in stock.items() if key != "population"}
            lowest_value_key = min(stock_without_population, key=stock_without_population.get)
            prior_buildings = building_factory.json_dict.get(lowest_value_key, [])
            prior_buildings_list = list(prior_buildings.keys())
            building = random.choice(prior_buildings_list)
            building_factory.build(building, planet)

        elif strategy == "cleverer":


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
            if building in planet.possible_resources:
                if building == "town":
                    # if planet can build population:
                    if "food" in planet.possible_resources and "population" in planet.possible_resources:
                        if not "town" in planet.buildings:
                            building_factory.build("town", planet)
                            return

                        elif planet.population > planet.population_limit:
                            building_factory.build(random.choice(planet.population_buildings), planet)
                            return
                else:
                    building_factory.build(building, planet)



    def create_economy(self, strategy):
        for planet in config.app.explored_planets:
            self.build_based_on_strategy(planet, strategy)

    def set_target(self):
        self.reachable_planets = [planet for planet in config.app.sprite_groups.planets.sprites()
                                  if
                                  self.parent.get_max_travel_range() > math.dist(self.parent.rect.center, planet.rect.center) / pan_zoom_handler.zoom]
        if self.reachable_planets:
            unexplored_planets = [planet for planet in self.reachable_planets if not planet.explored]
            if unexplored_planets:
                self.set_nearest_target(unexplored_planets)
            else:
                self.set_nearest_target(self.reachable_planets)
        else:
            self.set_nearest_target(config.app.sprite_groups.planets.sprites())

    def play(self):
        self.set_target()
        self.create_economy("cleverer")

    def update(self):
        for planet in self.reachable_planets:
            pygame.draw.line(self.parent.win, (255, 0, 0), self.parent.rect.center, planet.rect.center)

        nearest = self.get_nearest_target(self.reachable_planets)
        if nearest:
            pygame.draw.line(self.parent.win, (0, 255, 0), self.parent.rect.center, nearest.rect.center)

        actual_time = time.time()
        if not config.game_speed == 0:
            self.task_change_interval = self.task_change_interval_raw / config.game_speed
            self.build_change_interval = self.build_change_interval_raw / config.game_speed

        if actual_time - self.last_task_time > self.task_change_interval + random.randint(-10, 10):
            self.last_task_time = actual_time
            if self.parent.autopilot:
                self.play()
