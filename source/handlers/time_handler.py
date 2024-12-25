import time

import pygame

from source.configuration.game_config import config

# Set the desired FPS
FPS = 60
SCENE_UPDATE_INTERVAL = 25


class TimeHandler:  # original
    def __init__(self) -> None:
        self.world_time = time.time()
        self.clock = pygame.time.Clock()
        self.game_speed = config.game_speed
        self.stored_game_speed = config.game_speed
        self.count = 0
        self.value = 1
        self.set_fps(FPS)
        self.game_start_time = None
        self.time = time.time()

        # server_update timer
        self.last_server_update = time.time()
        self.server_update_interval = 1 / SCENE_UPDATE_INTERVAL

    def server_update_time_reached(self):
        """ returns True if enough time has passed since the last server update """
        if time.time() - self.last_server_update > self.server_update_interval:
            self.last_server_update = time.time()
            return True
        return False

    def set_game_speed(self, value: int) -> None:
        self.game_speed = value
        print("time_handler.set_game_speed", value)
        data = {"f": "set_game_speed", "game_speed": value}
        if hasattr(config.app, "game_client") and config.app.game_client.connected:
            config.app.game_client.send_message({"f": "set_game_speed", "game_speed": self.game_speed})
        else:
            self.handle_set_game_speed(data)

    def handle_set_game_speed(self, data: dict) -> None:
        value = data["game_speed"]
        self.game_speed = value
        self.stored_game_speed = self.game_speed
        if config.app.game_time:
            config.app.game_time.clock_slider.set_value(self.game_speed)

    def set_world_time(self, value: int) -> None:
        self.world_time = value

    @property
    def fps(self) -> float:
        return self.clock.get_fps()

    def set_fps(self, fps: int) -> None:  # Rename update_fps method to set_fps
        self.clock.tick(fps)

    def update_time(self):
        self.time = time.time()

        # update clients
        if self.server_update_time_reached():

            config.app.game_client.message_handler.update_clients()

    def listen(self, events):
        clock_slider = config.app.game_time.clock_slider
        for event in events:
            if event.type == pygame.KEYDOWN:
                # print(f"game_time_widget.listen: {event.key}")
                if event.key == 1073741911:  # pygame.K_PLUS:
                    clock_slider.set_value(clock_slider.get_value() + 1)
                elif event.key == 1073741910:  # pygame.K_MINUS:
                    clock_slider.set_value(clock_slider.get_value() - 1)

                elif event.key == 1073741913:  # 1
                    clock_slider.set_value(1)
                elif event.key == 1073741914:  # 2
                    clock_slider.set_value(10)
                elif event.key == 1073741915:  # 3
                    clock_slider.set_value(50)
                elif event.key == 1073741916:  # 4
                    clock_slider.set_value(100)
                elif event.key == 1073741917:  # 4
                    clock_slider.set_value(1000)


time_handler = TimeHandler()
