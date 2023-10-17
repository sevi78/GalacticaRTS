import pygame

from source.configuration import config
from source.editors import planet_editor, building_editor, settings
from source.game_play.navigation import navigate_to
from source.gui.panels.toggle_switch import ToggleSwitch
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.image_button import ImageButton
from source.utils import global_params
from source.utils.colors import colors
from source.utils.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image


class SettingsPanel(WidgetBase):
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
        # settings icon
        self.settings_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("settings_40x40.png"), (25, 25)),
            tooltip="open settings menu",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: settings.main(surface=self.win))
        self.widgets.append(self.settings_icon)
        self.max_width += self.icon_size + self.spacing

        # ship icon
        self.spacehunter_icon = ImageButton(win=self.win,
            x=self.settings_icon.get_screen_x() + 25,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("spacehunter_30x30.png"), (25, 25)),
            tooltip="navigate to this ship",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: navigate_to(None, ship="spacehunter"))
        self.widgets.append(self.spacehunter_icon)
        self.max_width += self.icon_size + self.spacing

        self.info_icon = ImageButton(win=self.win,
            x=self.spacehunter_icon.get_screen_x() + 25,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("info_30x30.png"), (25, 25)),
            tooltip="information about game controls",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_info_text())
        self.widgets.append(self.info_icon)
        self.max_width += self.icon_size + self.spacing

        self.planet_editor_icon = ImageButton(win=self.win,
            x=self.info_icon.get_screen_x() - 50,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("Zeta Bentauri_60x60.png"), (25, 25)),
            tooltip="open planet editor",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: planet_editor.main(surface=self.win))
        self.widgets.append(self.planet_editor_icon)
        self.max_width += self.icon_size + self.spacing

        self.building_editor_icon = ImageButton(win=self.win,
            x=self.planet_editor_icon.get_screen_x() - 50,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("building_icon.png"), (25, 25)),
            tooltip="open building editor",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: building_editor.main(surface=self.win))
        self.widgets.append(self.building_editor_icon)
        self.max_width += self.icon_size + self.spacing

        self.orbit_icon = ImageButton(win=self.win,
            x=self.building_editor_icon.get_screen_x() - 50,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("orbit_icon.png"), (25, 25)),
            tooltip="show orbit",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_global_variable("show_orbit", True))
        self.widgets.append(self.orbit_icon)
        self.max_width += self.icon_size + self.spacing

        # self.set_global_variable("show_orbit", True,var="enable_orbit" ))
        self.grid_icon = ImageButton(win=self.win,
            x=self.building_editor_icon.get_screen_x() - 50,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("grid_icon.png"), (25, 25)),
            tooltip="show grid",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_global_variable("show_grid", True))
        self.widgets.append(self.grid_icon)
        self.max_width += self.icon_size + self.spacing

        self.buttons_icon = ImageButton(win=self.win,
            x=self.building_editor_icon.get_screen_x() - 50,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("build.png"), (25, 25)),
            tooltip="show buttons on panel or on planet",
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_global_variable("planet_button_display_on_panel", True))
        self.widgets.append(self.buttons_icon)
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
        self.surface_rect.x = width - global_params.app.building_panel.surface.get_width() - self.max_width
        self.reposition_widgets()
        self.toggle_switch.reposition()

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.screen_x = (self.surface_rect.x + self.spacing) + (
                    self.icon_size + self.spacing) * self.widgets.index(icon)

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
