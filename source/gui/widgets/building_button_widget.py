import pygame.display

from source.configuration.game_config import config
from source.draw.rectangle import draw_transparent_rounded_rect
from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.widget_handler import WidgetHandler
from source.multimedia_library.images import get_image, scale_image_cached
from source.text.info_panel_text_generator import info_panel_text_generator
from source.text.tooltip_gen import tooltip_generator

ICON_SIZE = 25
IMAGE_RAW_SIZE = 125


class BuildingButtonWidget(WidgetBase):
    """
    Summary:
    The BuildingButtonWidget class is a widget used in a graphical user interface. It represents a button that displays
    different building options for a specific resource category. The class handles the creation, positioning,
    and visibility of the buttons based on the selected resource category and the parent widget.

    Example Usage:
    # Create a BuildingButtonWidget object
    building_button_widget = BuildingButtonWidget(win, x, y, width, height, app)

    # Show the widget and its buttons
    building_button_widget.show()

    # Hide the widget and its buttons
    building_button_widget.hide()
    Code Analysis
    Main functionalities
    Creates a widget that displays building buttons for different resource categories
    Handles the visibility of the buttons based on the selected resource category and parent widget
    Manages the positioning and layout of the buttons within the widget

    Methods:
    __init__(self, win, x, y, width, height, app, is_sub_widget=False, **kwargs): Initializes the BuildingButtonWidget
    object with the specified parameters and sets up the widget's properties and buttons.
    create_buttons(self): Creates the building buttons for each resource category and adds them to the widget.
    hide(self): Hides the widget and its buttons.
    hide_building_buttons(self): Hides the building buttons within the widget.
    show(self): Shows the widget and its buttons.
    on_resource_click(self, resource_button): Handles the click event on a resource button and shows or hides the
    corresponding building buttons.
    hide_unused_resources(self): Hides the resource buttons that are not applicable to the current parent widget.
    set_frame_height(self): Sets the height of the widget's frame based on the visible building buttons.
    reposition_buttons(self): Repositions the buttons within the widget based on their visibility.
    draw_frame(self): Draws the frame of the widget.
    draw(self): Draws the widget and its buttons on the screen.

    Fields:
    app: The application object that the widget belongs to.
    max_width: The maximum width of the widget.
    max_height: The maximum height of the widget.
    resource_buttons: A list of resource buttons within the widget.
    building_buttons: A dictionary of building buttons grouped by resource category.
    buttons: A dictionary of all buttons within the widget.
    name: The name of the widget.
    icon_size: The size of the icons used in the buttons.
    parent: The parent widget of the BuildingButtonWidget.
    fixed_parent: A flag indicating whether the parent widget is fixed or not.
    frame_color: The color of the widget's frame.
    surface: The surface object representing the widget.
    rect: The rectangle object representing the position and size of the widget.
    spacing: The spacing between buttons within the widget.
    surface_frame: The frame of the widget's surface.
    corner_radius: The radius of the rounded corners of the widget's frame.
    sub_widget_height: The height of the subwidget within the parent widget.
    """

    def __init__(self, win, x, y, width, height, app, is_sub_widget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        self.app = app
        self.max_width = 0
        self.max_height = 0
        self.max_height = 0
        self.resource_buttons = []
        self.active_resource_buttons = []
        self.building_buttons = {}
        self.buttons = {}

        self.name = "building button widget"
        self.icon_size = kwargs.get('icon_size', ICON_SIZE)
        self.parent = kwargs.get("parent", None)
        self.fixed_parent = kwargs.get("fixed_parent", False)
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.set_alpha(config.ui_panel_alpha)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.spacing = kwargs.get("spacing", 10)
        self.corner_radius = config.ui_rounded_corner_radius_small

        # subwidget height of building panel
        self.sub_widget_height = 0

        # construct buttons
        self.create_buttons()

        # register
        self.app.building_button_widgets.append(self)
        self.parent.widgets.append(self)

        self.hide()
        self.hide_building_buttons()

    def __delete__(self, instance):
        for widget in self.widgets:
            WidgetHandler.remove_widget(widget)
            del widget

        self.building_buttons = {}
        self.buttons = {}
        self.widgets = []
        WidgetHandler.remove_widget(self)
        del self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        self.hide_building_buttons()

    def create_button(self, x, y, width, height, image, tooltip, key, info_text, name, **kwargs):
        on_click = kwargs.get("on_click", lambda: print("no_function"))
        button = ImageButton(
                win=self.win,
                x=x,
                y=y,
                width=width,
                height=height,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image(image), (ICON_SIZE, ICON_SIZE)),
                image_raw=get_image(image),
                tooltip=tooltip,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                key=key,
                info_text=info_text,
                name=name,
                text=name,
                text_color=(0, 0, 0),
                font_size=0,
                on_click=on_click,
                info_panel_alpha=kwargs.get("info_panel_alpha", 255))

        return button

    def create_buttons(self):
        x = self.rect.x
        resource_categories = building_factory.get_resource_categories()

        # resource buttons
        for resource in resource_categories:
            y = self.rect.y
            resource_button = ImageButton(
                    win=self.win,
                    x=x,
                    y=y,
                    width=ICON_SIZE,
                    height=ICON_SIZE,
                    is_sub_widget=False,
                    parent=self,
                    image=scale_image_cached(get_image(resource + '_25x25.png'),
                            (ICON_SIZE, ICON_SIZE)),
                    tooltip=resource,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    key=resource,
                    info_text=None,
                    name=resource,
                    text_color=(0, 0, 0),
                    font_size=0)

            self.resource_buttons.append(resource_button)
            self.buttons[resource] = resource_button
            self.widgets.append(resource_button)

            # building buttons
            for building in building_factory.json_dict[resource]:
                info_text = info_panel_text_generator.create_info_panel_building_text(building)
                building_button = self.create_button(
                        x,
                        y + self.icon_size,
                        self.icon_size,
                        self.icon_size,
                        building + '_25x25.png',
                        tooltip_generator.create_building_tooltip(building),
                        resource,
                        info_text,
                        building,
                        info_panel_alpha=110
                        )

                resource_button.children.append(building_button)
                self.building_buttons[building] = building_button
                self.buttons[building] = building_button
                self.widgets.append(building_button)
                y += self.icon_size

            y += self.icon_size
            x += self.icon_size

    def hide(self):
        """hides self and its widgets
        """
        self._hidden = True
        for i in self.widgets:
            i.hide()

    def hide_building_buttons(self):
        if not hasattr(self, "resource_buttons"):
            return

        [building_button.hide() for resource_button in self.resource_buttons for building_button in
         resource_button.children]

    def show(self):
        """shows self and its widgets
        """
        if not self.app.selected_planet:
            return

        if hasattr(self.parent, "explored"):
            if not self.parent.explored:
                return

        if self.parent.name == "building panel":
            if not self.app.selected_planet.explored:
                self.hide()
                return

        self._hidden = False
        [i.show() for i in self.widgets]

        self.hide_unused_resources()
        self.hide_building_buttons()
        self.set_frame_height()

    def on_resource_click(self, resource_button):
        """ this is called from the resource buttons"""
        for i in resource_button.children:
            if i._hidden:
                i.show()
            else:
                i.hide()

        self.set_frame_height()

        # get resource key
        # print ("on_resource_click", resource_button.key, resource_button.name, resource_button.children)
        if hasattr(self.app, "building_edit"):
            self.app.building_edit.category = resource_button.key

            # if resource_button is a building
            if len(resource_button.children) == 0:
                self.app.building_edit.building = resource_button.name

    def hide_unused_resources(self):
        """ called from selected_planet.setter in main.py(self.app)"""
        if not self.app.explored_planets:
            self.hide()
            return

        if not self.app.selected_planet.explored and self.app.selected_planet == self.parent:
            self.hide()
            return

        if self.parent._hidden:
            self.hide()
            return

        if not self.fixed_parent:
            self.parent = self.app.selected_planet

        for resource_button in self.resource_buttons:
            key_ = resource_button.key
            if key_ == "mineral":   key_ = "minerals"

            if self.parent.name == "building panel":
                if key_ not in self.app.selected_planet.economy_agent.possible_resources:
                    resource_button.hide()
            else:
                if key_ not in self.parent.economy_agent.possible_resources:
                    resource_button.hide()

        self.set_frame_height()

    def set_frame_height(self):
        building_button_lengths = []
        for resource_button in self.resource_buttons:
            building_buttons = [b for b in resource_button.children if not b._hidden]
            building_button_lengths.append(len(building_buttons))

        if self._hidden:
            self.max_height = 0
        else:
            self.max_height = ICON_SIZE + max(building_button_lengths) * ICON_SIZE + self.spacing * 2

    def reposition_buttons(self):
        index = 0
        for resource_button in self.resource_buttons:
            if resource_button._hidden:
                index += 1
            resource_button.screen_x = self.rect.x + self.spacing + (
                    self.resource_buttons.index(resource_button) - index) * ICON_SIZE
            resource_button.screen_y = self.rect.y + self.spacing
            resource_button.set_image_position()
            for building_button in resource_button.children:
                building_button.screen_x = resource_button.screen_x
                building_button.screen_y = ICON_SIZE + resource_button.screen_y + resource_button.children.index(building_button) * ICON_SIZE
                building_button.set_image_position()

    def draw_frame(self):
        self.rect.width = self.max_width
        self.rect.height = self.max_height

        draw_transparent_rounded_rect(self.win, (0, 0, 0), self.rect,
                config.ui_rounded_corner_radius_small, config.ui_panel_alpha)
        pygame.draw.rect(self.win, self.frame_color, self.rect,
                config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)

        if len(self.active_resource_buttons) > 0:
            self.set_frame_height()
        else:
            self.max_height = 0

    def draw(self):
        # if not inside_screen(self.rect.center):
        #     self.hide()

        if self._hidden or self._disabled:
            return

        self.active_resource_buttons = [_ for _ in self.resource_buttons if not _._hidden]

        # check for parent, then set different positions and sizes based on parent
        if not self.parent.name == "building panel":
            self.spacing = 5
            self.corner_radius = 5
            if config.show_overview_buttons:
                self.hide()
                return

            elif self._hidden:
                self.show()

            self.max_width = len(self.active_resource_buttons) * ICON_SIZE + self.spacing * 2
            self.rect.centerx = self.parent.rect.centerx
            self.rect.y = self.parent.rect.centery + self.parent.rect.height

        # if parent is a planet
        else:
            self.max_width = self.parent.surface_rect.width
            self.rect.x = self.parent.surface_rect.x
            self.rect.y = self.parent.max_height - self.max_height - self.sub_widget_height

            if self.app.selected_planet:
                # set correct y_position using sub_widget_height
                self.sub_widget_height = 0
                if "space harbor" in self.app.selected_planet.economy_agent.buildings:
                    self.sub_widget_height += self.parent.sub_widget_height

                if "particle accelerator" in self.app.selected_planet.economy_agent.buildings:
                    self.sub_widget_height += self.parent.sub_widget_height

                # make shure it gets drawn after building panel is reopened
                if self._hidden:
                    self.show()

        self.reposition_buttons()

        # draw frame must be last to prevent bliting errors
        if not self._hidden:
            self.draw_frame()
