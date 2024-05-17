import copy
import math
import random
import time

import pygame.sprite

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import PanZoomLayeredUpdates

TASK_CHANGE_INTERVAL = 220


class AutopilotHandler:
    def __init__(self, parent):
        self.reachable_planets = []
        self.parent = parent
        self.last_task_time = 0
        self.task_change_interval_raw = TASK_CHANGE_INTERVAL
        self.task_change_interval = copy.copy(TASK_CHANGE_INTERVAL)

    def set_random_target(self, targets: PanZoomLayeredUpdates) -> None:
        self.parent.target = random.choice(targets)
        self.parent.orbit_object = None

    def set_nearest_target(self, targets: [PanZoomLayeredUpdates]) -> None:
        self.parent.target = self.get_nearest_target(targets)
        self.parent.orbit_object = None

    def set_reachable_planets(self) -> None:
        self.reachable_planets = [
            planet for planet in config.app.sprite_groups.planets.sprites() if
            self.parent.get_max_travel_range() >
            math.dist(self.parent.rect.center, planet.rect.center) / pan_zoom_handler.zoom]

    def set_target(self) -> None:
        self.set_reachable_planets()
        if self.reachable_planets:
            unexplored_planets = [planet for planet in self.reachable_planets if not planet.explored]
            if unexplored_planets:
                self.set_nearest_target(unexplored_planets)
            else:
                self.set_nearest_target(self.reachable_planets)
        else:
            self.set_nearest_target(config.app.sprite_groups.planets.sprites())

    def set_task_change_interval(self) -> None:
        if not config.game_speed == 0:
            self.task_change_interval = self.task_change_interval_raw / config.game_speed

    def get_nearest_target(self, targets: [PanZoomLayeredUpdates]) -> object:
        nearest_target = None
        nearest_distance = float("inf")  # Initialize with infinity

        for target in targets:
            distance = math.dist(self.parent.rect.center, target.rect.center)  # Replace with actual positions
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_target = target

        return nearest_target

    def task_change_time_reached(self) -> bool:
        actual_time = time.time()
        if actual_time - self.last_task_time > self.task_change_interval + random.randint(-10, 10):
            self.last_task_time = actual_time
            return True
        return False

    def draw_debug_lines(self) -> None:
        for planet in self.reachable_planets:
            pygame.draw.line(self.parent.win, (255, 0, 0), self.parent.rect.center, planet.rect.center)

        nearest = self.get_nearest_target(self.reachable_planets)
        if nearest:
            pygame.draw.line(self.parent.win, (0, 255, 0), self.parent.rect.center, nearest.rect.center)

    def update(self):
        self.draw_debug_lines()
        self.set_task_change_interval()

        if self.task_change_time_reached():
            if self.parent.autopilot:
                self.set_target()
