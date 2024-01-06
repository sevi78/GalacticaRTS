import random
import time

from source.factories.building_factory import building_factory
from source.handlers.pan_zoom_sprite_handler import sprite_groups, PanZoomLayeredUpdates
from source.utils import global_params
from source.utils.positioning import get_distance


class AutopilotHandler:
    def __init__(self, parent):
        self.parent = parent
        self.last_task_time = time.time()
        self.task_change_interval = 5
        self.tasks = ["set_random_target"]
        self.task = ""

    def set_random_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = random.choice(targets)
        self.parent.orbit_object = None

    def get_nearest_target(self, targets):
        nearest_target = None
        nearest_distance = float('inf')  # Initialize with infinity

        for target in targets:
            distance = get_distance(self.parent.rect.center, target.rect.center)  # Replace with actual positions
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_target = target

        return nearest_target

    def set_nearest_target(self, targets: PanZoomLayeredUpdates):
        self.parent.target = self.get_nearest_target(targets)
        self.parent.orbit_object = None

    def create_economy(self, strategy):
        player = global_params.app.player

        for i in global_params.app.explored_planets:
            if strategy == "random":
                building_factory.build(random.choice(building_factory.get_all_building_names()), i)

            elif strategy == "clever":
                # extract "city" from dict
                d_raw = player.get_stock()
                d = {key: max(0, value) for key, value in d_raw.items() if key != "city"}

                # get key with lowest value
                lowest_value_key = min(d, key=d.get)
                prior_buildings = building_factory.json_dict.get(lowest_value_key, [])
                building = random.choice(prior_buildings)
                building_factory.build(building, i)

    def update(self):
        actual_time = time.time()
        if actual_time - self.last_task_time > self.task_change_interval:
            self.last_task_time = actual_time
            # set random target if enough energy
            if self.parent.energy > self.parent.energy_max / 3:
                self.set_random_target(sprite_groups.planets.sprites())
            else:
                # set reloader target
                self.set_random_target(sprite_groups.ships.sprites())

            #self.create_economy("random")
            self.create_economy("clever")
            print("autopilot.update:")
