import time
import traceback

import pygame

from source.app.app_helper import AppHelper, select_next_item_in_list
from source.app.ui_builder import UIBuilder
from source.configuration.game_config import config
from source.draw.cursor import Cursor
from source.economy.economy_handler import economy_handler
from source.factories.ship_factory import ShipFactory
from source.game_play.cheat import Cheat
from source.game_play.enemy_handler import enemy_handler
from source.game_play.game_logic import GameLogic
from source.game_play.navigation import navigate_to, navigate_to_game_object_by_index
from source.gui.container.container_widget import ContainerWidget
from source.gui.container.filter_widget import FilterWidget
from source.gui.event_text import event_text
from source.gui.panels.map_panel import MapPanel
from source.gui.widgets.image_widget import ImageSprite
from source.gui.widgets.zoom_scale import ZoomScale
from source.handlers import event_text_handler
from source.handlers.file_handler import load_file
from source.handlers.game_event_handler import GameEventHandler
from source.handlers.mouse_handler import mouse_handler
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.score_plotter_handler import score_plotter_handler
from source.handlers.time_handler import time_handler
from source.handlers.ui_handler import ui_handler
from source.interaction.box_selection import BoxSelection
from source.level.level_edit import LevelEdit
from source.level.level_handler import LevelHandler
from source.level.level_select import LevelSelect
from source.multimedia_library.images import get_image
from source.player.player_edit import PlayerEdit
from source.trading.market import market

ECONOMY_UPDATE_INTERVAL = 2.0


