import pygame

from source.configuration.game_config import config
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image, overblit_button_image, scale_image_cached
from source.text.info_panel_text_generator import info_panel_text_generator


class ViewPanel(WidgetBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)

        self.name = "view panel"
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

        # icons
        self.show_ship_state_icon = None
        self.show_universe_icon = None
        self.buttons_icon = None
        self.map_icon = None
        self.show_event_text_icon = None
        self.show_tooltip_icon = None
        self.show_planet_names_icon = None
        self.orbit_icon = None
        self.cross_icon = None
        self.view_explored_planets_icon = None
        self.player_colors_icon = None

        self.create_icons()

        self.init = 0
        self.hide()

    def create_icons(self):
        self.show_universe_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("level_10.png"), (25, 25)),
                tooltip="show universe",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_universe", True, button=self.show_universe_icon))

        self.widgets.append(self.show_universe_icon)
        self.max_width += self.icon_size + self.spacing

        self.show_ship_state_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("state_icon.png"), (25, 25)),
                tooltip="show ship states",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_ship_state", True, button=self.show_ship_state_icon))

        self.widgets.append(self.show_ship_state_icon)
        self.max_width += self.icon_size + self.spacing

        self.view_explored_planets_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("view_explored_planets_icon.png"), (25, 25)),
                tooltip="show explored planets",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("view_explored_planets", True, button=self.view_explored_planets_icon))

        self.widgets.append(self.view_explored_planets_icon)
        self.max_width += self.icon_size + self.spacing

        self.cross_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("cross.png"), (25, 25)),
                tooltip="show cross",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("enable_cross", True, button=self.cross_icon))
        self.widgets.append(self.cross_icon)
        self.max_width += self.icon_size + self.spacing

        self.orbit_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("orbit_icon.png"), (25, 25)),
                tooltip="show orbit",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_orbit", True, button=self.orbit_icon))
        self.widgets.append(self.orbit_icon)
        self.max_width += self.icon_size + self.spacing

        self.show_planet_names_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("planet_text_icon.png"), (25, 25)),
                tooltip="show planet names",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: self.show_planet_names(button=self.show_planet_names_icon))
        self.widgets.append(self.show_planet_names_icon)
        self.max_width += self.icon_size + self.spacing

        self.show_tooltip_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("text_icon.png"), (25, 25)),
                tooltip="show tooltips",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: self.show_tooltip(button=self.show_tooltip_icon))

        self.widgets.append(self.show_tooltip_icon)
        self.max_width += self.icon_size + self.spacing

        self.show_event_text_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("text_icon.png"), (25, 25)),
                tooltip="show event text",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: self.show_event_text(button=self.show_event_text_icon))

        self.widgets.append(self.show_event_text_icon)
        self.max_width += self.icon_size + self.spacing

        self.map_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("map_icon.png"), (25, 25)),
                tooltip="show map",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_map_panel", True, button=self.map_icon))
        self.widgets.append(self.map_icon)
        self.max_width += self.icon_size + self.spacing

        self.buttons_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("smile.png"), (25, 25)),
                tooltip="show planet overview",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_overview_buttons", True, button=self.buttons_icon))
        self.widgets.append(self.buttons_icon)
        self.max_width += self.icon_size + self.spacing

        self.player_colors_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("color_icon.png"), (25, 25)),
                tooltip="show player colors",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.set_global_variable("show_player_colors", True, button=self.player_colors_icon))

        self.widgets.append(self.player_colors_icon)
        self.max_width += self.icon_size + self.spacing + self.spacing

    def show_planet_names(self, button):
        value = False
        for i in sprite_groups.planets.sprites():
            i.show_text = not i.show_text
            value = i.show_text

        overblit_button_image(button, "uncheck.png", value)

    def show_tooltip(self, button):
        config.app.tooltip_instance.active = not config.app.tooltip_instance.active
        overblit_button_image(button, "uncheck.png", config.app.tooltip_instance.active)

    def show_event_text(self, button):
        config.ui_event_text_visible = not config.ui_event_text_visible
        overblit_button_image(button, "uncheck.png", config.ui_event_text_visible)

    def set_info_text(self):
        config.app.info_panel.set_text(info_panel_text_generator.info_text)

    def reposition(self):
        win = pygame.display.get_surface()
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.surface_rect.width = self.max_width
        self.surface_rect.x = config.app.advanced_settings_panel.surface_rect.left - self.surface_rect.width
        self.reposition_widgets()

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
