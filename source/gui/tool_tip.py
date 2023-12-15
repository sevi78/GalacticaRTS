from collections import Counter

import pygame
from pygame.locals import MOUSEMOTION
from pygame_widgets import Mouse

from source.database.saveload import load_file
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.utils import global_params
from source.utils.text_formatter import format_number

INVISIBLE_X = -1000
INVISIBLE_Y = -1000
INVISIBLE_X_OFFSET = 10
INVISIBLE_Y_OFFSET = 10
TOOLTIP_ALPHA = 200


class ToolTip(WidgetBase):
    """Main functionalities:
    The ToolTip class is responsible for creating and displaying a tooltip on the screen. It receives a surface, position, size, color, and text color as parameters, and it can be a subwidget. It moves with the mouse and displays the text passed to it through the global_params module. It draws a filled rectangle with a border and the text passed to it.

    Methods:
    - __init__: initializes the ToolTip object with the given parameters and sets some default values.
    - move: moves the tooltip with the mouse and limits its position to the screen size.
    - get_text: gets the text to be displayed from the global_params module and sets the visibility of the tooltip accordingly.
    - draw_bordered_rect: draws a bordered rectangle around the tooltip.
    - draw: renders the tooltip on the screen with a filled rectangle, border, and text.
    - listen: listens to events, but does not do anything.
    - update: updates the tooltip by getting the text, moving it, and drawing it.

    Fields:
    - win: the surface on which the tooltip is drawn.
    - color: the color of the filled rectangle.
    - text_color: the color of the text.
    - x, y: the position of the tooltip.
    - width, height: the size of the tooltip.
    - size: a tuple containing the width and height of the tooltip.
    - rect_filled: a surface representing the filled rectangle of the tooltip.
    - parent: the parent widget of the tooltip.
    - _text: the text to be displayed.
    - font: the font used for the text.
    - text_img: a surface representing the rendered text.
    - txt_rect: the rectangle containing the rendered text.
    - visible: a boolean indicating whether the tooltip is visible or not."""

    def __init__(self, surface, x, y, width, height, color, text_color, isSubWidget, parent, **kwargs):
        super().__init__(surface, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 10)
        self.visible = False
        self.win = surface
        self.color = color
        self.text_color = text_color
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.height = height
        self.size = (self.world_width, self.height)
        self.rect_filled = pygame.surface.Surface(self.size)
        self.rect_filled.set_alpha(TOOLTIP_ALPHA)
        self.parent = parent

        # text
        self._text = ""
        self.font_size = 18
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.text_img = None
        self.txt_rect = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value

    def move(self, event):
        if self.visible and self.text_img:

            # limit position x
            max_x = pygame.display.get_surface().get_width()
            x = event.pos[0] + self.text_img.get_width() / 2
            min_x = 0
            x1 = event.pos[0] - self.text_img.get_width() / 2

            if x > max_x:
                self.world_x = max_x - self.text_img.get_width() - INVISIBLE_X_OFFSET
            elif x1 < min_x:
                self.world_x = min_x
            else:
                self.world_x = event.pos[0] - self.text_img.get_width() / 2

            # limit position y
            max_y = pygame.display.get_surface().get_height() - self.text_img.get_height()
            y = event.pos[1] + self.text_img.get_height()
            min_y = 0
            y1 = event.pos[1] - self.text_img.get_height()

            if y > max_y:
                self.world_y = max_y - self.text_img.get_height() - INVISIBLE_Y_OFFSET
            elif y1 < min_y:
                self.world_y = min_y
            else:
                self.world_y = event.pos[1] + self.text_img.get_height()

        else:
            self.world_x = INVISIBLE_X
            self.world_y = INVISIBLE_Y

    def get_text(self):
        self._text = global_params.tooltip_text
        if self._text != "":
            self.visible = True
        else:
            self.visible = False

    def reset_tooltip(self, obj):
        x, y = Mouse.getMousePos()
        if obj.on_hover_release_callback(x, y, obj.rect):
            global_params.tooltip_text = ""

    def listen(self, events):
        for event in events:
            if event.type == MOUSEMOTION:
                self.update(event)

    def update(self, events):
        self.get_text()
        self.move(events)
        self.draw()

    def draw(self):
        self.text_img = self.font.render(self._text, True, self.text_color)

        self.world_width = self.text_img.get_rect().width + 10
        self.height = self.text_img.get_rect().height + 7
        self.size = (self.world_width, self.height)

        self.rect_filled = pygame.surface.Surface(self.size)
        self.rect_filled.set_alpha(TOOLTIP_ALPHA)

        self.win.blit(self.rect_filled, (self.world_x, self.world_y))
        self.win.blit(self.text_img, (self.world_x + 5, self.world_y + 5))

        pygame.draw.rect(self.win, self.frame_color, (
            self.world_x, self.world_y, self.world_width,
            self.height), 1, int(global_params.ui_rounded_corner_radius_small))


