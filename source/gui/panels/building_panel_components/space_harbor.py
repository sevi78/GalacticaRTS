import pygame
from pygame_widgets.util import drawText
from source.factories.building_factory import building_factory
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image
from source.gui.panels.info_panel_components.info_panel_text_generator import info_panel_text_generator


class SpaceHarbor(WidgetBase):
    """
    displays ship buttons to build spaceships:
    Main functionalities:
    The SpaceHarbor class is responsible for displaying ship buttons to build spaceships. It creates a surface with
    three buttons for building spaceships, and sets their properties such as image, tooltip, and info text. It also
    handles the visibility of the buttons based on whether the selected planet has a space harbor building or not.
    When a button is clicked, it checks if the player has enough resources to build the spaceship, and if so, it
    deducts the resources from the player and creates a BuildingWidget to represent the spaceship being built.

    Methods:
    - __init__: initializes the SpaceHarbor object by setting its properties such as surface, buttons, and visibility.
    - set_info_text: sets the info text of the parent info panel to the info text of the SpaceHarbor object.
    - set_visible: determines whether the SpaceHarbor object should be visible based on whether the selected planet has
      a space harbor building or not.
    - listen: listens for events, but does not do anything.
    - draw: draws the SpaceHarbor object on the screen, including its surface, label, and buttons.
    - build_ship: builds the spaceship when a button is clicked, deducting the resources from the player and creating a
      BuildingWidget to represent the spaceship being built.

    Fields:
    - parent: the parent object of the SpaceHarbor object.
    - frame_color: the color of the frame of the SpaceHarbor object.
    - surface: the surface of the SpaceHarbor object.
    - surface_rect: the rectangle of the surface of the SpaceHarbor object.
    - spacing: the spacing between the buttons of the SpaceHarbor object.
    - font: the font used for the label of the SpaceHarbor object.
    - info_text: the info text of the SpaceHarbor object.
    - spacehunter_button: the button for building a spacehunter spaceship.
    - cargoloader_button: the button for building a cargoloader spaceship.
    - spaceship_button: the button for building a spaceship.
    - surface_frame: the frame of the surface of the SpaceHarbor object.
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.parent = kwargs.get("parent", None)
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.set_alpha(global_params.ui_panel_alpha)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.world_y
        self.spacing = self.parent.spacing

        # text
        self.font_size = kwargs.get("font_size", 12)
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.info_text = kwargs.get("infotext")

        # buttons
        self.spacehunter_button = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.get_screen_y(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("spacehunter_30x30.png"), (25, 25)),
            tooltip="build spacehunter",
            info_text=info_panel_text_generator.create_info_panel_ship_text("spacehunter"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: building_factory.build("spacehunter"),
            )

        self.cargoloader_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() / 2,
            y=self.get_screen_y(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("cargoloader_30x30.png"), (25, 25)),
            tooltip="build cargoloader",
            info_text=info_panel_text_generator.create_info_panel_ship_text("cargoloader"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: building_factory.build("cargoloader"),
            )

        self.spaceship_button = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width(),
            y=self.get_screen_y(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("spaceship_30x30.png"), (25, 25)),
            tooltip="build spaceship",
            info_text=info_panel_text_generator.create_info_panel_ship_text("spaceship"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: building_factory.build("spaceship"),
            )

        # initial hide the buttons
        self.parent.widgets.append(self)
        self.hide_buttons()

    def set_visible(self):
        if not self.parent.parent.selected_planet:
            visible = False
            return visible

        if "space harbor" in self.parent.parent.selected_planet.buildings:
            self.show_buttons()
            self.parent.parent.building_panel.max_height += self.parent.sub_widget_height
            visible = True
        else:
            self.hide_buttons()
            visible = False

        return visible

    def hide_buttons(self):
        self.spaceship_button.hide()
        self.cargoloader_button.hide()
        self.spacehunter_button.hide()

    def show_buttons(self):
        self.spaceship_button.show()
        self.cargoloader_button.show()
        self.spacehunter_button.show()

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
        self.win.blit(self.surface, self.surface_rect)
        pygame.draw.rect(self.win, self.frame_color, self.surface_rect, int(ui_rounded_corner_small_thickness), int(global_params.ui_rounded_corner_radius_small))


        # label
        drawText(self.win, "Space Harbor", self.frame_color,
            (self.surface_rect.x + self.parent.spacing_x - 36, self.surface_rect.y + self.spacing,
             self.get_screen_width(),
             20), self.font, "center")

        self.spacehunter_button.set_position((
            self.surface_rect.x + self.spacing * 3, self.surface_rect.y + self.spacing + 20))

        self.spaceship_button.set_position((
            self.surface_rect.x + self.get_screen_width() / 2 - self.spaceship_button.get_screen_width() / 2,
            self.surface_rect.y + self.spacing + 20))

        self.cargoloader_button.set_position((
            self.surface_rect.x + self.get_screen_width() - self.cargoloader_button.get_screen_width() - self.spacing * 3,
            self.surface_rect.y + self.spacing + 20))
