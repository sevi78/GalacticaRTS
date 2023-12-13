import os
import sys
import pygame

from source.factories.planet_factory import planet_factory
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.database.saveload import write_file


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

                    # self.universe.set_screen_size((global_params.WIDTH_CURRENT, global_params.WIDTH_CURRENT))
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

                #planet_factory.save_planets()

            if self.ctrl_pressed and self.l_pressed:
                pass
                #planet_factory.load_planets()

    def save_objects(self, filename, list_):
        if not list_:
            return
        data = {}
        for obj in list_:
            data[obj.name] = obj.get_dict()

        write_file(filename, data)



    def restart_game(self):
        planet_factory.delete_planets()
        self.explored_planets = []
        self.player = None
        self.create_player()


        self.selected_planet = sprite_groups.planets.sprites()[0]
        # planet_factory.load_planets()

        # size_x = 250
        # size_y = 35
        # spacing = 10
        #
        # self.building_panel.__init__(self.win,
        #     x=self.world_width - size_x,
        #     y=spacing,
        #     width=size_x - spacing,
        #     height=size_y,
        #     isSubWidget=False,
        #     size_x=size_x,
        #     size_y=size_y,
        #     spacing=spacing,
        #     parent=self,
        #     layer=9)