class ToolTipGenerator:
    def __init__(self):
        self.json_dict = load_file("buildings.json")

    def get_building(self, building):
        dict_ = {}
        for category, building_names in self.json_dict.items():
            if building in building_names.keys():
                for item, value in building_names[building].items():
                    dict_[item] = value
        return dict_

    def create_building_tooltip(self, building):
        price_text = f"to build a {building}, you will need "
        production_text = ""
        for key, value in self.get_building(building).items():
            if key.startswith("price_"):
                resource_key = key.split('price_')[1]
                if value > 0:
                    price_text += f"{resource_key}: {value}, "

            if key.startswith("production_"):
                production_key = key.split('production_')[1]
                if production_key == "minerals":
                    production_key = "mineral"

                if value > 0:
                    if production_text == "":
                        production_text = f"it will produce: "
                    production_text += f" {production_key}:  {value}, "
        text = price_text[:-2] + ". " + production_text[:-2]

        return text

    def create_level_tooltip(self, level, data):
        # get the size of the level
        width, height = (format_number(data["globals"]["width"] * 1000, 1),
                         format_number(data["globals"]["height"] * 1000, 1))

        # Count the number of planets, sun, moons
        num_planets = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "planet")
        num_moons = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "moon")
        num_suns = sum(1 for obj in data["celestial_objects"].values() if obj["type"] == "sun")

        # Get the possible resources
        resources = set()
        for obj in data["celestial_objects"].values():
            resources.update(obj["possible_resources"])

        # Count all resources in all planets
        all_resources = []
        for obj in data["celestial_objects"].values():
            all_resources.extend(obj["possible_resources"])

        # Order the resources from most to least
        ordered_resources = dict(sorted(Counter(all_resources).items(), key=lambda item: item[1], reverse=True))

        # Convert the ordered_resources dictionary to a list of tuples and then access the first item
        ordered_resources_list = list(ordered_resources.items())

        # Count the alien_population of all planets and moons
        alien_population_count = sum(
            obj["alien_population"] for obj in data["celestial_objects"].values() if obj["type"] in ["planet", "moon"])

        # Create the tooltip strings
        area_text = f"{width} x{height} km"
        if num_suns > 1:
            suntext = f"There are {num_suns} suns in this area of {area_text} of the universe"
        else:
            suntext = f"There is a single sun in this area of {area_text} of the universe"

        if num_planets > 1:
            planettext = f"with {num_planets} planets"
        else:
            planettext = f"with a single planet"

        if num_moons > 1:
            moontext = f"and {num_moons} moons."
        else:
            moontext = f"and a single moon."

        if alien_population_count > 0:
            alien_text = f"An estimated {format_number(alien_population_count, 1)} extraterrestrials live there. "
        else:
            alien_text = "(un)fortunately there are no aliens here."

        if ordered_resources_list[0][0] == "city":
            resource_text = f"A good place to grow population."
        else:
            resource_text = f"plenty of {ordered_resources_list[0][0]} can be found here !"


        # create the final tooltip
        tooltip = (f"level {level}: {suntext} {planettext} {moontext} Possible resources: {', '.join(resources)}."
                   f" {resource_text} {alien_text} ")

        return tooltip


tooltip_generator = ToolTipGenerator()
