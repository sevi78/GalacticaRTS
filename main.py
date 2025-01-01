import time
import traceback

import pygame

from source.app.app_helper import AppHelper, select_next_item_in_list
from source.app.ui_builder import UIBuilder
from source.configuration.game_config import config
from source.draw.cursor import Cursor
from source.economy.economy_handler import economy_handler
from source.editors.chat_edit import ChatEdit
from source.editors.client_edit import ClientEdit
from source.editors.settings_edit import SettingsEdit
from source.factories.ship_factory import ShipFactory
from source.game_play.cheat import Cheat
from source.game_play.enemy_handler import enemy_handler
from source.game_play.game_logic import GameLogic
from source.game_play.navigation import navigate_to, navigate_to_game_object_by_index
from source.gui.container.container_widget import ContainerWidget
from source.gui.container.filter_widget import FilterWidget
from source.gui.event_text import event_text
from source.gui.lod import level_of_detail
from source.gui.panels.map_panel import MapPanel
from source.gui.widgets.image_widget import ImageSprite
from source.gui.widgets.zoom_scale import ZoomScale
from source.handlers import event_text_handler
from source.handlers.file_handler import load_file
from source.handlers.game_event_handler import GameEventHandler
from source.handlers.mouse_handler import mouse_handler
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.position_handler import prevent_object_overlap
from source.handlers.score_plotter_handler import score_plotter_handler
from source.handlers.screen_handler import screen_handler
from source.handlers.time_handler import time_handler
from source.handlers.ui_handler import ui_handler
from source.interaction.box_selection import BoxSelection
from source.level.level_edit import LevelEdit
from source.level.level_handler import LevelHandler
from source.level.level_select import LevelSelect
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_ship_test2.interaction_handler import interaction_handler2
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

        # self.game_speed = 0#load_file("settings.json", "config")["game_speed"]
        self.run = 1

        self._selected_planet = None
        self.select_image = ImageSprite(self.win, 0, 0, 25, 25, get_image("check.png"), parent=self, hidden=True, layer=4)
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

    def handle_keyboard_input(self, events):
        for event in events:
            # ignore all inputs while any text input is active
            if config.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                # game pause
                if event.key == pygame.K_SPACE:
                    self.pause_game()

                # switch screen tiling, for debug only
                if event.key == pygame.K_TAB:
                    screen_handler.set_screen_tiled(1920, 1080, 2, self.game_client.id, not screen_handler.alignment)
                    print("pressed: ", event.key)

                # toggle map panel
                if event.key == pygame.K_m:
                    config.show_map_panel = not config.show_map_panel

                # toggle ship container
                if event.key == pygame.K_s:
                    config.app.ship_container.set_visible()

                # toggle planet container
                if event.key == pygame.K_p:
                    config.app.planet_container.set_visible()

                # toggle info panel
                if event.key == pygame.K_i:
                    config.app.info_panel._hidden = not config.app.info_panel._hidden

                # toggle building panel
                if event.key == pygame.K_b:
                    config.app.building_panel.toggle_switch.toggle_panel()


                # test weapon build for ships
                if event.key == pygame.K_w:
                    for i in sprite_groups.ships.sprites():
                        if i.owner == 1:
                            player = config.app.players[i.owner]
                            player.auto_economy_handler.build_ship_weapons()






    def update(self, events):
        """
        updates all game Elements except pygame_widgets and calls functions that need events
        :param events:
        :return:
        """

        # update box selection, might be mived to self.update
        self.box_selection.listen(events)

        # update select image
        if self.selected_planet:
            self.select_image.set_position(self.selected_planet.rect.centerx, self.selected_planet.rect.centery, "center")

        # update game_events
        self.game_event_handler.update()

        # update economy
        self.update_economy()

        self.handle_keyboard_input(events)

        # set fps
        # pygame.display.set_caption(f"GalacticaRTS: FPS: {time_handler.fps}, client_id: {self.game_client.id}, host:{self.game_client.host}" )

        # necessary functions, maybe could put these outside somehow
        self.quit_game(events)

        # really update the ui_helper every frame ???
        self.ui_helper.update()

        # update player
        for key, value in self.players.items():
            value.update()

        # cheat
        self.cheat(events)

        # update event_text
        event_text.update()
        event_text_handler.listen(event_text, events)

        # update lod, only needed for debug, remove it later!!!
        level_of_detail.draw_debug_rect()
        # pathfinding
        # pathfinding_manager.draw_path()

    def loop(self):
        """
        the game loop: blits the background
        calls self.update,  updates pygame_widgets and pygame.display
        :return:
        """
        # game loop
        while self.run == 1:
            # fill background
            self.win.fill((0, 0, 15))

            # get events
            events = pygame.event.get()

            # set fps
            # time_handler.set_fps(int(config.fps))
            time_handler.set_fps(800)
            time_handler.update_time()
            time_handler.listen(events)

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
            # interaction_handler2.handle_mouse()

            sprite_groups.draw(self.win, events=events)

            # update app
            self.update(events)

            # receive data from server
            self.game_client.message_handler.handle_messages()

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

            prevent_object_overlap(sprite_groups.ships, 80)