class App(AppHelper, UIBuilder, GameLogic, Cheat):
    """Main functionalities:
    The App class is the main class of the application. It inherits from AppHelper, UIBuilder, and GameLogic classes,
    and is responsible for managing the game loop, updating game elements, and handling user input.
    It also creates and manages the user interface, including buttons, panels, and menus, and sets the game speed.

    Methods:
    - update(events): updates all game elements except pygame_widgets and calls functions that need events.
      It also sets the fps, updates necessary functions, updates objects, displays event text, cheats,
      sets global population, and saves planet positions.
    - loop(): the game loop that blits the background, fog of war, and calls self.update, updates pygame_widgets and
      pygame.display.
    - __init__(self, width, height): initializes the App class and sets the app icon and game speed.

    Fields:
    - game_speed: the speed of the game.
    - events: the events that occur in the game loop."""

    __slots__ = ('event_text_font_size', 'pan_enabled', 'start_time', 'wait', 'game_speed', 'run')

    __slots__ += (
        'population_limit', 'ctrl_pressed', 's_pressed', 'l_pressed', 'singleton_buildings_images',
        'singleton_buildings',
        'resources', 'water_buildings', 'energy_buildings', 'food_buildings', 'mineral_buildings',
        'technology_buildings',
        'population_buildings', 'population_buildings', 'buildings', 'buildings_list', 'production', 'production_water',
        'production_energy', 'production_food', 'production_minerals', 'production_population', 'production_technology',
        'prices',
        'game_objects', 'planets', 'collectables', 'ufos', 'building_widget_list', 'planet_buttons', 'ships', 'editors',
        'missiles', 'gif_handlers', 'build_menu_visible', 'build_menu_widgets', 'build_menu_widgets_buildings',
        'config',
        'frame_color', 'ui_helper', 'level', 'universe', '_ship', 'pan_zoom_handler', 'planet_edit', 'font_edit',
        'enemy_handler_edit', 'ship_edit', 'win', 'box_selection', 'world_width', 'height', 'icons',
        'explored_planets', 'event_text', 'event_display_text', 'player', 'building_panel', 'game_time',
        'settings_panel', 'advanced_settings_panel', 'tooltip_instance', 'info_panel', 'resource_panel', 'build_menu',
        'event_panel', 'border', 'word_height_sum', 'text_surfaces')  # 'selected_planet',

    def __init__(self, width, height):
        # make self global, maybe we need that
        self.map_panel = None
        config.app = self

        self.ship_factory = ShipFactory()
        AppHelper.__init__(self)
        UIBuilder.__init__(self, width, height)

        self.pan_enabled = False

        # set app-icon
        pygame.display.set_icon(get_image("Zeta Bentauri_60x60.png"))
        self.start_time = time.time()
        self.wait = ECONOMY_UPDATE_INTERVAL

        self.game_speed = 0
        self.run = 1

        self._selected_planet = None
        self.select_image = ImageSprite(self.win, 0, 0, 25, 25, get_image("check.png"), parent=self, hidden=True)
        self.sprite_groups = sprite_groups

    @property
    def selected_planet(self):
        return self._selected_planet

    @selected_planet.setter
    def selected_planet(self, value):
        self._selected_planet = value
        if value:
            self.update_building_button_widgets()

    def set_selected_planet(self, planet):
        """ planet must be a PanZoomPlanet"""
        if planet:
            self.select_image.show()
            self.selected_planet = planet
            self.selected_planet.set_info_text()
            self.info_panel.set_text(planet.info_text)

        self.building_panel.reposition()
        self.info_panel.reposition()

    def set_planet_selection(self, value):
        try:
            # if empty list: do nothing
            my_list = self.explored_planets
            if config.show_human_player_only:
                my_list = [i for i in self.explored_planets if i.owner == 0]
            if not my_list:
                return

            if sprite_groups.planets:
                if self.selected_planet:
                    current_item = self.selected_planet
                else:
                    current_item = sprite_groups.planets.sprites()[0]

                next = select_next_item_in_list(my_list, current_item, value)

                # set new selected planet
                # pan_zoom_handler.zoom = 1.8
                self.set_selected_planet(next)
                navigate_to(self.selected_planet)

        except Exception as e:
            print("building_panel.set_planet_selection: An error occurred:", e)
            traceback.print_exc()

    def update_building_button_widgets(self):
        for building_button_widget in self.building_button_widgets:
            building_button_widget.show()

    def update_economy(self):
        if config.game_paused:
            return

        if time.time() > self.start_time + self.wait:
            self.start_time = time.time()

            economy_handler.update()
            market.update()
            score_plotter_handler.update()

    def update(self, events):
        """
        updates all game Elements except pygame_widgets and calls functions that need events
        :param events:
        :return:
        """
        # update select image
        if self.selected_planet:
            self.select_image.set_position(self.selected_planet.rect.centerx, self.selected_planet.rect.centery, "center")
            # self.select_image.show()
            self.select_image.draw()

        # update game_events
        self.game_event_handler.update()

        # update economy
        self.update_economy()

        # game pause
        for event in events:
            # ignore all inputs while any text input is active
            if config.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause_game()

        # set fps
        pygame.display.set_caption("GalacticaRTS" + "   " + str(f"FPS: {time_handler.fps}"))

        # necessary functions, maybe could put these outside somehow
        self.quit_game(events)
        self.ui_helper.update()

        # update player
        for key, value in self.players.items():
            value.update()

        # cheat
        self.cheat(events)

        # update event_text
        event_text.update()
        event_text_handler.listen(event_text, events)

        # pathfinding
        # pathfinding_manager.draw_path()

    def loop(self):
        """
        the game loop: blits the background,fog of war.
        calls self.update,  updates pygame_widgets and pygame.display
        :return:
        """
        # game loop
        while self.run == 1:
            # fill background
            self.win.fill((0, 0, 15))

            # set fps
            time_handler.set_fps(int(config.fps))

            # get events
            events = pygame.event.get()

            # update mouse handler
            mouse_handler.handle_mouse_inputs(events)

            # update pan_zoom_handler
            if config.enable_zoom:
                if not config.text_input_active:
                    if config.enable_pan:
                        if config.copy_object:
                            self.pan_enabled = False
                        else:
                            self.pan_enabled = True

                    pan_zoom_handler.listen(events)

            # update sprites
            # dont mess up the order! for some reason it must be drawn first then update

            sprite_groups.update(events=events)
            sprite_groups.listen(events)
            sprite_groups.draw(self.win, events=events)

            # update box selection, might be mived to self.update
            self.box_selection.listen(events)

            # update app
            self.update(events)

            # handle screensize using [>]
            self.set_screen_size((config.width_minimized, config.height_minimized), events)

            # update enemy handler
            enemy_handler.update()

            # pygame update
            # pygame.display.update()
            pygame.display.flip()

            # testing
            # pprint(f"find_unused_images_gifs: {find_unused_images_gifs(os.path.join(pictures_path), os.path.join(pictures_path + 'gifs'), images, gifs)}")
            # print(f"get_image.cache_info(): {get_image.cache_info()}")
            # print(f"sounds.get_sound.cache_info(): {sounds.get_sound.cache_info()}")


