import math

from source.gui.event_text import event_text
from source.gui.widgets.widget_handler import WidgetHandler
from source.utils import global_params
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils.positioning import get_distance

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

        self.name = kwargs.get("name", "noname")
        self.parent = kwargs.get("parent")
        self.hum = sounds.hum1
        self.sound_channel = 1
        self.energy_use = SHIP_ENERGY_USE

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

        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

        self.energy_max = SHIP_ENERGY_MAX
        self.energy = SHIP_ENERGY
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

    def __delete__(self, instance):
        # remove all references
        if self in self.parent.ships:
            self.parent.ships.remove(self)

        if self in sprite_groups.ships:
            sprite_groups.ships.remove(self)

        if self.target_object in sprite_groups.ships:
            sprite_groups.ships.remove(self.target_object)

        if self in self.parent.box_selection.selectable_objects:
            self.parent.box_selection.selectable_objects.remove(self)

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

        text = self.name + ":\n\n"
        text += "experience: " + str(self.experience) + "\n"
        text += "rank: " + self.rank + "\n\n"
        text += "resources loaded: " + "\n\n"
        text += "water: " + str(self.water) + "/" + str(self.water_max) + "\n"
        text += "energy: " + str(int(self.energy)) + "/" + str(int(self.energy_max)) + "\n"
        text += "food: " + str(self.food) + "/" + str(self.food_max) + "\n"
        text += "minerals: " + str(self.minerals) + "/" + str(self.minerals_max) + "\n"
        text += "technology: " + str(self.technology) + "/" + str(self.technology_max) + "\n\n"
        text += "speed: " + str(self.speed) + "\n"
        text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        text += "crew: " + str(self.crew) + "\n"

        if self.debug:
            text += "\n\ndebug:\n"

            text += "selected: " + str(self.selected) + "\n"

            if self.energy_reloader:
                text += "reloader: " + str(self.energy_reloader.name) + "\n"
            else:
                text += "reloader: " + str(None) + "\n"

            text += "move_stop: " + str(self.move_stop) + "\n"
            text += "moving: " + str(self.moving) + "\n"
            text += "position, x,y:" + str(int(self.get_screen_x())) + "/" + str(int(self.get_screen_y()))

            if self.target:
                text += "\ntarget: " + str(self.target.name) + "\n"
            else:
                text += "\ntarget: " + str(None) + "\n"

            if self.orbit_object:
                text += f"orbit_object:{self.orbit_object.name}\n"
            else:
                text += f"orbit_object: None\n"

            if self.orbit_angle:
                text += f"orbit_angle:{self.orbit_angle}\n"
            else:
                text += f"orbit_angle:{None}\n"

            if self.enemy:
                text += f"enemy:{self.enemy}\n"
                text += f"distance:{get_distance(self.rect.center, self.enemy.rect.center)}\n"

            else:
                text += f"enemy:{None}\n"

            text += f"target_reached:{self.target_reached}\n"

        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image_raw)

    def set_tooltip(self):
        text = "selected: " + str(self.selected)
        self.tooltip = self.name + ": " + " speed: " + str(self.speed) + "e, scanner range: " + str(self.fog_of_war_radius) + text

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                global_params.tooltip_text = self.tooltip

    def get_distance_to__(self, obj):
        if not obj:
            return 0

        x = self.get_screen_x()
        y = self.get_screen_y()
        x1 = obj.get_screen_x()
        y1 = obj.get_screen_y()
        distance = math.dist((x, y), (x1, y1))

        return distance

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

    def upgrade(self, key):
        setattr(self, key, getattr(self, key) * self.upgrade_factor)
