import pygame

from source.configuration.game_config import config
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.Icon import Icon
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.garbage_handler import garbage_handler
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image
from source.text.info_panel_text_generator import info_panel_text_generator


class ResourcePanel(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
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
        start_x = 200
        spacing = 150
        pos_x = 160
        pos_y = 15

        self.players_icon = ImageButton(win=self.win,
            x=70,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("multiplayer.png"), (25, 25)),
            image_raw=get_image("multiplayer.png"),
            tooltip="players",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            key="",
            info_text="players",
            name="players_icon",
            textColours=(0, 0, 0),
            font_size=0,
            outline_thickness=0,
            outline_threshold=0,
            onClick=lambda: config.app.player_edit.set_visible())

        self.widgets.append(self.players_icon)

        self.mission_icon = ImageButton(win=self.win,
            x=5,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("mission_512x512.png"), (25, 25)),
            image_raw=get_image("mission_512x512.png"),
            tooltip="this is your mission",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            key="",
            info_text="mission",
            name="mission_icon",
            textColours=(0, 0, 0),
            font_size=0,
            outline_thickness=0,
            outline_threshold=0)

        self.widgets.append(self.mission_icon)

        self.save_game_icon = ImageButton(win=self.win,
            x=35,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("save_icon_bk.png"), (25, 25)),
            image_raw=get_image("save_icon_bk.png"),
            tooltip="save game",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            key="",
            name="save_game_icon",
            textColours=(0, 0, 0),
            font_size=0,
            onClick=lambda: config.app.save_game_edit.set_visible(),
            outline_thickness=1,
            outline_threshold=127)

        self.widgets.append(self.save_game_icon)

        self.deal_manager_icon = ImageButton(win=self.win,
            x=100,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("deal_icon.png"), (25, 25)),
            image_raw=get_image("deal_icon.png"),
            tooltip="open deal manager",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            key="",
            name="deal_manager_icon",
            textColours=(0, 0, 0),
            font_size=0,
            onClick=lambda: config.app.deal_manager.set_visible(),
            outline_thickness=1,
            outline_threshold=127)

        self.widgets.append(self.deal_manager_icon)
        # self.max_width += self.icon_size + self.spacing
        # pos_x += self.spacing

        self.water_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("water_25x25.png"),
            key="water",
            tooltip="water is good to drink and for washing aswell",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0)
        self.widgets.append(self.water_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

        self.energy_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("energy_25x25.png"),
            key="energy",
            tooltip="energy is needed for almost everything",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0)
        self.widgets.append(self.energy_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

        self.food_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("food_25x25.png"),
            key="food",
            tooltip="this is food, you want to eat!!! Don't you?!??",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0)
        self.widgets.append(self.food_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

        self.minerals_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("minerals_25x25.png"),
            key="minerals",
            tooltip="some of the minerals look really nice in the sun!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0,)
        self.widgets.append(self.minerals_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

        self.technology_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("technology_25x25.png"),
            key="technology",
            tooltip="technology is bad! but we need some things to build and evolve technology",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0)
        self.widgets.append(self.technology_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

        self.population_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self.parent,
            image=get_image("population_25x25.png"),
            key="population",
            tooltip="population; produce food and water to make it grow!",
            frame_color=self.frame_color,
            moveable=False,
            include_text=False,
            layer=9,
            outline_thickness=1,
            outline_threshold=0)
        self.widgets.append(self.population_icon)
        self.max_width += self.icon_size + self.spacing
        pos_x += self.spacing

    def set_info_text(self):
        self.app.info_panel.set_text(info_panel_text_generator.info_text)

    def reposition(self):
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.max_width = self.app.advanced_settings_panel.surface_rect.left  # - self.app.info_panel.surface_rect.right
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
        # fps = f"fps: {str(self.clock.get_fps())}, {sprite_groups.__str__()} hover:{config.hover_object}"
        text = self.clock_font.render(fps, 0, self.frame_color)
        self.win.blit(text, (0, 0, 30, 30))
