import math
import time

from source.configuration.game_config import config
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class Spacestation:
    def __init__(self, parent):
        self.produce_start = time.time()
        self.update_interval = 1
        self.parent = parent
        self.nearest_sun = sprite_groups.get_nearest_obj_by_type(sprite_groups.planets.sprites(), "sun", self.parent)
        self.production_energy = 0

    def set_production_energy(self):
        # update timer
        if time.time() > self.produce_start + self.update_interval:

            self.produce_start = time.time()

            #
            dist = math.dist(self.parent.rect.center, self.nearest_sun.rect.center)
            print(f"self.nearest_sun: {self.nearest_sun}, dist: {dist}")
            max_production = 10000
            self.production_energy = max_production / (dist * pan_zoom_handler.zoom)

    def produce_energy(self):
        print (f"produce_energy:")
        self.set_production_energy()
        self.parent.energy += self.production_energy




