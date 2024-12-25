import pygame

from source.configuration.game_config import config

BORDER = -10
DEBUG_BORDER = 200


class LevelOfDetail:
    """
    Summary
    The LevelOfDetail class is responsible for managing the level of detail of a screen in a game. It allows setting the screen size, border size, and debug mode. It also provides a method to check if a given position is inside the screen limits.
    Example Usage
    # Create an instance of LevelOfDetail
    lod = LevelOfDetail()

    # Set the screen size
    lod.set_screen_size((800, 600))

    # Set the border size
    lod.set_border(20)

    # Enable debug mode
    lod.debug = True

    # Check if a position is inside the screen limits
    inside = lod.inside_screen((400, 300))
    print(inside)  # Output: True
    Code Analysis
    Main functionalities
    Set the screen size
    Set the border size
    Enable/disable debug mode
    Check if a position is inside the screen limits

    Methods
    __init__(): Initializes the LevelOfDetail instance and sets the initial values for the screen size, border size, and debug mode.
    debug: Getter and setter for the debug mode. When debug mode is enabled, the border size is set to a higher value.
    set_limits(): Updates the screen limits based on the current border size.
    set_border(border: int): Sets the border size and updates the screen limits.
    set_width(width: int): Sets the screen width and updates the screen limits.
    set_height(height: int): Sets the screen height and updates the screen limits.
    set_screen_size(screen_size: tuple): Sets the screen size (width and height) and updates the screen limits.
    inside_screen(pos: tuple) -> bool: Checks if a given position is inside the screen limits.

    Fields
    win: The window object representing the game screen.
    width: The width of the game screen.
    height: The height of the game screen.
    border: The size of the border around the screen.
    left_limit: The left limit of the screen (excluding the border).
    right_limit: The right limit of the screen (excluding the border).
    top_limit: The top limit of the screen (excluding the border).
    bottom_limit: The bottom limit of the screen (excluding the border).
    debug: A boolean indicating whether debug mode is enabled or not.
    """

    def __init__(self) -> None:
        self.win = config.win
        self.width = self.win.get_width()
        self.height = self.win.get_height()
        self.border = BORDER
        self.left_limit = 0
        self.right_limit = self.width
        self.top_limit = 0
        self.bottom_limit = self.height
        self.debug = False # be careful!!! you wont see some UI buttons if debug mode is enabled, because of the border
        self.set_limits()

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value) -> None:
        self._debug = value
        if value:
            self.border = DEBUG_BORDER
        else:
            self.border = BORDER
        self.set_limits()

    def set_limits(self) -> None:
        self.left_limit = self.border
        self.right_limit = self.width - self.border
        self.top_limit = self.border
        self.bottom_limit = self.height - self.border

    def set_border(self, border: int) -> None:
        self.border = border
        self.set_limits()

    def set_width(self, width: int) -> None:
        self.width = width
        self.set_limits()

    def set_height(self, height: int) -> None:
        self.height = height
        self.set_limits()

    def set_screen_size(self, screen_size: tuple):
        self.set_width(screen_size[0])
        self.set_height(screen_size[1])

    def draw_debug_rect(self):
        if not self.debug:
            return

        border_rect = pygame.Rect(self.left_limit, self.top_limit,
                self.right_limit - self.left_limit,
                self.bottom_limit - self.top_limit)
        pygame.draw.rect(self.win, (255, 0, 0), border_rect, 2)  # Red rectangle, 2 pixels wide

    def inside_screen(self, pos: tuple) -> bool:

        if pos[0] < self.left_limit:
            return False
        elif pos[0] > self.right_limit:
            return False
        elif pos[1] < self.top_limit:
            return False
        elif pos[1] > self.bottom_limit:
            return False
        else:
            return True




level_of_detail = LevelOfDetail()
