from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING, BUTTON_SIZE
from source.factories.universe_factory import universe_factory
from source.gui.lod import level_of_detail
from source.gui.widgets.Icon import Icon
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.checkbox import Checkbox
from source.handlers.file_handler import abs_database_path, soundpath
from source.handlers.file_handler import pictures_path, gifs_path
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups, PanZoomLayeredUpdates
from source.handlers.widget_handler import WidgetHandler
from source.universe.celestial_objects.celestial_object import CelestialObject
from source.universe.celestial_objects.celestial_object_static import CelestialObjectStatic

FONT_SIZE = 16


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
        self.layer_debug = False

        #  widgets
        self.widgets = []
        self.layer_checkboxes = []
        self.max_height = height

        # create widgets
        self.create_checkboxes()
        self.create_layer_checkboxes()
        self.create_close_button()
        self.create_save_button(lambda: print("no function"), "save , not working yet", name="save_icon")

        # hide initially
        self.hide()

    def create_checkboxes(self):
        x = self.world_width / 2 + BUTTON_SIZE * 2
        y = self.world_y + TOP_SPACING + self.text_spacing

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
                key="ships", image_name="spaceship.png", tooltip="debug spaceships", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
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

        checkbox_collectable_items = Checkbox(
                self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key="collectable_items", image_name="meteor_60x83.png", tooltip="debug collectable items", onClick=lambda: print("OKOKOK"), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(checkbox_collectable_items)
        self.widgets.append(checkbox_collectable_items)

        debug_checkbox = Checkbox(
                self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
                color=self.frame_color,
                key="debug_icon", tooltip="debug", onClick=lambda: print("debug: ",
                        config.debug), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(debug_checkbox)
        self.widgets.append(debug_checkbox)

        layer_checkbox = Checkbox(
                self.win, self.world_x - self.spacing_x + x + BUTTON_SIZE * 3, y, 30, 30, isSubWidget=False,
                color=self.frame_color, image_name="layer_icon.png",
                key="layer", tooltip="layers", onClick=lambda: print("layer: "), layer=9, parent=self)
        x += BUTTON_SIZE * 1.5
        self.checkboxes.append(layer_checkbox)
        self.widgets.append(layer_checkbox)

        for i in self.checkboxes:
            i.checked = False

    def create_layer_checkboxes(self):
        button_size = 20
        x = self.world_width / 2 + BUTTON_SIZE * 2
        y = self.world_y + TOP_SPACING + button_size * 1.6 + self.text_spacing

        for i in range(len(WidgetHandler.layer_switch.keys())):
            checkbox = Checkbox(
                    self.win,
                    self.world_x - self.spacing_x + x + BUTTON_SIZE * 3,
                    y,
                    button_size,
                    button_size,
                    isSubWidget=False,
                    color=self.frame_color,
                    key=f"layers:{i}",
                    image_name="layer_icon.png",
                    tooltip=f"show layer:{i}",
                    onClick=lambda: print("not working"),
                    layer=10,
                    parent=self,
                    button_size=button_size
                    )

            x += button_size * 1.625
            self.checkboxes.append(checkbox)
            self.layer_checkboxes.append((checkbox))
            self.widgets.append(checkbox)

    def set_debug_to_objects(self, key):
        if key in sprite_groups.__dict__:
            for obj in getattr(sprite_groups, key).sprites():
                obj.debug = getattr(self, key + "_debug")

        # if key == "quadrants":
        #     for k, v in level.quadrants.items():
        #         v.debug = getattr(self, key + "_debug")

    def get_checkbox_values(self, **kwargs) -> None:
        checkbox = kwargs.get("checkbox", None)
        value = kwargs.get("value", None)
        """gets the values from the checkboxes and calls update_planet_resources()"""
        self.checkbox_values = [i.key for i in self.checkboxes if i.checked]
        for i in self.checkboxes:
            if hasattr(self, i.key + "_debug"):
                setattr(self, i.key + "_debug", i.checked)
                self.set_debug_to_objects(i.key)

            if i.key == "debug_icon":
                config.debug = i.checked
                level_of_detail.debug = i.checked

            if i.key.startswith("layers"):
                # i.kex = layers:0  ect...
                # layer_switch = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
                layer_str = i.key.split(":")[1]
                WidgetHandler.layer_switch[layer_str] = int(i.checked)

    def update_checkbox_values(self):
        for i in self.layer_checkboxes:
            i.checked = WidgetHandler.layer_switch[str(self.layer_checkboxes.index(i))]

    def draw_texts(self, all_widgets, y):
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"pan_zoom.zoom: {pan_zoom_handler.zoom}")
        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"pan_zoom.world_offset_x: {pan_zoom_handler.world_offset_x}")
        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"pan_zoom.world_offset_y: {pan_zoom_handler.world_offset_y}")
        y += self.text_spacing * 2

        if self.layer_debug:
            celestials = [i for i in all_widgets if issubclass(i.__class__, (CelestialObject, CelestialObjectStatic))]

            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE, f"celestials: {len(celestials)}")
            y += self.text_spacing
            # self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
            #     f"quadrants: {len(level.quadrants)}")
            # y += self.text_spacing

            for key, value in universe_factory.celestial_objects.items():
                self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                        f"{key}: {len(value)} / visibles: {len([i for i in value if i._hidden == False])}")
                y += self.text_spacing

            y += self.text_spacing
            for key, value in sprite_groups.__dict__.items():
                if type(value) == PanZoomLayeredUpdates:
                    self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                            f"{key}: {len(value)} / visibles: {len([i for i in value if i._hidden == False])}")
                    y += self.text_spacing

            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                    f"WidgetHandler.widgets: {len(WidgetHandler.get_all_widgets())}")
            y += self.text_spacing
            building_button_widgets = [i for i in WidgetHandler.get_all_widgets() if i.name == "building button widget"]
            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                    f"WidgetHandler.building_button_widgets: {len(building_button_widgets)}")
            y += self.text_spacing
            image_button_widgets = [i for i in WidgetHandler.get_all_widgets() if isinstance(i, ImageButton)]
            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                    f"WidgetHandler.image_button_widgets: {len(image_button_widgets)}")
            y += self.text_spacing
            icons = [i for i in WidgetHandler.get_all_widgets() if isinstance(i, Icon)]
            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                    f"WidgetHandler.icons: {len(icons)}")
            y += self.text_spacing
            buttons = [i for i in WidgetHandler.get_all_widgets() if isinstance(i, Button)]
            self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                    f"WidgetHandler.buttons: {len(buttons)}")

        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"pictures_path: {pictures_path}")
        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"gifs_path: {gifs_path}")
        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"database_path: {abs_database_path()}")
        y += self.text_spacing
        self.draw_text(self.world_x + self.text_spacing, y, 200, FONT_SIZE,
                f"sound_path: {soundpath}")
        y += self.text_spacing
        return y

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.update_checkbox_values()
            self.draw_frame()
            y = self.world_y + TOP_SPACING + self.text_spacing
            self.draw_text(self.world_x + self.text_spacing, y, 200, 30, "Debug:")
            all_widgets = WidgetHandler.get_all_widgets()

            y += self.text_spacing * 2
            if not config.debug:
                y = self.draw_texts(all_widgets, y)

            self.max_height = y + self.text_spacing

            save_icon = [i for i in self.widgets if i.name == "save_icon"][0]
            save_icon.screen_y = self.max_height
