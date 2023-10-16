import pygame
from pygame_widgets.util import drawText
from source.configuration.config import all_possible_resources, production, prices, technology_upgrades
from source.configuration.economy_params import EconomyParams
from source.configuration.info_text import create_info_panel_building_text
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image

population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

ICON_SIZE = 25
FONT_SIZE = 12


class BuildingConstructorWidget(WidgetBase, EconomyParams):
    """The code defines a class called BuildingConstructorWidget which is a subclass of WidgetBase and EconomyParams.
    It represents a widget that allows the user to construct buildings on a selected planet in a game.
    The widget contains buttons for different types of resources and buildings, and it handles the visibility and
    positioning of these buttons based on the selected planet's available resources and buildings.
    Example Usage:
    ```python # Create an instance of BuildingConstructorWidget
    building_widget = BuildingConstructorWidget(win, x, y, width, height, isSubWidget=False, **kwargs)

    # Set the widget to be visible
    building_widget.set_visible()

    # Draw the widget on the screen
    building_widget.draw()
    ```
    Main functionalities:

    - The BuildingConstructorWidget class represents a widget that allows the user to construct buildings on a selected
        planet in a game. - It inherits from the WidgetBase and EconomyParams classes.
    - The widget contains buttons for different types of resources and buildings.
    - It handles the visibility and positioning of these buttons based on the selected planet's available resources and
        buildings.

    Methods:
    - __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs): Initializes the BuildingConstructorWidget
        object with the specified parameters.
    - set_visible(self): Sets the visibility of the widget based on the selected planet.
        If the planet is not selected or its name is "???", the buttons are hidden.
        Otherwise, the buttons are shown and the maximum height of the widget is updated.
    - set_building_button_tooltip(self, i): Creates tooltips for the building buttons based on the selected resource.
        It retrieves the prices and production information from the prices and production dictionaries.
    - create_buttons(self): Creates the resource and building buttons for the widget. It iterates over the
        all_possible_resources list and creates an ImageButton for each resource. It also creates an ImageButton for each
        building associated with the selected resource.
    - hide_buttons(self): Hides all the resource and building buttons.
    - show_buttons(self): Shows the resource and building buttons based on the selected planet's available resources
        and buildings.
    - listen_(self, events): Listens for events, but does nothing in this implementation.
    - draw(self): Draws the widget on the screen. It sets the position and size of the widget's surface, frame,
        and buttons based on the selected planet's buildings. It also draws the widget's label.

    Fields:
    - max_height: The maximum height of the widget.
    - name: The name of the widget.
    - icon_size: The size of the buttons' icons.
    - parent: The parent widget.
    - frame_color: The color of the widget's frame.
    - surface: The surface of the widget.
    - surface_rect: The rectangle that defines the position and size of the widget's surface.
    - spacing: The spacing between buttons.
    - surface_frame: The frame of the widget's surface.
    - font_size: The size of the font used for the widget's text.
    - font: The font used for the widget's text.
    - info_text: The information text for the widget's buttons.
    - resource_buttons: A dictionary that stores the resource buttons.
    - building_buttons: A dictionary that stores the building buttons.
    - buttons: A dictionary that stores all the buttons.
    - max_height: The maximum height of the widget.

    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        EconomyParams.__init__(self)

        self.max_height = 0
        self.name = "building constructor"
        self.icon_size = kwargs.get('icon_size', ICON_SIZE)
        self.parent = kwargs.get("parent", None)
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.world_y
        self.spacing = self.parent.spacing
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)

        # text
        self.font_size = kwargs.get('font_size', FONT_SIZE)
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.info_text = kwargs.get("infotext")

        self.resource_buttons = {}
        self.building_buttons = {}
        self.buttons = {}
        self.create_buttons()

        # register
        self.parent.widgets.append(self)

    def set_visible(self):
        if not self.parent.parent.selected_planet or self.parent.parent.get_planet_name() == "???":
            self.hide_buttons()
            visible = False
            return visible

        else:
            self.show_buttons()
            self.parent.parent.building_panel.max_height += self.parent.sub_widget_height
            visible = True

        return visible

    def set_building_button_tooltip(self, i):  # codium ai
        """
        Summary
        The set_building_button_tooltip method is responsible for creating tooltips for the buttons in the
        BuildingConstructorWidget class.

        Example Usage:

        widget = BuildingConstructorWidget()
        tooltip = widget.set_building_button_tooltip("water")
        print(tooltip)

        Inputs:
        i (string): The key representing the resource type for which the tooltips are being created.

        Flow:

        Initialize an empty list return_list to store the tooltips.
        Map the resource key to the corresponding resource name if necessary.
        Create a list price_list that contains the prices required to build each building of the given resource type.
        The prices are obtained from the prices dictionary.
        Create a list production_list that contains the production details for each building of the given resource type.
        The production details include the increase in population limit, the resources produced, and any additional
        benefits. The production details are obtained from the production dictionary.
        Iterate over the price_list and production_list simultaneously and concatenate the corresponding elements to
        form the tooltips. Append each tooltip to the return_list.
        Return the return_list containing all the tooltips.

        Outputs:
        return_list (list): A list of tooltips for the buttons, each tooltip containing information about the prices
        and production of the buildings for the given resource type.

        """
        return_list = []

        # prices
        resource = i.key
        resource_mapping = {"mineral": "minerals"}
        resource = resource_mapping.get(resource, resource)

        price_list = [f"to build {'an' if building[0] == 'a' else 'a'} {building} you need: " +
                      ', '.join([f"{key}: {value}" for key, value in prices[building].items() if value > 0])
                      for building in self.buildings[resource]]

        # production
        text = ""

        production_list = [(". a " + building + " increases the planets population limit by " + str(
            population_buildings_values[building]) if building in self.population_buildings else "") +
                           (". an " if building[0] == "a" else ". a ") + building + " will produce: " +
                           ", ".join([key + ": " + str(value) for key, value in production[building].items() if
                                      value > 0]) +
                           (f"it will increase the maximum buildings on the planet by "
                            f"{technology_upgrades[building]['buildings_max']}, " if building == "university" else "") +
                           (f"this will allow you to build space ships!, " if building == "space harbor" else "") for
                           building in self.parent.buildings[resource]]

        for i in range(len(price_list)):
            return_list.append(price_list[i] + production_list[i])

        return return_list

    def show_building_buttons(self, sender):  # not working yet
        """
        shows the buildong button only if planet is explored
        :param resource:
        """

        print("resource:", sender)

    def create_buttons(self):  # codiom ai
        def create_button(x, y, width, height, image, tooltip, key, info_text, name):
            button = ImageButton(win=self.win, x=x, y=y, width=width, height=height, isSubWidget=False, parent=self,
                image=pygame.transform.scale(get_image(image), (25, 25)), tooltip=tooltip,
                frame_color=self.frame_color, moveable=False, include_text=True, layer=self.layer, key=key,
                info_text=info_text, name=name, text=name, textColours=(0, 0, 0), font_size=0)

            return button

        for resource in all_possible_resources:
            # id_ = all_possible_resources.index(resource)
            resource_button = create_button(self.get_screen_x(), self.surface_rect.y + self.spacing, self.icon_size,
                self.icon_size, resource + '_25x25.png', resource, resource, None, None)
            self.resource_buttons[resource] = resource_button
            self.buttons[resource] = resource_button

            if resource == 'minerals':
                resource = 'mineral'

            y = self.icon_size

            for building in getattr(self, resource + '_buildings'):
                info_text = create_info_panel_building_text()[building]
                building_button = create_button(self.get_screen_x(), self.surface_rect.y + self.spacing + self.icon_size + y,
                    self.icon_size, self.icon_size, building + '_25x25.png', '', resource, info_text, building)

                resource_button.children.append(building_button)

                self.building_buttons[building] = building_button
                self.buttons[building] = building_button
                tooltip_index = getattr(self, resource + '_buildings').index(building)
                building_button.tooltip = self.set_building_button_tooltip(building_button)[tooltip_index]

                y += self.icon_size

    def hide_buttons(self):
        for name, button in self.resource_buttons.items():
            button.hide()
        for name, button in self.building_buttons.items():
            button.hide()

    def show_buttons(self):
        for name, button in self.resource_buttons.items():
            if name == "mineral":
                name = "minerals"

            if name in self.parent.parent.selected_planet.possible_resources:
                button.show()
            else:
                button.hide()

        for name, button in self.building_buttons.items():
            key = button.key
            if key == "mineral":
                key = "minerals"

            if key in self.parent.parent.selected_planet.possible_resources:
                button.show()
            else:
                button.hide()

    def draw(self):
        if not self.set_visible():
            return

        if self._hidden:
            self.hide_buttons()
            return
        else:
            self.show_buttons()

        # frame
        self.surface_rect.x = self.parent.surface_rect.x
        self.surface_rect.y = self.parent.world_y + self.spacing + 5
        self.surface_rect.height = self.icon_size * 6

        for building in self.parent.parent.selected_planet.buildings:
            if building == "space harbor":
                self.surface_rect.y += self.parent.sub_widget_height

            if building == "particle accelerator":
                self.surface_rect.y += self.parent.sub_widget_height

            if building == self.name:
                self.surface_rect.y = self.parent.world_y + self.parent.sub_widget_height + self.spacing + 5

        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.win.blit(self.surface, self.surface_frame)

        # label
        drawText(self.win, self.name, self.frame_color,
            (self.surface_rect.x + self.parent.spacing_x - 36, self.surface_rect.y + self.spacing,
             self.get_screen_width(),
             20), self.font, "center")

        # buttons
        x = 0
        y = 0
        for resource, resource_button in self.resource_buttons.items():
            resource_button.set_position((
                self.surface_rect.x + x + self.spacing * 3, self.surface_rect.y + self.spacing + 20))

            x += self.icon_size

        for building, building_button in self.building_buttons.items():
            id_ = getattr(self, building_button.key + "_buildings").index(building)
            key = building_button.key

            if key == "mineral":
                key = "minerals"

            building_button.set_position((self.resource_buttons[key].get_screen_x(), self.resource_buttons[
                key].get_screen_y() + self.icon_size + self.spacing + self.icon_size * id_))

        self.max_height = self.surface_rect.height
