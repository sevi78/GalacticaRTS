import math

import pygame.mouse

from source.configuration.game_config import config
from source.gui.event_text import event_text
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.time_handler import time_handler
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship_state_engine import PanZoomShipStateEngine
from source.text.info_panel_text_generator import info_panel_text_generator

SHIP_SPEED = 1.5
SHIP_GUN_POWER = 30
SHIP_GUN_POWER_MAX = 50
SHIP_INSIDE_SCREEN_BORDER = 10
SHIP_ITEM_COLLECT_DISTANCE = 30
SHIP_ROTATE_CORRECTION_ANGLE = 90
SHIP_TARGET_OBJECT_RESET_DISTANCE = 15
SHIP_RELOAD_MAX_DISTANCE = 300
SHIP_RELOAD_MAX_DISTANCE_MAX = 600
SHIP_ENERGY_USE = 0.1
SHIP_ENERGY_USE_MAX = 10
SHIP_ENERGY = 10000
SHIP_ENERGY_MAX = 10000
SHIP_ENERGY_RELOAD_RATE = 0.1
SHIP_ORBIT_SPEED = 0.5
SHIP_ORBIT_SPEED_MAX = 0.6

"""
TODO:
remove all variables for resources, self.resources must be used

"""


# disabled_functions = ["set_info_text", "set_tooltip", "submit_tooltip", "reload_ship"]
# for i in disabled_functions:
#     disabler.disable(i)
#
# @auto_disable

class PanZoomShipParams:
    def __init__(self, **kwargs):

        self.id = len(sprite_groups.ships)
        self.reloading = None
        self.reload_max_distance_raw = SHIP_RELOAD_MAX_DISTANCE
        self.reload_max_distance = self.reload_max_distance_raw
        self.reload_max_distance_max_raw = SHIP_RELOAD_MAX_DISTANCE_MAX
        self.reload_max_distance_max = self.reload_max_distance_max_raw

        self.name = kwargs.get("name", "noname_ship")
        self.type = "ship"
        self.parent = kwargs.get("parent")
        self.hum = sounds.hum1
        self.sound_channel = 1
        self.energy_use = SHIP_ENERGY_USE
        self.energy_use_max = SHIP_ENERGY_USE_MAX
        self.info_panel_alpha = kwargs.get("info_panel_alpha", 255)

        # load_from_db Game variables
        self.food = kwargs.get("food", 100)
        self.food_max = 200
        self.minerals = kwargs.get("minerals", 100)
        self.minerals_max = 200
        self.water = kwargs.get("water", 100)
        self.water_max = 200
        self.population = kwargs.get("population", 100)
        self.population_max = 200
        self.technology = kwargs.get("technology", 100)
        self.technology_max = 200
        self.energy_max = SHIP_ENERGY_MAX
        self.energy = SHIP_ENERGY

        self.resources = {
            "minerals": self.minerals,
            "food": self.food,
            "energy": self.energy,
            "water": self.water,
            "technology": self.technology
            }
        self.specials = []

        self.energy_reloader = None
        self.energy_reload_rate = SHIP_ENERGY_RELOAD_RATE
        self.move_stop = 0
        self.crew = 7
        self.crew_max = 12
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war, no needed anymore
        self.fog_of_war_radius = 100
        self.fog_of_war_radius_max = 300

        # upgrade
        self.upgrade_factor = 1.5
        self.upgrade_factor_max = 3.0

        # tooltip
        self.tooltip = ""

        # states
        self.state_engine = PanZoomShipStateEngine(self)

        # self.state = "sleeping"

    def set_resources(self):
        self.resources = {
            "minerals": self.minerals,
            "food": self.food,
            "population": self.population,
            "water": self.water,
            "technology": self.technology
            }

    def set_info_text(self):
        if not self == config.app.ship:
            if self.collide_rect.collidepoint(pygame.mouse.get_pos()):
                text = info_panel_text_generator.create_info_panel_ship_text(self)
                self.parent.info_panel.set_text(text)
                self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)
            return

        text = info_panel_text_generator.create_info_panel_ship_text(self)
        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)

    def set_tooltip(self):
        self.tooltip = f"{self.name}:  speed: {self.speed}"

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                config.tooltip_text = self.tooltip

    def reload_ship(self):
        """ This reloads the ship's energy """
        self.reloading = False
        # if there is no reloader or distane too far: return
        if not self.energy_reloader or math.dist(self.rect.center, self.energy_reloader.rect.center) > self.reload_max_distance:
            return

        # if there is a reloader and it is a planet, and the planet has enough energy_production and the player has enough energy
        if self.energy_reloader.type == "planet" and self.energy_reloader.economy_agent.production["energy"] > 0 and \
                self.energy_reloader.owner in self.parent.players.keys() and \
                self.parent.players[self.energy_reloader.owner].stock["energy"] - self.energy_reload_rate * \
                self.energy_reloader.economy_agent.production["energy"] > 0 and \
                self.energy < self.energy_max:

            # add energy
            self.reloading = True
            self.energy += self.energy_reload_rate * self.energy_reloader.economy_agent.production[
                "energy"] * time_handler.game_speed

            # subtract energy from player stock
            self.parent.players[self.energy_reloader.owner].stock["energy"] -= (
                    self.energy_reload_rate * self.energy_reloader.economy_agent.production[
                "energy"] * time_handler.game_speed)

        # if its a sun and ship needs energy
        elif self.energy_reloader.type == "sun" and self.energy < self.energy_max:
            self.reloading = True
            self.energy += self.energy_reload_rate * time_handler.game_speed

        # if its a ship and ship needs energy
        elif hasattr(self.energy_reloader, "crew") and self.energy_reloader.energy > 0 and \
                self.energy_reloader.energy - self.energy_reload_rate * time_handler.game_speed > 0 and \
                self.energy < self.energy_max:
            self.reloading = True
            self.energy += self.energy_reload_rate
            self.energy_reloader.energy -= self.energy_reload_rate * time_handler.game_speed

        if self.energy >= self.energy_max:
            self.reloading = False
            event_text.set_text(f"{self.name} reloaded successfully!!!", obj=self, sender=self.owner)
            sounds.stop_sound(self.sound_channel)

        if self.reloading:
            self.state_engine.set_state("reloading")
