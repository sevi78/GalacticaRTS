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


class PlanetaryDefenceWidget(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)

        self.name = "Planetary Defence"
        self.icon_size = kwargs.get("icon_size", 25)
        self.parent = kwargs.get("parent", None)
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.world_y
        self.spacing = self.parent.spacing
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)

        # text
        self.font_size = kwargs.get("font_size", 12)
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.info_text = kwargs.get("infotext")

        # buttons
        self.buttons = []
        self.button_size = 25
        self.cannon_icon = ImageButton(win=self.win,
            x=self.get_screen_x(),
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("cannon.png"), (self.button_size, self.button_size)),
            tooltip="build cannon",
            info_text= create_info_panel_planetary_defence_text("cannon"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.build("cannon"))



        # buttons
        self.missile_launcher_icon = ImageButton(win=self.win,
            x=self.get_screen_x() + self.button_size + 10,
            y=self.surface_rect.y + self.spacing,
            width=self.icon_size,
            height=self.icon_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(get_image("missile.png"), (self.button_size, self.button_size)),
            tooltip="build missile launcher",
            info_text=create_info_panel_planetary_defence_text("missile"),
            frame_color=self.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.build("missile"))

        # initial hide the buttons
        self.parent.widgets.append(self)
        self.buttons.append(self.cannon_icon)
        self.buttons.append(self.missile_launcher_icon)
        self.hide_buttons()

        print (create_info_panel_building_text())

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

    def listen_(self, events):
        pass

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

        if "space harbor" in self.parent.parent.selected_planet.buildings:
            self.surface_rect.y = self.parent.world_y + self.parent.sub_widget_height + self.spacing + 5

        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, ui_rounded_corner_small_thickness, global_params.ui_rounded_corner_radius_small)
        self.win.blit(self.surface, self.surface_frame)

        # label
        drawText(self.win, self.name, self.frame_color,
            (self.surface_rect.x + self.parent.spacing_x - 36, self.surface_rect.y + self.spacing,
             self.get_screen_width(),
             20), self.font, "center")

        # buttons
        self.cannon_icon.set_position((self.surface_rect.x + self.spacing * 3, self.surface_rect.y + self.spacing + 20))
        self.missile_launcher_icon.set_position((
        self.surface_rect.x + self.button_size + 10 + self.spacing * 3, self.surface_rect.y + self.spacing + 20))

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

            # get the position and size
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

            # add building widget to building cue to make shure it can be build only if building_cue is < building_slots_amount
            planet.building_cue += 1
