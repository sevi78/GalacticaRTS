import pygame


class UIHelper:
    """Main functionalities:

    The UIHelper class is designed to assist in the creation of dynamic user interfaces in Pygame. It provides methods
    for setting anchor points, spacing, and centering elements on the screen. It also includes a method for updating the
    positions of UI elements based on changes in the size of the Pygame display surface.

    Methods:
    - __init__(self, parent): initializes the UIHelper object with a reference to the parent object, sets the Pygame
    display surface, and initializes various fields
    - set_anchor_right(self, value): sets the anchor point for the right side of the UI element
    - set_anchor_bottom(self, value): sets the anchor point for the bottom of the UI element
    - set_spacing(self, spacing): sets the spacing between UI elements
    - center_pos(self, width, height): calculates the center position of the screen based on the width and height of the
      UI element
    - update(self): updates the positions of UI elements based on changes in the size of the Pygame display surface
    - hms(self, seconds): converts a number of seconds into a formatted string representing hours, minutes, and seconds

    Fields:
    - parent: a reference to the parent object
    - win: the Pygame display surface
    - width: the width of the Pygame display surface
    - height: the height of the Pygame display surface
    - right: the right edge of the UI element
    - left: the left edge of the UI element
    - top: the top edge of the UI element
    - bottom: the bottom edge of the UI element
    - anchor_right: the anchor point for the right side of the UI element
    - anchor_left: the anchor point for the left side of the UI element
    - anchor_top: the anchor point for the top of the UI element
    - anchor_bottom: the anchor point for the bottom of the UI element
    - spacing: the spacing between UI elements"""

    def __init__(self, parent):
        self.parent = parent
        self.win = pygame.display.get_surface()
        self.world_width = self.win.get_width()
        self.world_height = self.win.get_height()

        self.right = 0
        self.left = 0
        self.top = 0
        self.bottom = 0

        self.anchor_right = 0
        self.anchor_left = 0
        self.anchor_top = 0
        self.anchor_bottom = 0

        self.spacing = 10

    def set_anchor_right(self, value):
        self.anchor_right = self.world_width - value

    def set_anchor_bottom(self, value):
        self.anchor_bottom = self.height - value

    def set_spacing(self, spacing):
        self.spacing = spacing

    def update(self):
        """
        updates positions for dynamic UI
        :return:
        """
        self.win = pygame.display.get_surface()
        self.world_width = self.win.get_width()
        self.height = self.win.get_height()

        self.set_anchor_right(self.parent.building_panel.get_screen_width())
        self.set_anchor_bottom(30)

    def hms(self, seconds):
        """
        time converter
        :param seconds:
        :return: datetime format
        """

        h = seconds // 3600
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
