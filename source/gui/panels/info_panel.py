import pygame

from source.configuration import config
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.utils.text_wrap import TextWrap

PLANET_IMAGE_SIZE = 100
TOGGLESIZE = 20


class InfoPanel(WidgetBase, TextWrap):
    """Main functionalities:
    The InfoPanel class is a subclass of WidgetBase and represents a panel that displays information to the user. It can display text, images, and a frame. The panel can be resized based on the length of the text displayed, and the text is automatically wrapped to fit within the panel. The panel can also be repositioned, and the planet image can be aligned to the top right or center of the panel.

    Methods:
    - update_text(): wraps the text and updates the height of the panel
    - set_text(): sets the text to be displayed on the panel
    - set_colors(): sets the color of the text and background of the panel
    - set_planet_image(): sets the planet image to be displayed on the panel
    - set_size_from_text(): sets the size of the panel based on the height of the text
    - wrap_text(): wraps the text to fit within the panel
    - reposition(): repositions the panel (not currently working)
    - draw(): draws the panel, frame, planet image, and text
    - listen(): listens for events (not currently implemented)
    - update(): updates the panel (calls draw() if visible)

    Fields:
    - layer: the layer of the panel
    - parent: the parent object of the panel
    - width: the width of the panel
    - height: the height of the panel
    - size: the size of the panel (tuple of width and height)
    - win: the surface on which to draw the panel
    - font: the font used for the text on the panel
    - text: the text to be displayed on the panel
    - color: the color of the text on the panel
    - bg_color: the background color of the panel
    - pos: the position of the panel (tuple of x and y coordinates)
    - x: the x-coordinate of the top left corner of the panel
    - y: the y-coordinate of the top left corner of the panel
    - border: the border size of the panel
    - surface_rect: the rectangle frame of the panel
    - planet_image: the planet image to be displayed on the panel
    - planet_rect: the rectangle frame of the planet image
    - rect_filled: the filled rectangle of the panel
    - word_height_sum: the sum of the heights of all the words in the text
    - text_surfaces: a dictionary of the text surfaces and their positions
    - visible: a boolean indicating whether the panel is visible or not"""

    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        TextWrap.__init__(self)
        self.name = "info panel"
        self.layer = kwargs.get("layer", 4)
        self.parent = kwargs.get("parent")
        self.world_width = width
        self.height = height
        self.max_height = self.height
        self.size = (self.world_width, self.height)
        self.win = win
        self.font_size = 18
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.text = config.info_text
        self.color = (0, 0, 0)
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.pos = [x, y]
        self.world_x = self.pos[0]
        self.world_y = self.pos[1]
        self.set_colors(self.frame_color, (12, 10, 1))
        self.surface_rect = pygame.draw.rect(self.win, self.frame_color, pygame.Rect(self.world_x, self.world_y, self.world_width,
            self.height + 10), 1, global_params.ui_rounded_corner_radius_small)
        self.planet_image = None
        self.planet_rect = None
        self.rect_filled = pygame.Surface((self.world_width, self.height))

        # visible
        self.visible = True

        # toggle switch to pop in or out
        self.toggle_switch = ToggleSwitch(self, 15)
        self.init = 0

        self.update_text()

    def update_text(self):
        # Wrap text before rendering onto surface
        self.wrap_text(self.text, self.pos, self.size, self.font, self.color)
        self.set_size_from_text()
        if self.planet_image:
            self.set_planet_image(self.planet_image)
        self.reposition()

    def set_text(self, text):
        """
        this is called from outside:
        :param text:
        """
        self.text = ""
        self.text = text

    def set_colors(self, color, bg_color):
        self.color = color
        self.bg_color = bg_color

    def set_planet_image(self, planet_image, **kwargs):

        # self.set_size_from_text()
        size = kwargs.get("size", None)
        align = kwargs.get("align", "topright")
        alpha = kwargs.get("alpha", 128)

        if size:
            self.planet_image = pygame.transform.scale(planet_image, size)
        else:
            self.planet_image = pygame.transform.scale(planet_image, (
                PLANET_IMAGE_SIZE, PLANET_IMAGE_SIZE))

        self.planet_rect = self.planet_image.get_rect()

        if align == "topright":
            self.planet_rect.right = self.rect_filled.get_rect().right + self.get_screen_x()
            self.planet_rect.top = self.rect_filled.get_rect().top + self.get_screen_y()

        elif align == "center":
            self.planet_rect.left = self.world_x + self.surface_rect.width / 2
            self.planet_rect.centery = self.world_y + self.surface_rect.height / 2

        if alpha:
            self.planet_image.set_alpha(alpha)

    def set_size_from_text(self):
        self.height = self.word_height_sum
        self.size = self.world_width, self.height
        self.max_height = self.surface_rect.height + self.toggle_switch.toggle_size

    def draw(self):
        if self._hidden:
            return

        if self.parent.build_menu_visible: return
        # gets the wrapped text
        self.update_text()

        # draw the panel
        self.rect_filled = pygame.Surface((self.world_width, self.height + 10))
        self.rect_filled.fill(self.bg_color)
        self.rect_filled.set_alpha(128)

        # draw the frame
        self.surface_rect = pygame.draw.rect(self.win, self.frame_color, pygame.Rect(self.world_x, self.world_y, self.world_width,
            self.height + 10), ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)

        # draw the planet icon
        if hasattr(self, 'planet_image') and self.planet_image:
            self.win.blit(self.planet_image, self.planet_rect)

        # self.toggle_switch.reposition()

        # reset text_surfaces for correct displaying
        self.text_surfaces = {}

        if not self.init:
            self.reposition()
            self.init = 1

        self.max_height = self.surface_rect.height + self.toggle_switch.toggle_size

    def reposition(self):
        self.toggle_switch.reposition()
