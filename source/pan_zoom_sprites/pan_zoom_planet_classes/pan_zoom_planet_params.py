import pygame

from source.database.database_access import create_connection, get_database_file_path
from source.gui.event_text import event_text
from source.multimedia_library.images import images, pictures_path, get_image
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.gui.panels.info_panel_components.info_panel_text_generator import info_panel_text_generator


class PanZoomPlanetParams:
    def __init__(self, kwargs):
        self._image_name_small = kwargs.get("image_name_small")
        self.image_name_big = kwargs.get("image_name_big")
        self.orbit_radius = 0
        self.font_size = kwargs.get('font_size', 20)
        self.font = kwargs.get('font', pygame.font.SysFont(global_params.font_name, self.font_size))
        self.check_image = get_image("check.png")

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

        # dirty hack to make shure athmosphere_raw gets updated
        if value != "":
            if self.has_atmosphere == 1:
                self.atmosphere_raw = images[pictures_path]["atmospheres"][value]
                self.atmosphere = self.atmosphere_raw
        else:
            self.atmosphere_raw = None
            self.atmosphere = self.atmosphere_raw

    def set_atmosphere(self):
        if self.has_atmosphere == 1:
            conn = create_connection(get_database_file_path())
            cur = conn.cursor()
            self.atmosphere_name = cur.execute(f"select atmosphere_name from planets where id = {self.id}").fetchone()[
                0]
            conn.close()

            self.atmosphere = images[pictures_path]["atmospheres"][self.atmosphere_name]
            self.atmosphere_raw = self.atmosphere

    def set_planet_name_(self):
        if self.property == "ship" or "ufo":
            return

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
        # if self.parent.build_menu_visible: return
        # self.parent.info_panel.visible = True

        if self.explored:
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
        # # print (gen_text)
        #
        # if self.explored:
        #     text = self.info_text_raw
        #     self.info_text = text
        #     self.parent.info_panel.set_planet_image(self.image_raw)
        # else:
        #     text = "unknown planet" + ":\n\n"
        #     text += "resources: ???\n"
        #     text += "energy: ???\n"
        #
        # text += f"orbit_object_id:{self.orbit_object_id}\n"
        # text += f"orbit_object:{self.orbit_object}\n"
        # if self.orbit_angle != None and self.orbit_angle != "None":
        #     text += f"orbit_angle:{int(self.orbit_angle)}\n"
        # else:
        #     text += f"orbit_angle:None\n"
        # text += f"orbit_distance:{int(self.orbit_distance)}\n"
        # text += f"x,y:{int(self.world_x), int(self.world_y)}\n"
        # text += f"_x,_y:{int(self.screen_x), int(self.screen_y)}\n"
        # text += f"smiley hidden:{self.smiley_button._hidden}\n, smiley disabled:{self.smiley_button._disabled}\n"
        # text += f"smiley.screen_x:{self.smiley_button.screen_x}, smiley_y:{self.smiley_button.screen_y}\n"
        # text += f"smiley.x:{self.smiley_button.x}, smiley.y:{self.smiley_button.y}\n"
        #
        # self.info_text = text
        # try:
        #     self.parent.info_panel.set_text(self.info_text)
        #     self.parent.info_panel.set_planet_image(self.image_raw)
        # except AttributeError as e:
        #     print("set_info_text(self):", e)
        #
        # self.parent.info_panel.set_planet_image(self.image_raw)

    def get_explored(self):
        """
        called only once when the planet gets explored
        shows buttons ect
        """
        if self.type == "sun":
            self.explored = True
            self.just_explored = True
            self.string = self.name
            return

        sounds.play_sound(sounds.happy, channel=4)

        self.parent.set_selected_planet(self)
        if not self in self.parent.explored_planets:
            self.parent.add_explored_planet(self)
        self.explored = True
        self.show_overview_button()
        self.string = self.name

        # set event text
        event_text.text = f"Gratulation! you have reached a the Planet {self.name} !"
        self.parent.update_building_button_widgets()
