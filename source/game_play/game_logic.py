import os
import sys

import pygame

from source.configuration.game_config import config
from source.handlers.file_handler import write_file


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
        if config.game_paused:
            config.game_paused = False
        else:
            config.game_paused = True

        print("pause_game", config.game_paused)
        if config.game_speed > 0:
            self.game_speed = config.game_speed
            config.game_speed = 0

            # config.enable_orbit = False
            self.event_text = "Game Paused!"

        else:
            config.game_speed = self.game_speed
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
            if config.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    """ x = 0
                        y = 0
                        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"""
                    screen_info = pygame.display.Info()
                    current_size = (screen_info.current_w, screen_info.current_h)
                    os.environ['SDL_VIDEO_CENTERED'] = '1'
                    # # Set the position of the window to the second monitor
                    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, -1080)

                    if current_size[0] == config.width:
                        pygame.display.set_mode(size, pygame.RESIZABLE, pygame.DOUBLEBUF)
                        config.width_current = size[0]
                        config.height_current = size[1]
                    else:
                        pygame.display.set_mode((
                            config.width, config.height), pygame.RESIZABLE, pygame.DOUBLEBUF)
                        config.width_current = size[0]
                        config.height_current = size[1]

    def save_objects(self, filename, list_):
        if not list_:
            return
        data = {}
        for obj in list_:
            data[obj.name] = obj.get_dict()

        write_file(filename, "config", data)
