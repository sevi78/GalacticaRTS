import os
import sys

import pygame

from source.configuration.game_config import config
from source.handlers.file_handler import write_file
from source.handlers.time_handler import time_handler


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

    def pause_game(self):
        if self.game_client.connected:
            self.game_client.send_message({"f": "pause_game"})
        else:
            self.handle_pause_game()



    def handle_pause_game(self):
        # toggle game_paused
        config.game_paused = not config.game_paused

        # print("handle_pause_game.pause_game:", config.game_paused)
        if config.game_paused:
            time_handler.stored_game_speed = time_handler.game_speed
            time_handler.game_speed = 0
            self.event_text = "Game Paused!"
            print(f"handle_pause_game.Game Paused! {time_handler.game_speed}")
        else:
            time_handler.game_speed = time_handler.stored_game_speed
            self.event_text = "Game Continued!"
            print(f"handle_pause_game.Game Continued! {time_handler.game_speed}")

    def quit_game(self, events):
        """
        :param events:
        quit the game with quit icon or esc
        """

        for event in events:
            if event.type == pygame.QUIT:
                # self.network_client.disconnect()
                self.game_client.disconnect_from_server()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_client.disconnect_from_server()
                    # self.network_client.disconnect()
                    sys.exit()



    def set_screen_size(self, size, events):
        for event in events:
            if config.text_input_active:
                return

            if event.type == pygame.KEYDOWN:
                screen_info = pygame.display.Info()
                current_w, current_h = screen_info.current_w, screen_info.current_h

                if event.key == pygame.K_UP:
                    current_size = (screen_info.current_w, screen_info.current_h)
                    os.environ['SDL_VIDEO_CENTERED'] = '1'

                    if current_size[0] == config.width:
                        pygame.display.set_mode(size, pygame.RESIZABLE, pygame.DOUBLEBUF)
                        config.width_current = size[0]
                        config.height_current = size[1]
                    else:
                        pygame.display.set_mode((config.width, config.height), pygame.RESIZABLE, pygame.DOUBLEBUF)
                        config.width_current = size[0]
                        config.height_current = size[1]

                if event.key == pygame.K_LEFT:
                    new_width = current_w // 2
                    size = (new_width, current_h)
                    position = (0, 0)
                    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{position[0]},{position[1]}'
                    pygame.display.set_mode(size, pygame.RESIZABLE, pygame.DOUBLEBUF)
                    config.width_current = new_width
                    config.height_current = current_h

                if event.key == pygame.K_RIGHT:
                    new_width = current_w // 2
                    size = (new_width, current_h)
                    position_x = current_w - new_width
                    position = (position_x, 0)
                    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{position[0]},{position[1]}'
                    pygame.display.set_mode(size, pygame.RESIZABLE, pygame.DOUBLEBUF)
                    config.width_current = new_width
                    config.height_current = current_h

    def save_objects(self, filename, list_):
        if not list_:
            return
        data = {}
        for obj in list_:
            data[obj.name] = obj.get_dict()

        write_file(filename, "config", data)
