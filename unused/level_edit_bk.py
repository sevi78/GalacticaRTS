import math
import random
import pygame

from source.draw.circles import draw_zoomable_circle
from source.draw.zoomable_rect import draw_zoomable_rect
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.factories.planet_factory import planet_factory
from source.factories.solar_system_factory import SolarSystemFactory
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.selector import Selector
from source.handlers import level_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.factories.universe_factory import universe_factory
from source.configuration import global_params
from source.multimedia_library.images import get_image
from source.handlers.color_handler import colors

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
                    {"list_name": i, "list": getattr(self, i)}, self, FONT_SIZE, repeat_clicks=True))

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
        self.central_compression_list = [_ for _ in range(100)]
        self.level_list = [_ for _ in range(12)]
        self.planets_list = [_ for _ in range(1, 25)]
        self.suns_list = [_ for _ in range(1, 35)]
        self.moons_list = [_ for _ in range(1, 50)]
        self.width_list = [_ for _ in range(5000, 1000000, 1000)]
        self.height_list = [_ for _ in range(5000, 1000000, 1000)]
        self.collectable_item_amount_list = [_ for _ in range(0, 50, 1)]
        self.universe_density_list = [_ for _ in range(0, 110, 10)]
        self.lists = ["level_list", "planets_list", "suns_list", "moons_list", "width_list", "height_list",
                      "collectable_item_amount_list", "universe_density_list", "central_compression_list"]

        # current values
        self.central_compression = 1
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

        # set default values
        self.data = global_params.app.level_handler.data
        self.default_data = None

        # create widgets
        self.create_selectors()
        self.create_save_button(lambda: global_params.app.level_handler.save_level(f"level_{self.level}.json", "levels", self.data), "save level")
        #self.create_load_button(lambda: global_params.app.level_handler.load_level(self.level), "load level", data=self.data)
        self.create_load_button(lambda: global_params.app.level_handler.load_level(f"level_{self.level}.json", 'levels'), "load level")
        self.create_close_button()
        self.create_randomize_button()
        self.create_update_button()

        self.set_selector_current_value()

        # hide initially
        self.hide()

        #self.solar_system_factory = SolarSystemFactory(
        #self.width, self.height, self.universe_density, self.collectable_item_amount, self.suns, self.planets, self.moons)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        print(f"@level.setter: {self.level}")

    def set_data_to_editor(self, level):
        self.data = global_params.app.level_handler.data
        self.level = level
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

    def selector_callback(self, key, value):
        """this is the selector_callback function called from the selector to return the values to the editor"""
        setattr(self, key, value)
        if key in self.data["globals"].keys():
            self.data["globals"][key] = value

        if key == "central_compression":
            universe_factory.central_compression = value

        self.inputbox.set_text(f"Level {self.level}")

    def randomize_level(self):
        ignorables = ["level"]
        for selector in self.selectors:
            if not selector.key in ignorables:
                selector.current_value = random.choice(selector.list)
                self.selector_callback(selector.key, selector.current_value)
        self.refresh_level()

    def refresh_level(self):
        global_params.app.level_handler.delete_level()

        # recreate objects
        # self.solar_system_factory = SolarSystemFactory(
        #     self.width, self.height, self.universe_density, self.collectable_item_amount, self.suns, self.planets, self.moons)
        # self.data = self.solar_system_factory.randomize_data()
        planet_factory.create_planets_from_data(data=self.data)
        level_handler.create_universe()

    def delete_object(self):
        selected_ships = global_params.app.box_selection.selected_objects

        # used for ships
        if len(selected_ships) > 0:
            for i in selected_ships:
                i.__delete__(i)

        # used for planets
        selected_planet = global_params.app.selected_planet
        if selected_planet:
            sprite_groups.planets.remove(selected_planet)
            selected_planet.__delete__()
            selected_planet.kill()

            # delete gif handlers attached to planet
            for i in sprite_groups.gif_handlers.sprites():
                if i.parent == selected_planet:
                    i.end_object()


    def listen(self, events):
        """show or hide, navigate to planet on selection"""
        self.inputbox.handle_events(events)

        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.isVisible():
                        self.delete_object()

    def draw(self):
        """"""
        if not self._hidden or self._disabled:
            self.draw_frame()
            self.inputbox.update()
            draw_zoomable_rect(self.win, colors.ui_darker, 0, 0, self.width, self.height, border_radius=int(pan_zoom_handler.zoom * 250))
            draw_zoomable_circle(self.win, colors.ui_darker, 0 + self.width / 2, 0 + self.width / 2, self.width / 2)


