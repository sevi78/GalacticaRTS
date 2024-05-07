import pygame

from source.game_play.ranking import Ranking
from source.gui.event_text import event_text
from source.handlers.player_handler import player_handler
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.configuration.game_config import config
from source.text.info_panel_text_generator import info_panel_text_generator


class PanZoomPlanetParams:
    def __init__(self, kwargs):
        self._image_name_small = kwargs.get("image_name_small")
        self._atmosphere_name = kwargs.get("atmosphere_name")
        self.image_name_big = kwargs.get("image_name_big")
        self.orbit_radius = 0
        self.font_size = kwargs.get('font_size', 20)
        self.font = kwargs.get('font', pygame.font.SysFont(config.font_name, self.font_size))
        self.show_text = True
        self.under_attack = False

        # rank
        self.ranking = Ranking()
        self.rank = "Cadet"

    @property
    def image_name_small(self):
        return self._image_name_small

    @image_name_small.setter
    def image_name_small(self, value):
        self._image_name_small = value
        # dirty hack to make shure image_raw gets updated
        self.image_raw = get_image(value)

    @property
    def atmosphere_name(self):
        return self._atmosphere_name

    @atmosphere_name.setter
    def atmosphere_name(self, value):
        self._atmosphere_name = value

        if value != "":
            self.gif = self._atmosphere_name
            self.setup_gif_handler()
        else:
            if hasattr(self, "gif_handler"):
                if self.gif_handler:
                    self.gif_handler.kill()

    def set_planet_name(self):
        planets_with_same_orbit_object_id = [i for i in sprite_groups.planets if
                                             i.orbit_object_id == self.orbit_object_id]
        sorted_planets = sorted(planets_with_same_orbit_object_id, key=lambda planet: planet.orbit_distance)

        distance_string = self.name
        for index, planet in enumerate(sorted_planets):
            if not self.orbit_distance == 0.0:
                if planet == self:
                    if self.orbit_object:
                        distance_string = f"{self.orbit_object.name} - {chr(64 + index)}"

        self.name = distance_string

    def set_info_text(self):
        """
        sets the text used for the info_panel
        """

        if self.explored or self.owner != -1:
            gen_text = info_panel_text_generator.create_info_panel_planet_text(self)
            self.info_text = gen_text
        else:
            text = "unknown planet" + ":\n\n"
            text += "resources: ???\n"
            text += "energy: ???\n"
            self.info_text = text

        self.parent.info_panel.set_text(self.info_text)
        self.parent.info_panel.set_planet_image(self.image_raw)
        return

    def get_explored(self, owner):

        """
        called only once when the planet gets explored
        shows buttons ect
        """
        # set owner
        if self.owner != owner:
            if self.owner != -1:
                event_text.set_text(f"Bad Luck! the planet {self.name} belongs to an alien species !", obj=self)
                return

        self.owner = owner
        self.player_color = pygame.color.THECOLORS.get(player_handler.get_player_color(self.owner))

        if self.type == "sun":
            self.explored = True
            self.just_explored = True
            self.string = self.name
            self.hide_overview_button()
            return

        sounds.play_sound(sounds.happy, channel=4)

        self.parent.set_selected_planet(self)
        if not self in self.parent.explored_planets:
            self.parent.add_explored_planet(self)

        self.explored = True
        self.show_overview_button()
        self.string = self.name

        # set event text
        event_text.set_text(f"Gratulation! you have reached a the Planet {self.name} !", obj=self)
        self.parent.update_building_button_widgets()
