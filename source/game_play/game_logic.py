import os
import sys

import pygame

from source.configuration import config
from source.gui.widgets.building_widget import BuildingWidget
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.database.saveload import write_file
from source.multimedia_library.sounds import sounds


class GameLogic:
    """Main functionalities:
    The GameLogic class is responsible for the game logic of the application.
    It contains methods for building buildings on planets, paying for those buildings, adding objects to the game,
    and pausing the game. It also has access to the selected planet and player information.

    Methods:
    - build(building): builds a building on the selected planet if certain conditions are met, such as
      minimum population and available building slots. It also pays for the building and creates a building widget to
      track progress.
    - build_payment(building): pays for a building if it is being built.
    - add_object(): adds objects to the game, such as celestial objects.
    - pause_game(): pauses or continues the game depending on its current state.

Fields:
- None."""

    def __init__(self):
        pass

    def build(self, building):
        """
        this builds the buildings on the planet: first check for prices ect, then build a building_widget
        that overgives the values to the planet if ready
        :param building: string
        """
        planet = self.selected_planet
        # only build if selected planet is set
        if not planet: return

        # check for minimum population
        if building in self.buildings_list:
            if config.build_population_minimum[building] > planet.population:
                self.event_text = "you must reach a population of minimum " + str(
                    config.build_population_minimum[building]) + " people to build a " + building + "!"

                sounds.play_sound("bleep", channel=7)
                return

        # build building widget, first py the bill
        # pay the bill
        if planet.building_cue >= planet.building_slot_amount:
            self.event_text = "you have reached the maximum(" + str(planet.building_slot_amount) + ") of buildings that can be build at the same time on " + planet.name + "!"
            sounds.play_sound("bleep", channel=7)
            return

        if len(planet.buildings) + planet.building_cue >= planet.buildings_max:
            self.event_text = "you have reached the maximum(" + str(planet.buildings_max) + ") of buildings that can be build on " + planet.name + "!"
            sounds.play_sound("bleep", channel=7)
            return

        self.build_payment(building)

        # predefine variables used to build building widget to make shure it is only created once
        widget_key = None
        widget_value = None
        widget_name = None

        # check for prices
        if building in self.buildings_list:
            for key, value in self.prices[building].items():
                if (getattr(self.player, key) - value) > 0:

                    widget_key = key
                    widget_value = value
                    widget_name = building
                else:
                    return

        # create building_widget ( progressbar)
        if widget_key:
            widget_width = self.building_panel.get_screen_width()
            widget_height = 35
            spacing = 5

            # get the position and size
            win = pygame.display.get_surface()
            height = win.get_height()
            y = height - spacing - widget_height - widget_height * len(self.building_widget_list)

            sounds.play_sound(sounds.bleep2, channel=7)

            # print("build:", planet.building_slot_amount, planet.building_cue)

            building_widget = BuildingWidget(win=self.win,
                x=self.building_panel.screen_x,
                y=y,
                width=widget_width,
                height=widget_height,
                name=widget_name,
                fontsize=18,
                progress_time=5,
                parent=self,
                key=widget_key,
                value=widget_value,
                planet=planet,
                tooltip="building widdget", layer=4
                )

            # add building widget to building cue to make shure it can be build only if building_cue is < building_slots_amount
            planet.building_cue += 1

    def build_payment(self, building):
        """
        pays the bills if something is build ;)
        :param building: str
        """
        # only build if has selected planet
        if not self.selected_planet: return

        # if "building" is a building and not called from another button(hack)
        if building in self.buildings_list:
            # check for prices
            for key, value in self.prices[building].items():
                # if price is bigger than zero
                if (getattr(self.player, key) - value) > 0:
                    setattr(self.player, key, getattr(self.player, key) - value)

    def pause_game(self):
        if global_params.game_paused:
            global_params.game_paused = False
        else:
            global_params.game_paused = True

        print("pause_game", global_params.game_paused)
        if global_params.game_speed > 0:
            self.game_speed = global_params.game_speed
            global_params.game_speed = 0

            # global_params.enable_orbit = False
            self.event_text = "Game Paused!"

        else:
            global_params.game_speed = self.game_speed
            # global_params.enable_orbit = True
            self.event_text = "Game Continued!"

    def quit_game(self, events):
        """
        :param events:
        quit the game with quit icon or esc
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def set_screen_size(self, size, events):
        """
        set the screen size using 's'
        :param size:
        :param events:
        """

        for event in events:
            # ignore all inputs while any text input is active
            if global_params.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    screen_info = pygame.display.Info()
                    current_size = (screen_info.current_w, screen_info.current_h)
                    os.environ['SDL_VIDEO_CENTERED'] = '1'

                    if current_size[0] == global_params.WIDTH:
                        pygame.display.set_mode(size, pygame.RESIZABLE, pygame.DOUBLEBUF)
                        global_params.WIDTH_CURRENT = size[0]
                        global_params.HEIGHT_CURRENT = size[1]
                    else:
                        pygame.display.set_mode((
                            global_params.WIDTH, global_params.HEIGHT), pygame.RESIZABLE, pygame.DOUBLEBUF)
                        global_params.WIDTH_CURRENT = size[0]
                        global_params.HEIGHT_CURRENT = size[1]

                    #self.universe.set_screen_size((global_params.WIDTH_CURRENT, global_params.WIDTH_CURRENT))
                    # for i in sprite_groups.planets:
                    #     i.set_screen_size((global_params.WIDTH_CURRENT, global_params.WIDTH_CURRENT))

    def save_load(self, events):
        """
        stores the planet positions, use ctrl + S
        """
        # ignore all inputs while any text input is active
        if global_params.text_input_active:
            return
        # check events for l_ctr +s for saving
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.s_pressed = True
                if event.key == pygame.K_l:
                    self.l_pressed = True
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.s_pressed = False
                if event.key == pygame.K_l:
                    self.l_pressed = False
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = False

            if self.ctrl_pressed and self.s_pressed:
                print("self.save_planets()")
                self.save_planets()
                #self.save_objects("config.json", "ship_config", self.ships)

            if self.ctrl_pressed and self.l_pressed:
                self.load_planets()

    def save_planets(self):
        # save_load each file
        for planet in sprite_groups.planets:
            planet.save_to_db()
            # save_planets_data(self.planets, "database")

    def save_objects(self, filename, list_):
        if not list_:
            return
        data = {}
        for obj in list_:
            data[obj.name] = obj.get_dict()

        write_file(filename, data)

    def load_planets(self):
        # save_load each file
        for planet in sprite_groups.planets:
            planet.load_from_db()
            # save_planets_data(sprite_groups.planets, "database")

    def restart_game(self):
        self.selected_planet = None
        self.game_objects = []
        self.explored_planets = []

        # print ("before_init: ", len(sprite_groups.planets))
        for planet in sprite_groups.planets:
            sprite_groups.planets.remove(planet)
            planet.reset_planet()

        for planet in sprite_groups.planets:
            # planet.set_orbit_object()

            planet.explored = False
            planet.just_explored = False

        size_x = 250
        size_y = 35
        spacing = 10

        self.building_panel.__init__(self.win,
            x=self.world_width - size_x,
            y=spacing,
            width=size_x - spacing,
            height=size_y,
            isSubWidget=False,
            size_x=size_x,
            size_y=size_y,
            spacing=spacing,
            parent=self,
            layer=9)

        # print("after_init: ", len(sprite_groups.planets))
