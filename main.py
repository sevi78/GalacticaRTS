import time

import pygame
# from pygame.locals import QUIT, KEYDOWN, KEYUP

from source.app.app_helper import AppHelper
from source.app.ui_builder import UIBuilder
from source.editors.ship_edit import ShipEdit

from source.game_play.cheat import Cheat
from source.game_play.enemy_handler import enemy_handler
from source.game_play.game_logic import GameLogic
from source.gui.building_button_widget import BuildingButtonWidget
from source.gui.widgets import widget_handler
from source.interaction import copy_agent
from source.interaction.box_selection import BoxSelection
# from source.level.level_factory import LevelFactory, Level
from source.universe.universe_background import Universe
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import text_input_active, enable_pan, copy_object

from source.multimedia_library.images import get_image
from source.utils.mouse import Mouse
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils.text_wrap import TextWrap
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups

pygame.init()

ECONOMY_UPDATE_INTERVAL = 2.0


class App(AppHelper, UIBuilder, GameLogic, Cheat, TextWrap):
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
        'city_buildings', 'population_buildings', 'buildings', 'buildings_list', 'production', 'production_water',
        'production_energy', 'production_food', 'production_minerals', 'production_city', 'production_technology',
        'prices',
        'game_objects', 'planets', 'collectables', 'ufos', 'building_widget_list', 'planet_buttons', 'ships', 'editors',
        'missiles', 'gif_handlers', 'build_menu_visible', 'build_menu_widgets', 'build_menu_widgets_buildings',
        'config',
        'frame_color', 'ui_helper', 'level', 'universe', '_ship', 'pan_zoom_handler', 'planet_edit', 'font_edit',
        'enemy_handler_edit', 'ship_edit', 'clock', 'win', 'box_selection', 'world_width', 'height', 'icons',
        'explored_planets', 'event_text', 'event_display_text', 'player', 'building_panel', 'game_time',
        'settings_panel', 'advanced_settings_panel', 'tooltip_instance', 'info_panel', 'resource_panel', 'build_menu',
        'event_panel', 'border', 'word_height_sum', 'text_surfaces')  # 'selected_planet',

    def __init__(self, width, height):
        AppHelper.__init__(self)
        UIBuilder.__init__(self, width, height)
        TextWrap.__init__(self)

        self.event_text_font_size = 25
        self.pan_enabled = False

        # set app-icon
        pygame.display.set_icon(get_image("Zeta Bentauri_60x60.png"))
        self.start_time = time.time()
        self.wait = ECONOMY_UPDATE_INTERVAL

        self.game_speed = 0
        self.run = 1

        # make self global, maybe we need that
        global_params.app = self

        temp = []
        for key, value in self.__dict__.items():
            if not key in self.__slots__:
                temp.append(key)

        print(f"pan_zoom_planet.__dict__: {self.__dict__} \n __slots__; {self.__slots__}\n tmp:{temp}")

    @property
    def selected_planet(self):
        return self._selected_planet

    @selected_planet.setter
    def selected_planet(self, value):
        self._selected_planet = value
        if value:
            self.update_building_button_widgets()

    def update_building_button_widgets(self):
        for building_button_widget in self.building_button_widgets:
            building_button_widget.show()
            # building_button_widget.hide_unused_resources()

    def update_economy(self):
        if global_params.game_paused:
            return

        if time.time() > self.start_time + self.wait:
            self.start_time = time.time()
            for i in sprite_groups.planets.sprites():
                i.calculate_production()
                i.add_population()
            self.calculate_global_production()

    def update(self, events):
        """
        updates all game Elements except pygame_widgets and calls functions that need events
        :param events:
        :return:
        """
        self.update_economy()

        self.events = events
        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return
            copy_agent.update(events)

            # only resize background on window resize
            if event.type == pygame.WINDOWRESIZED:
                pass
                # self.bg = pygame.transform.scale(self.bg, (self.win.get_width(), self.win.get_height()))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.build_menu_visible:
                        self.close_build_menu()
                    else:
                        self.open_build_menu()

                if event.key == pygame.K_SPACE:
                    self.pause_game()

                if event.key == pygame.K_r:
                    self.restart_game()

        # set fps
        pygame.display.set_caption(global_params.root + "   " + str(f"FPS: {self.clock.get_fps()}"))

        # necessary functions, maybe could put these outside somehow
        self.quit_game(events)
        self.ui_helper.update()
        self.player.update()

        # event text
        event_text_height = 25
        self.event_text_font = pygame.font.SysFont(global_params.font_name, self.event_text_font_size)
        prefix = "GPT-1357: "
        self.event_display_text = prefix + self.event_text

        if not global_params.edit_mode:
            # drawText(self.win, self.event_display_text, self.frame_color,
            #     (self.ui_helper.left, self.ui_helper.anchor_bottom - event_text_height , self.ui_helper.world_width,
            #      event_text_height), self.event_text_font, "center")

            self.wrap_text(self.event_display_text, (
                self.ui_helper.left, self.ui_helper.anchor_bottom - event_text_height),
                (self.ui_helper.world_width, event_text_height), self.event_text_font, colors.frame_color)

        # cheat
        self.cheat(events)

        # set global population
        self.player.population = int(sum([i.population for i in sprite_groups.planets]))

        # store planet positions
        self.save_load(events)
        # self.background.draw()

    def loop(self):
        """
        the game loop: blits the background,fog of war.
        calls self.update,  updates pygame_widgets and pygame.display
        :return:
        """
        # game loop
        while self.run == 1:
            self.win.fill((0, 0, 0))
            self.clock.tick(int(global_params.fps))
            # settings
            events = pygame.event.get()
            Mouse.updateMouseState()

            # draw background, fog of war
            if hasattr(self, "background_image"):
                pass
                # self.background_image.draw()

            # update pan_zoom_handler
            if global_params.enable_zoom:
                if not text_input_active:
                    if enable_pan:
                        if copy_object:
                            self.pan_enabled = False
                        else:
                            self.pan_enabled = True

                    pan_zoom_handler.listen(events, self.pan_enabled)
                    # self.pan_zoom_handler.listen(events, self.pan_enabled)

                # if pan_zoom_handler.panning:
                #     if self.selected_planet:
                #         self.selected_planet.reset_building_buttons_visible_state()

            # update sprites
            # dont mess up the order! for some reason it must be drawn first then update

            sprite_groups.update()
            sprite_groups.listen(events)
            sprite_groups.draw(self.win)

            # update pygame_widgets
            widget_handler.update(events)

            # update box selection, might be mived to self.update
            self.box_selection.listen(events)

            # update app
            self.update(events)

            # handle screensize using [>]
            self.set_screen_size((global_params.WIDTH_MINIMIZED, global_params.HEIGHT_MINIMIZED), events)

            enemy_handler.update()

            # pygame update
            pygame.display.update()


if __name__ == "__main__":
    app = App(global_params.WIDTH, global_params.HEIGHT)
    app.box_selection = BoxSelection(app.win, sprite_groups.ships.sprites() + sprite_groups.planets.sprites())
    win = app.win
    # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    width = 800
    height = 600
    # app.ship_edit = ShipEdit(pygame.display.get_surface(),
    #     pygame.display.get_surface().get_rect().centerx - width / 2,
    #     pygame.display.get_surface().get_rect().y,
    #     width, height, parent=app, obj=app.ship, layer=9)
    # blabla
    # building_button_widget = BuildingButtonWidget(win, 200, 100, 300, 200, app, False, layer= 4, parent= sprite_groups.planets.sprites()[0])
    app.loop()