def init():
    EDITOR_WIDTH = 700
    EDITOR_HEIGHT = 600

    # initialize pygame
    pygame.init()

    # initialize app
    app = App(config.width, config.height)

    # initialize editors
    app.level_handler = LevelHandler(app)
    app.level_select = LevelSelect(pygame.display.get_surface(),
            int(pygame.display.get_surface().get_rect().centerx - EDITOR_WIDTH / 2),
            pygame.display.get_surface().get_rect().y,
            EDITOR_WIDTH, EDITOR_WIDTH, parent=app, obj=None)

    level_edit_width = EDITOR_WIDTH / 1.6
    app.level_edit = LevelEdit(pygame.display.get_surface(),
            int(pygame.display.get_surface().get_rect().right - level_edit_width),
            pygame.display.get_surface().get_rect().y,
            int(level_edit_width), EDITOR_HEIGHT, parent=app, ignore_other_editors=True)

    EDITOR_HEIGHT = 600
    EDITOR_WIDTH = 700
    app.settings_edit = SettingsEdit(
            pygame.display.get_surface(),
            int(pygame.display.get_surface().get_rect().centerx - EDITOR_WIDTH / 2),
            pygame.display.get_surface().get_rect().y,
            int(EDITOR_WIDTH / 1.5),
            EDITOR_HEIGHT,
            parent=app,
            obj=None,
            layer=9)  # , game_paused=True)

    # initialize game_event_handler
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
            sprite_groups.convert_sprite_groups_to_container_widget_items_list("ships"),
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
            sprite_groups.convert_sprite_groups_to_container_widget_items_list("planets"),
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
    app.create_player_edit(2)

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
    # chat edit
    h_ = 150
    app.chat_edit = ChatEdit(
            app.win,
            config.app.map_panel.world_width,
            config.app.win.get_height() - h_,
            600,
            h_,
            parent=app,
            frame_corner_radius=0,
            frame_corner_thickness=0)
    app.chat_edit.set_visible()

    # client_edit
    app.client_edit = ClientEdit(
            app.win,
            0,
            0,
            1000,
            0,
            name="client_edit",
            parent=app,
            ignore_other_editors=True, drag_enabled=True, save=True
            )

    # cursor object
    app.cursor = Cursor()

    # zoom scale
    app.zoom_scale = ZoomScale(
            app.win,
            250,
            app.win.get_size()[1] - 10,
            180,
            5,
            anchor_left=app.map_panel)

    # restore ui elements
    ui_handler.restore_ui_elements()

    # scenario_1()

    # initialize box_selection
    app.box_selection = BoxSelection(app.win, sprite_groups.ships.sprites() + sprite_groups.planets.sprites())



    return app


def main():
    # initialise objects
    app = init()

    # start game loop
    app.loop()


if __name__ == "__main__":
    main()
