import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING, BUTTON_SIZE
from source.gui.widgets.checkbox import Checkbox

from source.gui.widgets.widget_handler import WidgetHandler
from source.level.level_factory import level
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups, PanZoomLayeredUpdates
from source.universe.universe_background import universe_factory
from source.utils import global_params


class DebugEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        # debug
        self.quadrants_debug = False
        self.celestials_debug = False
        self.ships_debug = False
        self.planets_debug = False
        self.ufos_debug = False
        self.missiles_debug = False

        #  widgets
        self.widgets = []

        self.max_height = height

        # create widgets
        self.create_checkboxes()
        self.create_close_button()
        self.create_save_button(lambda: print("no function"), "save , not working yet")

        # hide initially
        self.hide()

    def create_checkboxes(self):
        """"""

        y = self.world_y + TOP_SPACING + self.text_spacing
        x = self.world_width / 2 + BUTTON_SIZE * 2

        checkbox_missiles = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="missiles", image_name="missile42x17.gif", tooltip="debug missiles", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_missiles)
        self.widgets.append(checkbox_missiles)

        checkbox_ships = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="ships", image_name="spaceship_30x30.png", tooltip="debug spaceships", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_ships)
        self.widgets.append(checkbox_ships)

        checkbox_planets = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="planets", image_name="Zeta Bentauri_60x60.png", tooltip="debug planets", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_planets)
        self.widgets.append(checkbox_planets)

        checkbox_ufos = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="ufos", image_name="ufo_74x30.png", tooltip="debug ufos", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_ufos)
        self.widgets.append(checkbox_ufos)

        checkbox_celestials = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="celestials", image_name="asteroid_40x33.png", tooltip="debug celestial objects", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_celestials)
        self.widgets.append(checkbox_celestials)

        checkbox_quadrant = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="quadrants", image_name="grid_icon.png", tooltip="debug quadrants", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_quadrant)
        self.widgets.append(checkbox_quadrant)

        debug_checkbox = Checkbox(
            self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
            color=self.frame_color,
            key="debug_icon", tooltip="debug", onClick=lambda: print("debug: ",
                global_params.debug), layer=9, parent=self)

        self.checkboxes.append(debug_checkbox)
        self.widgets.append(debug_checkbox)

        for i in self.checkboxes:
            i.checked = False

    def set_debug_to_objects(self, key):
        if key in sprite_groups.__dict__:
            for obj in getattr(sprite_groups, key).sprites():
                obj.debug = getattr(self, key + "_debug")

        if key == "quadrants":
            for k, v in level.quadrants.items():
                v.debug = getattr(self, key + "_debug")

    def get_checkbox_values(self):
        """gets the values from the checkboxes and calls update_planet_resources()"""
        self.checkbox_values = [i.key for i in self.checkboxes if i.checked]
        for i in self.checkboxes:
            if hasattr(self, i.key + "_debug"):
                setattr(self, i.key + "_debug", i.checked)
                self.set_debug_to_objects(i.key)

            if i.key == "debug_icon":
                global_params.debug = i.checked

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            y = self.world_y + TOP_SPACING + self.text_spacing
            self.draw_text(self.world_x + self.text_spacing, y, 200, 30, "Debug:")

            celestals = len(WidgetHandler.get_all_widgets())

            y += self.text_spacing * 2

            self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                f"pan_zoom.zoom: {pan_zoom_handler.zoom}")
            y += self.text_spacing

            self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                f"pan_zoom.world_offset_x: {pan_zoom_handler.world_offset_x}")
            y += self.text_spacing

            self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                f"pan_zoom.world_offset_y: {pan_zoom_handler.world_offset_y}")
            y += self.text_spacing * 2

            self.draw_text(self.world_x + self.text_spacing, y, 200, 20, f"celestials: {celestals}")
            y += self.text_spacing

            self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                f"quadrants: {len(level.quadrants)}")
            y += self.text_spacing

            for key, value in universe_factory.celestial_objects.items():
                self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                    f"{key}: {len(value)} / visibles: {len([i for i in value if i._hidden == False])}")
                y += self.text_spacing
            y += self.text_spacing
            for key, value in sprite_groups.__dict__.items():
                if type(value) == PanZoomLayeredUpdates:
                    self.draw_text(self.world_x + self.text_spacing, y, 200, 20,
                        f"{key}: {len(value)} / visibles: {len([i for i in value if i._hidden == False])}")
                    y += self.text_spacing
