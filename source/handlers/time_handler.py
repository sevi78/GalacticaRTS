import pygame

# Set the desired FPS
FPS = 60


class TimeHandler:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self._game_speed = 1
        self.count = 0
        self.value = 1
        self.set_fps(FPS)

    def __repr__(self) -> str:
        return f"""
        game_speed: {self.game_speed}
        fps: {self.fps}
        factor (self.fps / self.game_speed): {self.get_time_factor()}
        """

    @property
    def game_speed(self):
        return self._game_speed

    @game_speed.setter
    def game_speed(self, value):
        self._game_speed = max(value, 1)  # Use max(value, 1) to ensure game speed is never less than 1

    @property
    def fps(self) -> float:
        return self.clock.get_fps()

    def get_time_factor(self) -> float:
        return self.game_speed / self.fps if self.fps else 0  # Use return self.game_speed / self.fps if self.fps else 0 to avoid try-except block

    def set_fps(self, fps: int) -> None:  # Rename update_fps method to set_fps
        self.clock.tick(fps)


time_handler = TimeHandler()
# def main():
#
#
#     # Start the main loop
#     while True:
#         time_handler.set_fps(FPS)
#         # Get events from the event queue
#         for event in pygame.event.get():
#             # Check for the quit event
#             if event.type == pygame.QUIT:
#                 # Quit the game
#                 pygame.quit()
#                 sys.exit()
#
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     time_handler.game_speed += 1
#                 if event.key == pygame.K_DOWN:
#                     time_handler.game_speed -= 1
#
#                 # if event.key == pygame.K_SPACE:
#                 #     dummy.update()
#                 #     print(time_handler)
#                 #     print(dummy)
#
#         dummy.update_value()
#         print(time_handler)
#         print(dummy)
#
#         # Draw the game screen
#         pygame.display.update()
#
#         # Limit the FPS by sleeping for the remainder of the frame time
#
#
# if __name__ == "__main__":
#     pygame.init()
#     pygame.display.set_mode((400, 400))
#     dummy = Dummy(time_handler)
#     main()
