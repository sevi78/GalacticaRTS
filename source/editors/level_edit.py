import random

import pygame

from source.configuration.game_config import config
from source.draw.circles import draw_zoomable_circle
from source.draw.zoomable_rect import draw_zoomable_rect
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.factories.planet_factory import planet_factory
from source.factories.universe_factory import universe_factory
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.gui.widgets.selector import Selector
from source.handlers import position_handler
from source.handlers.color_handler import colors
from source.handlers.file_handler import get_ships_list
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image, get_image_names_from_folder
from source.text.info_panel_text_generator import info_panel_text_generator

PLANET_MAX_SIZE = 200.0
PLANET_MIN_SIZE = 10.0
BUTTON_SIZE = 25


class LevelEdit(EditorBase):
    """Main functionalities:
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.level_handler = config.app.level_handler

        #  widgets
        self.create_inputboxes()
        self.inputbox.disable()

        # lists
        self.central_compression_list = [_ for _ in range(101)]
        self.level_list = [_ for _ in range(12)]
        self.planets_list = [_ for _ in range(1, 51)]
        self.suns_list = [_ for _ in range(1, 31)]
        self.moons_list = [_ for _ in range(1, 151)]
        self.spaceship_list = [_ for _ in range(0, 11)]
        self.spacehunter_list = [_ for _ in range(0, 11)]
        self.cargoloader_list = [_ for _ in range(0, 11)]
        self.width_list = [_ for _ in range(5000, 1001000, 1000)]
        self.height_list = [_ for _ in range(5000, 1001000, 1000)]
        self.collectable_item_amount_list = [_ for _ in range(0, 101, 1)]
        self.universe_density_list = [_ for _ in range(0, 110, 10)]
        self.population_density_list = [_ for _ in range(0, 105, 5)]
        self.planet_orbit_speed_list = [_ for _ in range(10, 110, 10)]
        self.lists = ["level_list", "planets_list", "suns_list", "moons_list", "width_list", "height_list",
                      "collectable_item_amount_list", "universe_density_list", "central_compression_list",
                      "population_density_list", "planet_orbit_speed_list"]

        # temp dict
        self.last_created = {}

        # create widgets
        self.create_selectors()
        self.create_save_button(lambda: self.level_handler.save_level(f"level_{self.level_handler.data['globals']['level']}.json", "levels"), "save level")
        self.create_load_button(lambda: self.level_handler.load_level(f"level_{self.level_handler.data['globals']['level']}.json", 'levels'), "load level")
        self.create_close_button()
        self.create_randomize_button()
        self.create_smoothing_button()
        self.create_update_button()
        self.create_rename_button()
        self.create_owner_button()
        self.create_explore_button()

        self.set_selector_current_value()

        # hide initially
        self.hide()

    def create_randomize_button(self):
        randomize_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("randomize_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="randomize level",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
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
        update_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2 + BUTTON_SIZE,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("update_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="refresh level",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: self.refresh_level(),
                )

        update_button.hide()

        self.buttons.append(update_button)
        self.widgets.append(update_button)

    def create_owner_button(self):
        owner_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2 + BUTTON_SIZE * 2,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("owner.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="set owners",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: self.level_handler.set_planet_owners(),
                )

        owner_button.hide()

        self.buttons.append(owner_button)
        self.widgets.append(owner_button)

    def create_smoothing_button(self):
        smoothing_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2 + BUTTON_SIZE * 3,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("calculate.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="smooth planet positions",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: position_handler.smooth_planet_positions(
                        self.level_handler.data["globals"]["width"], self.level_handler.data["globals"]["height"]),
                )

        smoothing_button.hide()

        self.buttons.append(smoothing_button)
        self.widgets.append(smoothing_button)

    def create_rename_button(self):
        rename_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2 + BUTTON_SIZE * 4,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("rename_planets_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="rename planets",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: planet_factory.generate_planet_names())

        rename_button.hide()

        self.buttons.append(rename_button)
        self.widgets.append(rename_button)

    def create_explore_button(self):
        explore_button = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE / 2 + BUTTON_SIZE * 5,
                y=self.world_y + TOP_SPACING + BUTTON_SIZE / 2,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("explore_icon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="explore planets",
                info_text=info_panel_text_generator.create_create_info_panel_level_text(
                        self.level_handler.data["globals"]["level"], self.level_handler.data),
                frame_color=self.frame_color,
                moveable=False,
                include_text=False,
                layer=self.layer,
                onClick=lambda: planet_factory.explore_planets())

        explore_button.hide()

        self.buttons.append(explore_button)
        self.widgets.append(explore_button)

    def create_inputboxes(self):
        """"""
        self.inputbox = InputBox(self.win, self.world_x - self.spacing_x / 2 + self.world_width / 2, self.world_y + TOP_SPACING + 16, self.spacing_x * 2, 32,
                text="          Edit Level!", parent=self, key="name", draw_frame=False)
        self.widgets.append(self.inputbox)

    def create_selectors(self):
        # Desired order of keys
        desired_order = ["level", "level_success", "width", "height", "universe_density", "central_compression",
                         "goal", "suns", "planets", "moons", "collectable_item_amount", "spaceship", "spacehunter",
                         "cargoloader", "population_density", "planet_orbit_speed"]

        # for key, value in self.level_handler.data["globals"].items():
        #     if not key in desired_order:
        #         desired_order.append(key)

        # Create a new dictionary with the desired key order
        self.level_handler.data["globals"] = {key: self.level_handler.data["globals"][key] for key in desired_order}

        x = self.world_x + self.world_width / 2 - ARROW_SIZE / 2
        y = 140
        no_repeat_clicks = ["suns", "planets", "moons", "spaceship", "spacehunter", "cargoloader"]
        # create global selectors
        for key, value in self.level_handler.data["globals"].items():
            # print(f"key:{key}, value: {value}")
            repeat_clicks = key not in no_repeat_clicks
            if hasattr(self, key + "_list"):
                setattr(self, "selector_" + key.split("_list")[0],
                        Selector(self.win, x, self.world_y + y, ARROW_SIZE, self.frame_color, 9, self.spacing_x,
                                {"list_name": key, "list": getattr(self, key + "_list")}, self, FONT_SIZE, repeat_clicks=repeat_clicks, restrict_list_jump=not repeat_clicks))

                y += self.spacing_y

            else:
                print(f"cant create selector, no list availlable:{key}")

        # finally set the max height of the panel based on the selectors
        self.max_height = y

    def set_selector_current_value(self):
        """updates the selectors values"""
        for i in self.selectors:
            if i.key in self.level_handler.data["globals"]:
                i.set_current_value(self.level_handler.data["globals"][i.key])

            else:
                print(f"missing {i.key} in level_handler.data['globals'], (level_{self.level_handler.data['globals']['level']}, adding to data!)")
                self.level_handler.data["globals"][i.key] = i.current_value

    def selector_callback(self, key, value, selector):
        """this is the selector_callback function called from the selector to return the values to the editor"""

        if key in self.level_handler.data["globals"].keys():
            self.level_handler.data["globals"][key] = value
        else:
            print(f"selector_callback: cant find {key} in level_handler.data['globals']!")

        if key == "central_compression":
            universe_factory.central_compression = value

        if key == "planet_orbit_speed":
            for planet in sprite_groups.planets.sprites():
                planet.orbit_speed = planet.orbit_speed_raw / 100 * self.level_handler.data["globals"][key]

        # update scene: to make sure changes got displayed
        self.update_scene(key)

    def update_scene(self, key: str):
        # get selector value
        selector_value = self.level_handler.data["globals"][key]

        # add object to scene:
        self.update_ships(key, selector_value)
        self.update_planets(key, selector_value)

    def update_ships(self, key, selector_value):
        # check if key is a ship
        if not key in get_ships_list():
            return

        # get all ships with the given key
        ship_key_list = [_.id for _ in sprite_groups.ships.sprites() if _.name == key]

        # check if object needs to be added or deleted based on selector_value
        if selector_value > len(ship_key_list):
            add = True
        else:
            add = False

        # add ship
        if add:
            # get values for the constructor
            border = min(self.level_handler.data["globals"]["width"], self.level_handler.data["globals"]["height"]) / 4
            world_x = self.level_handler.level_dict_generator.get_random_position(
                    self.level_handler.data["globals"]["width"], border)
            world_y = self.level_handler.level_dict_generator.get_random_position(
                    self.level_handler.data["globals"]["height"], border)
            name = key
            data = self.level_handler.data_default
            weapons = {}

            # add ship to the scene
            ship = self.parent.ship_factory.create_ship(name, world_x, world_y, self.parent, weapons, data=data)
        else:
            # remove object from scene
            if len(sprite_groups.ships.sprites()) > 0:
                # get id of the last created ship
                last_ship_id = max([_.id for _ in sprite_groups.ships.sprites() if _.name == key])

                # get last created ship
                last_ship = [_ for _ in sprite_groups.ships.sprites() if _.name == key and _.id == last_ship_id][0]

                # finally delete the ship
                sprite_groups.ships.sprites()[
                    sprite_groups.ships.sprites().index(last_ship)].__delete__(sprite_groups.ships.sprites().index(last_ship))

    def update_planets(self, key, selector_value):
        # check if key is a planet:
        if not key in ["suns", "planets", "moons"]:
            return

        key_ = key[:-1]
        # get all planets with the given key
        planet_key_list = [_.id for _ in sprite_groups.planets.sprites() if _.type == key_]

        # check if object needs to be added or deleted based on selector_value
        if selector_value > len(planet_key_list):
            add = True
        else:
            add = False

        # add planet
        if add:
            # get values for the constructor
            border = min(self.level_handler.data["globals"]["width"], self.level_handler.data["globals"]["height"]) / 4
            world_x = self.level_handler.level_dict_generator.get_random_position(
                    self.level_handler.data["globals"]["width"], border)
            world_y = self.level_handler.level_dict_generator.get_random_position(
                    self.level_handler.data["globals"]["height"], border)
            id_ = len(sprite_groups.planets.sprites())

            if key_ == "sun":
                orbit_object_id = id_
                image_names = get_image_names_from_folder(key)

            elif key_ == "planet":
                orbit_object_id = random.choice([_.id for _ in sprite_groups.planets.sprites() if _.type == "sun"])
                image_names = get_image_names_from_folder(key)

            elif key_ == "moon":
                orbit_object_id = random.choice([_.id for _ in sprite_groups.planets.sprites() if _.type == "planet"])
                image_names = get_image_names_from_folder("gifs", startswith_string="moon")

            # generate data
            planet_data = self.level_handler.level_dict_generator.create_celestial_object(
                    id_, key_, image_names, orbit_object_id, world_x, world_y)
            data = {"celestial_objects": {str(id_): planet_data}}

            # add planet to the scene
            planet_factory.create_planets_from_data(data)
            planet = [_ for _ in sprite_groups.planets.sprites() if _.id == id_][0]

            planet.name = "not set"
        else:
            # remove object from scene
            if len(sprite_groups.planets.sprites()) > 0:
                # get id of the last created planet
                last_planet_id = max([_.id for _ in sprite_groups.planets.sprites() if _.type == key_])

                # get last created planet
                last_planet = [_ for _ in sprite_groups.planets.sprites() if _.type == key_ and _.id == last_planet_id][
                    0]

                # finally delete the planet
                planet_factory.delete_planet(last_planet)

    def randomize_level(self):
        ignorables = ["level"]
        for selector in self.selectors:
            if not selector.key in ignorables:
                selector.current_value = random.choice(selector.list)
                self.selector_callback(selector.key, selector.current_value, selector)
        self.refresh_level()

    def refresh_level(self):
        self.level_handler.delete_level()
        self.level_handler.generate_level_dict_from_editor()
        planet_factory.create_planets_from_data(data=self.level_handler.data)
        self.parent.selected_planet = sprite_groups.planets.sprites()[0]
        self.parent.ship_factory.create_ships_from_data(data=self.level_handler.data)
        self.level_handler.create_universe()

        # set info text
        for i in self.buttons:
            i.info_text = info_panel_text_generator.create_create_info_panel_level_text(
                    self.level_handler.data["globals"]["level"], self.level_handler.data)

        self.level_handler.setup_pan_zoom_handler()

    def delete_object(self):
        selected_ships = config.app.box_selection.selected_objects

        # used for ships
        if len(selected_ships) > 0:
            for i in selected_ships:
                i.__delete__(i)

        # used for planets
        selected_planet = config.app.selected_planet
        planet_factory.delete_planet(selected_planet)

    def listen(self, events):
        """show or hide, navigate to planet on selection"""
        if not self._hidden and not self._disabled:
            self.inputbox.handle_events(events)
            self.handle_hovering()
            self.drag(events)

            for event in events:
                # ignore all inputs while any text input is active
                if config.text_input_active:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.isVisible():
                            self.delete_object()

    def draw_level_borders(self):
        draw_zoomable_rect(self.win, colors.ui_darker, 0, 0,
                self.level_handler.data["globals"]["width"],
                self.level_handler.data["globals"]["height"], border_radius=int(pan_zoom_handler.zoom * 250))
        draw_zoomable_circle(self.win, colors.ui_darker, 0 + self.level_handler.data["globals"]["width"] / 2, 0 +
                                                         self.level_handler.data["globals"]["width"] / 2,
                                                         self.level_handler.data["globals"]["width"] / 2)

    def draw(self):
        """"""
        if not self._hidden or self._disabled:
            self.inputbox.update()
            self.draw_level_borders()
            self.draw_frame()