def main():
    EDITOR_WIDTH = 700
    EDITOR_HEIGHT = 600

    # initialize pygame
    pygame.init()

    # initialize app
    app = App(config.width, config.height)

    # initialize box_selection
    app.box_selection = BoxSelection(app.win, sprite_groups.ships.sprites() + sprite_groups.planets.sprites())

    # initialize editors
    app.level_handler = LevelHandler(app)
    app.level_select = LevelSelect(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().centerx - EDITOR_WIDTH / 2,
            pygame.display.get_surface().get_rect().y,
            EDITOR_WIDTH, EDITOR_WIDTH, parent=app, obj=None)

    level_edit_width = EDITOR_WIDTH / 1.6

    app.level_edit = LevelEdit(pygame.display.get_surface(),
            pygame.display.get_surface().get_rect().right - level_edit_width,
            pygame.display.get_surface().get_rect().y,
            level_edit_width, EDITOR_HEIGHT, parent=app, ignore_other_editors=True)

    app.game_event_handler = GameEventHandler(data=load_file("game_event_handler.json", "config"), app=app)

    # load first level
    app.level_handler.load_level(f"level_{config.level}.json", "levels")

    # update level_successes
    app.level_handler.update_level_successes()

    # create map
    width, height = app.info_panel.world_width, app.info_panel.world_width
    app.map_panel = MapPanel(app.win, app.info_panel.world_x, app.win.get_size()[1] - width, width, height)

    # containers:
    container_width = 300
    container_height = 150

    # ship container
    app.ship_container = ContainerWidget(
            app.win,
            app.advanced_settings_panel.screen_x,
            60,
            container_width,
            container_height,
            market.convert_sprite_groups_to_container_widget_items_list("ships"),
            function=navigate_to_game_object_by_index,
            layer=9,
            list_name="ships",
            name="ships_container",

            filter_widget=FilterWidget(
                    app.win,
                    260,
                    60,
                    container_width,
                    150,
                    ["energy", "speed", "experience", "owner", "name", "state"],
                    parent=app,
                    layer=10,
                    list_name="ships",
                    name="ships_container_filter",
                    ignore_other_editors=True
                    )
            )

    # planet container
    app.planet_container = ContainerWidget(
            app.win,
            app.advanced_settings_panel.screen_x + 320,
            60,
            container_width * 2,
            container_height,
            market.convert_sprite_groups_to_container_widget_items_list("planets"),
            function=navigate_to_game_object_by_index,
            layer=9,
            list_name="planets",
            name="planets_container",
            filter_widget=FilterWidget(
                    app.win,
                    260,
                    60,
                    container_width,
                    150,
                    ["population", "population_limit", "buildings", "explored", "owner", "name"],
                    parent=app,
                    layer=10,
                    list_name="planets",
                    name="planets_container_filter",
                    ignore_other_editors=True
                    ))

    # player edit
    width = 1200
    app.player_edit = PlayerEdit(pygame.display.get_surface(),
            int(pygame.display.get_surface().get_width() / 2 - width / 2),
            pygame.display.get_surface().get_rect().y,
            width, height, parent=app, obj=None, layer=9, ignore_other_editors=True, drag_enabled=False, save=False)  # , game_paused=True)

    # deal container
    app.deal_container = ContainerWidget(
            app.win,
            600,
            60,
            600,
            container_height,
            [],
            function=navigate_to_game_object_by_index,
            layer=9,
            list_name="deals",
            name="deal_container",

            filter_widget=FilterWidget(
                    app.win,
                    260,
                    60,
                    container_width,
                    150,
                    ["water", "energy", "food", "minerals", "technology", "owner_index"],
                    parent=app,
                    layer=10,
                    list_name="deals",
                    name="deals_container_filter",
                    ignore_other_editors=True
                    )
            )
    # cursor object
    app.cursor = Cursor()

    # zoom scale
    app.zoom_scale = ZoomScale(app.win, 250, app.win.get_size()[1] - 10, 180, 5, anchor_left=app.map_panel)

    # restore ui elements
    ui_handler.restore_ui_elements()

    # start game loop
    app.loop()


if __name__ == "__main__":
    main()
