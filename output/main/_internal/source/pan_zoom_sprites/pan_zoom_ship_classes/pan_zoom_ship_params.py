from source.gui.event_text import event_text
from source.handlers.widget_handler import WidgetHandler
from source.text.info_panel_text_generator import info_panel_text_generator
from source.configuration import global_params
from source.multimedia_library.sounds import sounds
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import get_distance

SHIP_SPEED = 1.5
SHIP_GUN_POWER = 30
SHIP_GUN_POWER_MAX = 50
SHIP_INSIDE_SCREEN_BORDER = 10
SHIP_ITEM_COLLECT_DISTANCE = 30
SHIP_ROTATE_CORRECTION_ANGLE = 90
SHIP_TARGET_OBJECT_RESET_DISTANCE = 15
SHIP_RELOAD_MAX_DISTANCE = 300
SHIP_RELOAD_MAX_DISTANCE_MAX = 600
SHIP_ENERGY_USE = 0.001
SHIP_ENERGY = 10000
SHIP_ENERGY_MAX = 10000
SHIP_ENERGY_RELOAD_RATE = 0.1
SHIP_ORBIT_SPEED = 0.5
SHIP_ORBIT_SPEED_MAX = 0.6


class PanZoomShipParams():
    """

    """

    def __init__(self, **kwargs):
        self.id = len(sprite_groups.ships)
        self.reload_max_distance_raw = SHIP_RELOAD_MAX_DISTANCE
        self.reload_max_distance = self.reload_max_distance_raw
        self.reload_max_distance_max_raw = SHIP_RELOAD_MAX_DISTANCE_MAX
        self.reload_max_distance_max = self.reload_max_distance_max_raw

        self.name = kwargs.get("name", "noname_ship")
        self.parent = kwargs.get("parent")
        self.hum = sounds.hum1
        self.sound_channel = 1
        self.energy_use = SHIP_ENERGY_USE
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

        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "energy":self.energy,
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

        # fog of war
        self.fog_of_war_radius = 100
        self.fog_of_war_radius_max = 300
        # self.parent.fog_of_war.draw_fog_of_war(self)

        # upgrade
        self.upgrade_factor = 1.5
        self.upgrade_factor_max = 3.0

        # tooltip
        self.tooltip = ""

        # uprade
        self.building_slot_amount = 1
        self.building_cue = 0
        self.buildings_max = 10
        self.buildings = []



    def __delete__(self, instance):
        # remove all references
        # if self in self.parent.ships:
        #     self.parent.ships.remove(self)

        if self in sprite_groups.ships:
            sprite_groups.ships.remove(self)

        if self.target_object in sprite_groups.ships:
            sprite_groups.ships.remove(self.target_object)

        try:
            if self in self.parent.box_selection.selectable_objects:
                self.parent.box_selection.selectable_objects.remove(self)
        except:
            pass

        WidgetHandler.remove_widget(self.progress_bar)

        self.progress_bar = None
        self.kill()

    def set_resources(self):
        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

    def set_info_text(self):
        if not self == global_params.app.ship:
            return

        text = info_panel_text_generator.create_info_panel_ship_text(self)
        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image_raw, alpha=self.info_panel_alpha)

    def set_tooltip(self):
        text = "selected: " + str(self.selected)
        self.tooltip = self.name + ": " + " speed: " + str(self.speed) + "e, scanner range: " + str(self.fog_of_war_radius) + text

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                global_params.tooltip_text = self.tooltip

    def reload_ship(self):
        if self.energy_reloader:
            dist = get_distance(self.rect.center, self.energy_reloader.rect.center)

            if dist > self.reload_max_distance:
                return

            # if reloader is a planet
            if hasattr(self.energy_reloader, "production"):
                if self.energy_reloader.production["energy"] > 0:
                    if self.parent.player.energy - self.energy_reload_rate * self.energy_reloader.production[
                        "energy"] > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate * self.energy_reloader.production[
                                "energy"] * global_params.game_speed
                            self.parent.player.energy -= self.energy_reload_rate * self.energy_reloader.production[
                                "energy"] * global_params.game_speed
                            self.flickering()
                        else:
                            event_text.text = "PanZoomShip reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)

                if self.energy_reloader.type == "sun":
                    if self.energy < self.energy_max:
                        self.energy += self.energy_reload_rate * global_params.game_speed
                        self.flickering()

            # if relaoder is a ship
            elif hasattr(self.energy_reloader, "crew"):
                if self.energy_reloader.energy > 0:
                    if self.energy_reloader.energy - self.energy_reload_rate * global_params.game_speed > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate
                            self.energy_reloader.energy -= self.energy_reload_rate * global_params.game_speed
                            self.flickering()
                        else:
                            event_text.text = "PanZoomShip reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)
        else:
            sounds.stop_sound(self.sound_channel)


