import math
from source.handlers.time_handler import time_handler

from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class Spacestation:
    def __init__(self, parent):
        self.produce_start = time_handler.time
        self.update_interval = 10
        self.parent = parent
        self.nearest_sun = sprite_groups.get_nearest_obj_by_type(sprite_groups.planets.sprites(), "sun", self.parent)
        self.production = {}
        self.production["energy"] = 0

    def set_production_energy(self):
        # update timer
        if time_handler.time > self.produce_start + self.update_interval:
            self.produce_start = time_handler.time

            #
            dist = math.dist(self.parent.rect.center, self.nearest_sun.rect.center)
            # print(f"self.nearest_sun: {self.nearest_sun}, dist: {dist}")
            max_production = 10000
            self.production["energy"] = max_production / (dist * pan_zoom_handler.zoom)

    def produce_energy(self):
        # print (f"produce_energy:")
        self.set_production_energy()
        self.parent.energy += self.production["energy"]
