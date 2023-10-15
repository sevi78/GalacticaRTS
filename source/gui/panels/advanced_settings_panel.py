import pygame

from source.configuration import config
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image


class AdvancedSettingsPanel(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.name = "settings panel"
        self.anchor_right = kwargs.get("anchor_right")
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.frame_color = colors.frame_color

        # construct surface
        self.icon_size = kwargs.get("icon_size", 25)
        self.max_width = 0
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.font_size = 18
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.max_height = self.get_screen_y() + self.surface_rect.height

        self.create_icons()

        # toggle switch to pop in or out
        self.toggle_switch = ToggleSwitch(self, 15)
        self.init = 0

    def create_icons(self):
        # event panel edit icon
        self.event_panel_edit_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("game_play_icon.png"), (25, 25)),
            tooltip="open event panel edit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.game_play_edit.set_visible())
        self.widgets.append(self.event_panel_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # debug edit icon
        self.debug_edit_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("debug_icon.png"), (25, 25)),
            tooltip="open debug edit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.debug_edit.set_visible())
        self.widgets.append(self.debug_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # enemy edit icon
        self.enemy_handler_edit_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("gameplay_settings_icon.png"), (25, 25)),
            tooltip="open enemy handler edit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.enemy_handler_edit.set_visible())
        self.widgets.append(self.enemy_handler_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # planet edit icon
        self.planet_edit_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("planet_edit.png"), (25, 25)),
            tooltip="open planet edit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.planet_edit.set_visible())
        self.widgets.append(self.planet_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # ship icon
        self.ship_edit_icon = ImageButton(win=self.win,
            x=self.planet_edit_icon.get_screen_x() + 25,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("ship_edit.png"), (25, 25)),
            tooltip="open ship edit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.ship_edit.set_visible())
        self.widgets.append(self.ship_edit_icon)
        self.max_width += self.icon_size + self.spacing

        self.font_edit_icon = ImageButton(win=self.win,
            x=self.ship_edit_icon.get_screen_x() + 25,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("font_icon.png"), (25, 25)),
            tooltip="open font select",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: global_params.app.font_edit.set_visible())
        self.widgets.append(self.font_edit_icon)

        self.max_width += self.icon_size + self.spacing + self.spacing

    def set_info_text(self):
        global_params.app.info_panel.set_text(config.info_text)

    def draw_frame(self):
        # # frame
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.win.blit(self.surface, self.surface_frame)

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.surface_rect.width = self.max_width
        self.surface_rect.x = width - global_params.app.building_panel.surface_rect.width - global_params.app.settings_panel.surface_rect.width - self.max_width

        self.reposition_widgets()
        self.toggle_switch.reposition()

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.screen_x = (self.surface_rect.x + self.spacing) + (
                        self.icon_size + self.spacing) * self.widgets.index(icon)

    def listen_(self, events):
        pass

    def draw(self):
        """draws the ui elements"""
        if not self.init:
            self.reposition()
            self.init = 1

        if self._hidden:
            return

        self.draw_frame()
