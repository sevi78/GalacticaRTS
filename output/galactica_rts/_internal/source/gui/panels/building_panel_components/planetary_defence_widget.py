import pygame
from pygame_widgets.util import drawText

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, scale_image_cached
from source.text.info_panel_text_generator import info_panel_text_generator

# Constants
FONT_SIZE = 12
ICON_SIZE = 25
BUTTON_SIZE = 25


class PlanetaryDefenceWidget(WidgetBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
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
        self.surface.set_alpha(config.ui_panel_alpha)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.world_y
        self.spacing = self.parent.spacing

    def _initialize_text(self, kwargs):
        self.font_size = kwargs.get("font_size", FONT_SIZE)
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.info_text = kwargs.get("infotext")

    def _initialize_buttons(self):
        self.buttons = []
        self.cannon_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("cannon.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="build cannon",
                info_text=info_panel_text_generator.create_info_panel_planetary_defence_text("cannon"),
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: building_factory.build("cannon", config.app.selected_planet))

        self.missile_launcher_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE + 10,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("missile.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="build missile launcher",
                info_text=info_panel_text_generator.create_info_panel_planetary_defence_text("missile"),
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: building_factory.build("missile", config.app.selected_planet))

        self.energy_blast_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE * 2 + 10,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("energy blast.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="build energy blaster",
                info_text=info_panel_text_generator.create_info_panel_planetary_defence_text("energy blast"),
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: building_factory.build("energy blast", config.app.selected_planet))

        self.electro_magnetic_impulse_icon = ImageButton(win=self.win,
                x=self.get_screen_x() + BUTTON_SIZE * 3 + 10,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("electro magnetic impulse.png"), (BUTTON_SIZE, BUTTON_SIZE)),
                tooltip="build electro magnetic impulse(E.M.P.)",
                info_text=info_panel_text_generator.create_info_panel_planetary_defence_text("electro magnetic impulse"),
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: building_factory.build("electro magnetic impulse", config.app.selected_planet))

        self.parent.widgets.append(self)
        self.buttons.append(self.cannon_icon)
        self.buttons.append(self.missile_launcher_icon)
        self.buttons.append(self.energy_blast_icon)
        self.buttons.append(self.electro_magnetic_impulse_icon)

    def set_visible(self):
        if not self.parent.parent.selected_planet:
            visible = False
            return visible

        if "particle accelerator" in self.parent.parent.selected_planet.economy_agent.buildings:
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

        if "space harbor" in self.parent.parent.selected_planet.economy_agent.buildings:
            self.surface_rect.y = self.parent.world_y + self.parent.sub_widget_height + self.spacing + 5

        self.win.blit(self.surface, self.surface_rect)
        pygame.draw.rect(self.win, self.frame_color, self.surface_rect, config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)

    def _draw_label(self):
        drawText(self.win, self.name, self.frame_color,
                (self.surface_rect.x + self.parent.spacing_x - 36, self.surface_rect.y + self.spacing,
                 self.get_screen_width(),
                 20), self.font, "center")

    def _draw_buttons(self):
        for i in self.buttons:
            i.set_position((self.surface_rect.x + BUTTON_SIZE * self.buttons.index(i) + self.spacing * 3,
                            self.surface_rect.y + self.spacing + 20))

# # Logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
