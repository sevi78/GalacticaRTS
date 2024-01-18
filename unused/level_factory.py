import pygame.display
from source.handlers.file_handler import load_file, write_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class LevelFactory__:
    def __init__(self, win):
        self.win = win

    def save_level__(self, level: int, data: dict):
        print(f"keys:{data['celestial_objects']['0'].keys()}")
        # pprint(f"data:{data}")
        view = []
        for planet in sprite_groups.planets.sprites():
            for key, value in data["celestial_objects"][str(planet.id)].items():
                if hasattr(planet, key):
                    data["celestial_objects"][str(planet.id)][key] = getattr(planet, key)

            for ship in sprite_groups.ships.sprites():
                if not str(ship.id) in data["ships"].keys():
                    data["ships"][str(ship.id)] = {"name": "", "world_x": 0, "world_y": 0}
                for key, value in data["ships"][str(ship.id)].items():
                    data["ships"][str(ship.id)][key] = getattr(ship, key)

        write_file(f"level_{level}.json", data)





#level_factory = LevelFactory(pygame.display.get_surface())
