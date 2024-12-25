import pygame

from source.configuration.game_config import config
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.multimedia_library.images import get_image, scale_image_cached
from source.text.info_panel_text_generator import info_panel_text_generator


class AdvancedSettingsPanel(WidgetBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
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
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect,
                config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)
        self.font_size = 18
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.max_height = self.get_screen_y() + self.surface_rect.height

        self.create_icons()

        # toggle switch to pop in or out
        # self.toggle_switch = ToggleSwitch(self, 15)
        self.init = 0
        self.hide()

    def create_icons(self):
        # level select
        self.auto_economy_queue_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("autopilot.png"), (25, 25)),
                tooltip="open auto economy edit queue edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.auto_economy_calculator_edit.set_visible())
        self.widgets.append(self.auto_economy_queue_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # level select
        self.level_select_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("level_icon.png"), (25, 25)),
                tooltip="open level select",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.level_select.set_visible())
        self.widgets.append(self.level_select_icon)
        self.max_width += self.icon_size + self.spacing

        # level edit
        self.level_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("level_edit_icon.png"), (25, 25)),
                tooltip="open level edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.level_edit.set_visible())
        self.widgets.append(self.level_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # planet edit icon
        self.planet_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("planet_edit.png"), (25, 25)),
                tooltip="open planet edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.planet_edit.set_visible())
        self.widgets.append(self.planet_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # event panel edit icon
        self.building_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("building_icon.png"), (25, 25)),
                tooltip="open building edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.building_edit.set_visible())
        self.widgets.append(self.building_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # debug edit icon
        self.debug_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("debug_icon.png"), (25, 25)),
                tooltip="open debug edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.debug_edit.set_visible())
        self.widgets.append(self.debug_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # enemy edit icon
        self.enemy_handler_edit_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("gameplay_settings_icon.png"), (25, 25)),
                tooltip="open enemy handler edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.enemy_handler_edit.set_visible())
        self.widgets.append(self.enemy_handler_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # ship icon
        self.ship_edit_icon = ImageButton(win=self.win,
                x=self.planet_edit_icon.get_screen_x() + 25,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("ship_edit.png"), (25, 25)),
                tooltip="open ship edit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.ship_edit.set_visible())
        self.widgets.append(self.ship_edit_icon)
        self.max_width += self.icon_size + self.spacing

        # settings icon
        self.settings_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("settings_40x40.png"), (25, 25)),
                tooltip="open settings menu",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.settings_edit.set_visible())  # settings.main(surface=self.win))
        self.widgets.append(self.settings_icon)
        self.max_width += self.icon_size + self.spacing + self.spacing

    def set_info_text(self):
        config.app.info_panel.set_text(info_panel_text_generator.info_text)

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.surface_rect.width = self.max_width
        # self.surface_rect.x = width - config.app.building_panel.surface_rect.width - config.app.settings_panel.surface_rect.width - self.max_width
        self.surface_rect.x = config.app.settings_panel.surface_rect.right - self.surface_rect.width
        self.reposition_widgets()
        # self.toggle_switch.reposition()

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.screen_x = (self.surface_rect.x + self.spacing) + (
                    self.icon_size + self.spacing) * self.widgets.index(icon)

    def draw(self):
        """draws the ui elements"""
        if not self.init:
            self.reposition()
            self.init = 1

        if self._hidden:
            return

        self.draw_frame()
