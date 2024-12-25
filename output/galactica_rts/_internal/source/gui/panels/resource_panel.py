import pygame

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.Icon import Icon
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.garbage_handler import garbage_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image
from source.text.info_panel_text_generator import info_panel_text_generator


class ResourcePanel(WidgetBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
        self.app = kwargs.get("app")
        self.name = "resource panel"
        self.anchor_right = kwargs.get("anchor_right")
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.frame_color = colors.frame_color

        # remove this later

        self.clock_font = pygame.font.SysFont(config.font_name, 12)

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

        self.icons = []
        self.create_icons()

        # toggle switch to pop in or out
        self.toggle_switch = ToggleSwitch(self, 15)
        self.init = 0

    def create_icons(self):
        """
        creates the icons used for displaying the resources on top of the screen
        """
        pos_x = 160
        pos_y = 15
        resources = building_factory.get_resource_categories()
        resource_texts = {
            "water": "water is good to drink and for washing as well",
            "energy": "energy is needed for almost everything",
            "food": "this is food, you want to eat!!! Don't you?!??",
            "minerals": "some of the minerals look really nice in the sun!",
            "technology": "technology is bad! but we need some things to build and evolve technology",
            "population": "population; produce food and water to make it grow!"
            }

        for resource in resources:
            setattr(self, f"{resource}_icon", Icon(win=self.win,
                    x=pos_x,
                    y=pos_y,
                    width=self.icon_size,
                    height=self.icon_size,
                    is_sub_widget=False,
                    parent=self.parent,
                    image=get_image(f"{resource}_25x25.png"),
                    key=resource,
                    tooltip=resource_texts[resource],
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=False,
                    layer=9,
                    outline_thickness=1,
                    outline_threshold=0,
                    clickable=True,
                    on_click=lambda resource_=resource: self.parent.cheat_resource(resource_, 1000, player_index=0)))

            self.widgets.append(getattr(self, f"{resource}_icon"))
            self.max_width += self.icon_size + self.spacing
            pos_x += self.spacing

    def set_info_text(self):
        self.app.info_panel.set_text(info_panel_text_generator.info_text)

    def reposition(self):
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.max_width = self.app.settings_panel.surface_rect.left  # - self.app.info_panel.surface_rect.right
        self.surface_rect.width = self.max_width
        self.surface_rect.left = self.app.info_panel.surface_rect.left

        self.reposition_widgets()
        self.toggle_switch.reposition()

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.x = (self.surface_rect.x + self.spacing) + (self.icon_size + self.spacing) * self.widgets.index(icon)

    def draw(self):
        """draws the ui elements"""
        if not self.init:
            self.reposition()
            self.init = 1

        if self._hidden:
            return

        self.draw_frame()

        # fps, memory usage, this just for debug purposes
        # self.clock.tick(int(config.fps))
        # fps = f"fps: {str(self.clock.get_fps())}"  # , {sprite_groups.__str__()} hover:{config.hover_object}"
        fps = f"fps: {str(round(time_handler.fps, 1))}, memory usage: {garbage_handler.get_memory_usage()} MB"
        caption = f"GalacticaRTS: FPS: {round(time_handler.fps, 1)},memory usage: {garbage_handler.get_memory_usage()} MB,  ip: {config.app.game_client.ip}, client_id: {config.app.game_client.id}, is_host: {config.app.game_client.is_host}"
        # fps = f"fps: {str(self.clock.get_fps())}, {sprite_groups.__str__()} hover:{config.hover_object}"
        text = self.clock_font.render(caption, 0, self.frame_color)
        self.win.blit(text, (0, 0, 30, 30))
