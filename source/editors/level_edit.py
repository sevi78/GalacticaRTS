import math
import random
import pygame

from source.draw.zoomable_rect import draw_zoomable_rect
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.factories.planet_factory import planet_factory
from source.factories.solar_system_factory import SolarSystemFactory
from source.gui.event_text import event_text
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.selector import Selector
from source.level.level_factory import level_factory
from source.multimedia_library.screenshot import capture_screenshot
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.universe.universe_background import universe_factory
from source.utils import global_params
from source.multimedia_library.images import get_image
from source.utils.colors import colors

PLANET_MAX_SIZE = 200.0
PLANET_MIN_SIZE = 10.0


class LevelEditBuilder:
    def create_randomize_button(self):
        button_size = 32
        randomize_button = ImageButton(win=self.win,
            x=self.get_screen_x() + button_size / 2,
            y=self.world_y + TOP_SPACING + button_size / 2,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("randomize_icon.png"), (button_size, button_size)),
            tooltip="randomize level",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=self.layer,
            onClick=lambda: self.randomize_level(),
            )

        randomize_button.hide()

        self.buttons.append(randomize_button)
        self.widgets.append(randomize_button)

    def create_update_button(self):
        button_size = 32
        update_button = ImageButton(win=self.win,
            x=self.get_screen_x() + button_size * 2,
            y=self.world_y + TOP_SPACING + button_size / 2,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("update_icon.png"), (button_size, button_size)),
            tooltip="refresh level",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=self.layer,
            onClick=lambda: self.refresh_level(),
            )

        update_button.hide()

        self.buttons.append(update_button)
        self.widgets.append(update_button)

    def create_inputboxes(self):
        """"""
        self.inputbox = InputBox(self.win, self.world_x - self.spacing_x / 2 + self.world_width / 2, self.world_y + TOP_SPACING, self.spacing_x * 2, 32,
            text="Exoprime", parent=self, key="name")
        self.widgets.append(self.inputbox)

    def create_selectors(self):
        """"""
        x = self.world_x + self.world_width / 2 - ARROW_SIZE / 2
        y = 140

        for i in self.lists:
            setattr(self, "selector_" + i.split("_list")[0],
                Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
                    {"list_name": i, "list": getattr(self, i)}, self, FONT_SIZE))

            y += self.spacing_y
            self.max_height = y


class LevelEdit(EditorBase, LevelEditBuilder):
    """Main functionalities:
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.create_inputboxes()
        self.inputbox.disable()

        # lists
        self.level_list = [_ for _ in range(10)]
        self.planets_list = [_ for _ in range(10)]
        self.suns_list = [_ for _ in range(5)]
        self.moons_list = [_ for _ in range(10)]
        self.width_list = [_ for _ in range(5000, 25000, 1000)]
        self.height_list = [_ for _ in range(5000, 25000, 1000)]
        self.collectable_item_amount_list = [_ for _ in range(0, 50, 1)]
        self.universe_density_list = [_ for _ in range(0, 100, 10)]
        self.lists = ["level_list", "planets_list", "suns_list", "moons_list", "width_list", "height_list",
                      "collectable_item_amount_list", "universe_density_list"]

        # current values
        self._level = 0
        self.level = 0
        self.planets = 3
        self.suns = 1
        self.moons = 1
        self.width = global_params.scene_width
        self.height = global_params.scene_height
        self.universe_density = 25.0
        self.ships = []
        self.collectable_item_amount = 20

        # create widgets
        self.create_selectors()
        self.create_save_button(lambda: self.save_level(), "save level")
        self.create_load_button(lambda: self.load_level(self.level), "load level")
        self.create_close_button()
        self.create_randomize_button()
        self.create_update_button()

        # set default values
        self.data = None
        self.default_data = None
        self.load_level(self.level)
        self.set_selector_current_value()

        # hide initially
        self.hide()

        self.solar_system_factory = SolarSystemFactory(
            self.width, self.height, self.universe_density, self.collectable_item_amount, self.suns, self.planets, self.moons)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    def load_level(self, level):
        self.data = level_factory.load_level(level)
        if not self.data:
            self.data = level_factory.load_level(0)

        self.set_selector_current_value()
        planet_factory.delete_planets()
        # planet_factory.create_planets_from_json(self.level)

        planet_factory.create_planets_from_data(self.data)
        self.set_data_to_editor()
        self.create_universe()

    def save_level(self):
        level_factory.save_level(self.level, self.data)

        # save screenshot
        screen_x, screen_y = pan_zoom_handler.world_2_screen(0, 0)
        capture_screenshot(
            self.win,
            f"level_{self.level}.png",
            (screen_x, screen_y, self.width * pan_zoom_handler.zoom, self.height * pan_zoom_handler.zoom),
            (360, 360),
            event_text=event_text)

    def set_data_to_editor(self):
        self.planets = len(self.data["celestial_objects"].keys())
        self.moons = len([(key, value) for key, value in self.data["celestial_objects"].items() if
                          value["type"] == "moon"])
        self.suns = len([(key, value) for key, value in self.data["celestial_objects"].items() if
                         value["type"] == "sun"])

        for key, value in self.data["globals"].items():
            setattr(self, key, value)

        self.inputbox.set_text(f"Level {self.level}")

    def set_selector_current_value(self):
        """updates the selectors values"""
        for i in self.selectors:
            i.set_current_value(getattr(self, i.key))

    def get_input_box_values(self, obj, key, value):
        pass

    def selector_callback(self, key, value):
        """this is the selector_callback function called from the selector to return the values to the editor"""
        setattr(self, key, value)
        if key in self.data["globals"].keys():
            self.data["globals"][key] = value

    def randomize_level(self):
        ignorables = ["level"]
        for selector in self.selectors:
            if not selector.key in ignorables:
                selector.current_value = random.choice(selector.list)
                self.selector_callback(selector.key, selector.current_value)
        self.refresh_level()

    def refresh_level(self):
        # delet objects
        planet_factory.delete_planets()
        for i in sprite_groups.collectable_items.sprites():
            i.end_object()

        # recreate objects
        self.solar_system_factory = SolarSystemFactory(
            self.width, self.height, self.universe_density, self.collectable_item_amount, self.suns, self.planets, self.moons)
        self.data = self.solar_system_factory.randomize_data()
        planet_factory.create_planets_from_data(data=self.data, explored=True)
        self.create_universe()

    def create_universe(self):
        universe_factory.delete_universe()
        universe_factory.delete_artefacts()
        universe_factory.amount = int(math.sqrt(math.sqrt(self.width)) * self.data["globals"]["universe_density"])
        universe_factory.create_universe(0, 0, self.width, self.height)
        universe_factory.create_artefacts(0, 0, self.width, self.height,
            self.data["globals"]["collectable_item_amount"])

    def listen(self, events):
        """show or hide, navigate to planet on selection"""
        self.inputbox.handle_events(events)

        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return

    def draw(self):
        """"""
        if not self._hidden or self._disabled:
            self.draw_frame()
            self.inputbox.update()
            draw_zoomable_rect(self.win, colors.ui_darker, 0, 0, self.width, self.height, border_radius=int(pan_zoom_handler.zoom * 250))
