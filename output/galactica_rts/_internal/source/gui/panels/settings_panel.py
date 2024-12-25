import pygame

from source.configuration.game_config import config
from source.game_play.navigation import navigate_to
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.buttons.image_button import ImageButton, Delegate
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image, overblit_button_image
from source.text.info_panel_text_generator import info_panel_text_generator


class SettingsPanel(WidgetBase):
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
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)
        self.font_size = 18
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # icons
        self.chat_icon = None
        self.settings_icon = None
        self.autopilot_icon = None
        self.info_icon = None
        self.spacehunter_icon = None
        self.planets_icon = None
        self.ships_icon = None
        self.add_deal_icon = None
        self.deal_manager_icon = None
        self.save_game_icon = None
        self.mission_icon = None
        self.players_icon = None
        self.view_icon = None
        self.server_icon = None
        self.orbit_icon = None

        self.create_icons()

        # toggle switch to pop in or out
        self.toggle_switch = ToggleSwitch(self, 15)
        self.init = 0

    def create_icons(self):
        # self.economy_overview_icon = ImageButton(win=self.win,
        #     x=self.get_screen_x(),
        #     y=self.surface_rect.y + self.spacing,
        #     width=self.icon_size,
        #     height=self.icon_size,
        #     is_sub_widget=False,
        #     parent=self,
        #     image=pygame.transform.scale(
        #         get_image("economy_icon.png"), (25, 25)),
        #     tooltip="navigate to this ship",
        #     frame_color=self.frame_color,
        #     moveable=False,
        #     include_text=True, layer=self.layer,
        #     on_click=lambda: config.app.economy_overview.set_visible())
        # self.widgets.append(self.economy_overview_icon)
        # self.max_width += self.icon_size + self.spacing

        self.chat_icon = ImageButton(
                win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("chat_icon.png"), (25, 25)),
                tooltip="chat",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                name="chat_icon",
                on_click=lambda: config.app.chat_edit.set_visible())

        self.widgets.append(self.chat_icon)
        self.max_width += self.icon_size + self.spacing

        self.server_icon = ImageButton(
                win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("server_icon.png"), (25, 25)),
                tooltip="server settings",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                name="server_icon",
                on_click=lambda: config.app.client_edit.set_visible(),
                delegate=Delegate("check.png"))

        self.widgets.append(self.server_icon)
        self.max_width += self.icon_size + self.spacing

        self.view_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("view_icon.png"), (25, 25)),
                image_raw=get_image("view_icon.png"),
                tooltip="view",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                key="",
                info_text="",
                name="view_icon",
                text_color=(0, 0, 0),
                font_size=0,
                outline_thickness=0,
                outline_threshold=0,
                on_click=lambda: config.app.view_panel.set_visible())

        self.widgets.append(self.view_icon)
        self.max_width += self.icon_size + self.spacing

        self.players_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("multiplayer.png"), (25, 25)),
                image_raw=get_image("multiplayer.png"),
                tooltip="players",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                key="",
                info_text="",
                name="players_icon",
                text_color=(0, 0, 0),
                font_size=0,
                outline_thickness=0,
                outline_threshold=0,
                on_click=lambda: config.app.player_edit.set_visible())

        self.widgets.append(self.players_icon)
        self.max_width += self.icon_size + self.spacing

        self.mission_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
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
                text_color=(0, 0, 0),
                font_size=0,
                outline_thickness=0,
                outline_threshold=0)

        self.widgets.append(self.mission_icon)
        self.max_width += self.icon_size + self.spacing

        self.save_game_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
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
                text_color=(0, 0, 0),
                font_size=0,
                on_click=lambda: config.app.save_game_edit.set_visible(),
                outline_thickness=1,
                outline_threshold=127)

        self.widgets.append(self.save_game_icon)
        self.max_width += self.icon_size + self.spacing

        self.deal_manager_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
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
                text_color=(0, 0, 0),
                font_size=0,
                on_click=lambda: config.app.deal_container.set_visible(),
                outline_thickness=1,
                outline_threshold=127)

        self.widgets.append(self.deal_manager_icon)
        self.max_width += self.icon_size + self.spacing

        self.add_deal_icon = ImageButton(win=self.win,
                x=self.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("add_deal_icon.png"), (25, 25)),
                image_raw=get_image("deal_icon.png"),
                tooltip="add deal",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                key="",
                name="add_deal_icon",
                text_color=(0, 0, 0),
                font_size=0,
                on_click=lambda: config.app.add_deal_edit.set_visible(),
                outline_thickness=1,
                outline_threshold=127)

        self.widgets.append(self.add_deal_icon)
        self.max_width += self.icon_size + self.spacing

        self.ships_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("ship_container_icon.png"), (25, 25)),
                tooltip="ship select",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.ship_container.set_visible())
        self.widgets.append(self.ships_icon)
        self.max_width += self.icon_size + self.spacing

        self.planets_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("planet_container_icon.png"), (25, 25)),
                tooltip="planet select",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.planet_container.set_visible())

        self.widgets.append(self.planets_icon)
        self.max_width += self.icon_size + self.spacing

        # ship icon
        self.spacehunter_icon = ImageButton(win=self.win,
                x=self.get_screen_x(),
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("spacehunter.png"), (25, 25)),
                tooltip="navigate to this ship",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: navigate_to(None, ship="spacehunter"))
        self.widgets.append(self.spacehunter_icon)
        self.max_width += self.icon_size + self.spacing

        self.info_icon = ImageButton(win=self.win,
                x=self.spacehunter_icon.get_screen_x() + 25,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("info_30x30.png"), (25, 25)),
                tooltip="information about game controls",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: self.set_info_text())
        self.widgets.append(self.info_icon)
        self.max_width += self.icon_size + self.spacing

        # self.planet_editor_icon = ImageButton(win=self.win,
        #     x=self.info_icon.get_screen_x() - 50,
        #     y=self.surface_rect.y + self.spacing,
        #     width=self.icon_size,
        #     height=self.icon_size,
        #     is_sub_widget=False,
        #     parent=self,
        #     image=pygame.transform.scale(
        #         get_image("Zeta Bentauri_60x60.png"), (25, 25)),
        #     tooltip="open planet editor",
        #     frame_color=self.frame_color,
        #     moveable=False,
        #     include_text=True, layer=self.layer,
        #     on_click=lambda: planet_editor.main(surface=self.win))
        # self.widgets.append(self.planet_editor_icon)
        # self.max_width += self.icon_size + self.spacing

        self.autopilot_icon = ImageButton(win=self.win,
                x=self.info_icon.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(
                        get_image("autopilot.png"), (25, 25)),
                tooltip="enable autopilot",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: self.enebale_autopilot(self.autopilot_icon))

        self.widgets.append(self.autopilot_icon)
        self.max_width += self.icon_size + self.spacing

        # settings icon
        self.settings_icon = ImageButton(win=self.win,
                x=self.info_icon.get_screen_x() - 50,
                y=self.surface_rect.y + self.spacing,
                width=self.icon_size,
                height=self.icon_size,
                is_sub_widget=False,
                parent=self,
                image=pygame.transform.scale(get_image("settings_40x40.png"), (25, 25)),
                tooltip="open advanced settings panel",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True, layer=self.layer,
                on_click=lambda: config.app.advanced_settings_panel.set_visible())  # settings.main(surface=self.win))

        self.widgets.append(self.settings_icon)
        self.max_width += self.icon_size + self.spacing + self.spacing

    def enebale_autopilot(self, button):
        value = False
        for i in sprite_groups.ships.sprites():
            i.autopilot = not i.autopilot
            value = i.autopilot

        config.enable_autopilot = value
        overblit_button_image(button, "uncheck.png", value)

    def set_info_text(self):
        config.app.info_panel.set_text(info_panel_text_generator.info_text)
        config.app.info_panel.set_planet_image(get_image("info_30x30.png"), size=(
            50, 50), alpha=78, align="center")

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()
        self.max_height = self.get_screen_y() + self.surface_rect.height

        # reposition
        self.surface_rect.width = self.max_width
        self.surface_rect.x = width - config.app.building_panel.surface.get_width() - self.max_width
        self.reposition_widgets()
        self.toggle_switch.reposition()

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.screen_x = ((self.surface_rect.x + self.spacing)
                             + (self.icon_size + self.spacing) * self.widgets.index(icon))

    def draw(self):
        """
        draws the ui elements
        """
        if not self.init:
            self.reposition()
            self.init = 1

        if self._hidden:
            return

        self.draw_frame()

        # TODO: fix this, shluc be on another place, somewher at inbitialize
        if not config.app.game_client.is_host:
            self.settings_icon.disable()
            self.save_game_icon.disable()
        else:
            self.settings_icon.enable()
            self.save_game_icon.enable()
