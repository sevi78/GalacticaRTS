import random

import pygame.display

from source.configuration.game_config import config
from source.handlers.file_handler import load_file
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.interfaces.interface import InterfaceData
from source.multimedia_library.images import get_image_names_from_folder
from source.pan_zoom_sprites.pan_zoom_ufo import PanZoomUfo
from source.text.info_panel_text_generator import info_panel_text_generator
from source.text.tooltip_gen import tooltip_generator

ENEMY_SPAWN_INTERVAL = 1555
pan_zoom_ufo_config = load_file("enemy_handler_config.json", "config")


# pan_zoom_ufo_config = load_file("pan_zoom_ufo_config.json")
# pan_zoom_ufo_config["spawn_interval"] = ENEMY_SPAWN_INTERVAL

class EnemyHandler(InterfaceData):
    """
    Summary
    The EnemyHandler class is responsible for managing the spawning of UFOs in the game. It keeps track of the spawn
    interval, the time since the last spawn, and the explored planets with aliens. It also provides a method to check if
    the UFO limit has been reached and a method to spawn a UFO on a random explored planet.

    Example Usage

    enemy_handler = EnemyHandler(60)  # Create an instance of EnemyHandler with a spawn interval of 60
    enemy_handler.update()  # Update the enemy handler, which will spawn a UFO if conditions are met

    Code Analysis

    Main functionalities

    Manages the spawning of UFOs in the game
    Keeps track of the spawn interval and the time since the last spawn
    Keeps track of the explored planets with aliens
    Checks if the UFO limit has been reached
    Spawns a UFO on a random explored planet

    Methods
    __init__(self, spawn_interval): Initializes the EnemyHandler instance with the given spawn interval and sets up the
    interface data.
    setup(self): Loads the configuration data from a file and updates the instance variables accordingly.
    ufo_limit_reached(self): Checks if the UFO limit has been reached based on the player's population and the number of
    existing UFOs.
    set_explored_planets_with_aliens(self): Updates the list of explored planets with aliens.
    update(self): Updates the enemy handler, incrementing the time since the last spawn and spawning a UFO if conditions
    are met.
    spawn_ufo(self, planet): Spawns a UFO on the given planet, creating a new instance of the PanZoomUfo class.

    Fields
    name: The name of the enemy handler.
    spawn_interval: The interval between UFO spawns.
    time_since_last_spawn: The time elapsed since the last UFO spawn.
    explored_planets_with_aliens: A list of explored planets that have aliens.
    win: The Pygame display surface.
    interface_variables: A dictionary of interface variables used for the user interface.
    """

    def __init__(self, interface_variables):
        self.name = "enemy handler"
        self.time_since_last_spawn = 0
        self.explored_planets_with_aliens = []
        self.win = pygame.display.get_surface()
        self.interface_variable_names = []
        self.ufo_id = 0
        self.explosion_gifs = get_image_names_from_folder("gifs", startswith_string="explosion")
        self.ufo_images = get_image_names_from_folder("ships", startswith_string="ufo")

        for dict_name, dict in interface_variables.items():
            for key, value in dict.items():
                setattr(self, key, value)
                setattr(self, key + "_max", value)
                if not key.endswith("_max"):
                    self.interface_variable_names.append(key)

        InterfaceData.__init__(self, self.interface_variable_names)
        self.setup()

    def setup(self):
        data = load_file("enemy_handler_config.json", "config")
        for name, dict in data.items():
            if name == self.name:
                for key, value in dict.items():
                    if key in self.__dict__:
                        setattr(self, key, value)

    def ufo_limit_reached(self):
        if config.app.player.population < 500:
            return True

        if len(sprite_groups.ufos.sprites()) * 1000 > config.app.player.population:
            return True

        return False

    def set_explored_planets_with_aliens(self):
        if config.app:
            self.explored_planets_with_aliens = [i for i in config.app.explored_planets if
                                                 i.alien_population != 0]

    def update(self):
        self.time_since_last_spawn += 1
        if self.time_since_last_spawn >= self.spawn_interval:
            if not self.explored_planets_with_aliens:
                self.set_explored_planets_with_aliens()

            if len(self.explored_planets_with_aliens) > 0 and not self.ufo_limit_reached():
                planet = random.choice(self.explored_planets_with_aliens)
                self.spawn_ufo(planet)
                self.time_since_last_spawn = 0

    def spawn_ufo(self, planet):
        x, y = pan_zoom_handler.screen_2_world(planet.screen_x, planet.screen_y)

        attitude = random.randint(0, 100)
        attitude_bool = 0 if attitude < 50 else 1


        ufo = PanZoomUfo(self.win,
            x,
            y,
            pan_zoom_ufo_config["enemy handler"]["width"],
            pan_zoom_ufo_config["enemy handler"]["height"],
            pan_zoom=pan_zoom_handler,
            image_name=self.ufo_images[attitude_bool],
            align_image="center",
            group="ufos",
            explosion_name=random.choice(self.explosion_gifs),
            tooltip="",
            infotext="",
            attitude=attitude,
            lifetime=random.randint(30, 60),
            explosion_relative_gif_size=5.0,
            id=self.ufo_id,
            layer=0,
            outline_thickness=1,
            outline_threshold=0)

        ufo.tooltip = tooltip_generator.create_ufo_tooltip(ufo)
        ufo.info_text = info_panel_text_generator.create_info_panel_ufo_text(ufo)
        self.ufo_id += 1
        return ufo


# Create an instance of the EnemyHandler class
enemy_handler = EnemyHandler(pan_zoom_ufo_config)
