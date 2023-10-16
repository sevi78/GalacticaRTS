import logging
import pygame
from pygame_widgets.util import drawText

from source.app.app_helper import check_if_enough_resources_to_build
from source.configuration.config import planetary_defence_prices
from source.configuration.info_text import create_info_panel_building_text, create_info_panel_planetary_defence_text
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.building_widget import BuildingWidget
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds

FONT_SIZE = 12

# Constants
ICON_SIZE = 25
BUTTON_SIZE = 25

class PlanetaryDefenceWidget(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.name = "Planetary Defence"
        self.icon_size = kwargs.get("icon_size", ICON_SIZE)
        self.parent = kwargs.get("parent", None)
        self.frame_color = colors.frame_color
        self.width = width
        self.height = height

        self._initialize_surface()
        self._initialize_text(kwargs)
        self._initialize_buttons()

        self.hide_buttons()

    def _initialize_surface(self):
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.world_y
        self.spacing = self.parent.spacing
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)

    def _initialize_text(self, kwargs):
        self.font_size = kwargs.get("font_size", FONT_SIZE)
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.info_text = kwargs.get("infotext")

    def _initialize_buttons(self):
        self.buttons = []
        self.cannon_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("cannon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
            tooltip="build cannon",
            info_text= create_info_panel_planetary_defence_text("cannon"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.build("cannon"))

        self.missile_launcher_icon = ImageButton(win=self.win,
            x=self.get_screen_x() + BUTTON_SIZE + 10,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("missile.png"), (BUTTON_SIZE, BUTTON_SIZE)),
            tooltip="build missile launcher",
            info_text=create_info_panel_planetary_defence_text("missile"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.build("missile"))

        self.parent.widgets.append(self)
        self.buttons.append(self.cannon_icon)
        self.buttons.append(self.missile_launcher_icon)

    def set_visible(self):
        if not self.parent.parent.selected_planet:
            visible = False
            return visible

        if "particle accelerator" in self.parent.parent.selected_planet.buildings:
            self.show_buttons()
            self.parent.parent.building_panel.max_height += self.parent.sub_widget_height
            visible = True
        else:
            self.hide_buttons()
            visible = False

        return visible

    def hide_buttons(self):
        for button in self.buttons:
            button.hide()

    def show_buttons(self):
        for button in self.buttons:
            button.show()

    def draw(self):
        if not self.set_visible():
            return

        if self._hidden:
            self.hide_buttons()
            return
        else:
            self.show_buttons()

        self._draw_frame()
        self._draw_label()
        self._draw_buttons()

    def _draw_frame(self):
        self.surface_rect.x = self.parent.surface_rect.x
        self.surface_rect.y = self.parent.world_y + self.spacing + 5

        if "space harbor" in self.parent.parent.selected_planet.buildings:
            self.surface_rect.y = self.parent.world_y + self.parent.sub_widget_height + self.spacing + 5

        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.win.blit(self.surface, self.surface_frame)

    def _draw_label(self):
        drawText(self.win, self.name, self.frame_color,
            (self.surface_rect.x + self.parent.spacing_x - 36, self.surface_rect.y + self.spacing,
             self.get_screen_width(),
             20), self.font, "center")

    def _draw_buttons(self):
        self.cannon_icon.set_position((self.surface_rect.x + self.spacing * 3, self.surface_rect.y + self.spacing + 20))
        self.missile_launcher_icon.set_position((
        self.surface_rect.x + BUTTON_SIZE + 10 + self.spacing * 3, self.surface_rect.y + self.spacing + 20))

    def build(self, obj):
        price = planetary_defence_prices[obj]
        player = self.parent.parent.player
        app = self.parent.parent
        planet = app.selected_planet

        if check_if_enough_resources_to_build(obj):
            # pay
            for key, value in price.items():
                setattr(player, key, getattr(player, key) - value)

            # building widget
            widget_width = self.parent.get_screen_width()
            widget_height = 35
            spacing = 5

            win = pygame.display.get_surface()
            height = win.get_height()
            y = height - spacing - widget_height - widget_height * len(app.building_widget_list)

            sounds.play_sound(sounds.bleep2, channel=7)

            building_widget = BuildingWidget(win=app.win,
                x=app.building_panel.screen_x,
                y=y,
                width=widget_width,
                height=widget_height,
                name=obj,
                fontsize=18,
                progress_time=5,
                parent=app,
                key="",
                value=0,
                planet=app.selected_planet,
                tooltip=obj, layer=4
                )

            planet.building_cue += 1

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
