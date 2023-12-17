from pprint import pprint

import pygame.display
from source.database.file_handler import load_file, write_file
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups



class LevelFactory:
    def __init__(self, win):
        self.win = win

    def save_level(self, level: int, data: dict):
        print (f"keys:{data['celestial_objects']['0'].keys()}")
        #pprint(f"data:{data}")
        view = []
        for planet in sprite_groups.planets.sprites():
            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    data["celestial_objects"][str(planet.id)][key] = getattr(planet, key)
                    view.append(f"{key}:{value}")

        write_file(f"level_{level}.json", data)
        pprint(f"save_level: wip{view}")

    def load_level(self, level: int):
        print("load level:", level)
        return load_file(f"level_{level}.json")

    def get_planet_amount(self, data):
        return len(data.keys())


level_factory = LevelFactory(pygame.display.get_surface())
