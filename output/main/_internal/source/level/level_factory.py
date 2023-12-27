import pygame.display
from source.database.file_handler import load_file, write_file
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class LevelFactory:
    def __init__(self, win):
        self.win = win

    def save_level(self, level: int, data: dict):
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

    def load_level(self, level: int):
        print("load level:", level)
        return load_file(f"level_{level}.json")

    def get_planet_amount(self, data):
        return len(data.keys())


level_factory = LevelFactory(pygame.display.get_surface())
