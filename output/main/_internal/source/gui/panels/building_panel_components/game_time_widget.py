from datetime import datetime

import pygame

from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.slider import Slider
from source.configuration import global_params
from source.handlers.color_handler import colors
from source.configuration.global_params import ui_rounded_corner_small_thickness
from source.multimedia_library.images import get_image


class GameTime(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.clockslider_height = 7
        self.time_factor = 1
        self.world_year = int(datetime.timestamp(datetime.now()))

        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, int(ui_rounded_corner_small_thickness), int(global_params.ui_rounded_corner_radius_small))

        self.font_size = 18
        self.font = pygame.font.SysFont(global_params.font_name, self.font_size)
        self.create_slider()
        self.create_icons()

    def create_icons(self):
        self.image = get_image("clock.png")
        self.image_size = self.image.get_size()
        self.clock_icon = ImageButton(win=self.win,
            x=self.surface_rect.x + (self.spacing / 2),
            y=self.surface_rect.y + (self.spacing / 2),
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=self.image,
            tooltip="this is the time, don't waste it !",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.clock_slider.setValue(1),
            layer=self.layer
            )

        self.arrow_size = 15
        self.minus_arrow_button = Button(win=self.win,
            x=self.clock_icon.get_screen_x() + self.spacing * 2,
            y=self.clock_slider.get_screen_y() - self.clock_slider.get_screen_height() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                get_image("arrow-left.png"), (self.arrow_size, self.arrow_size)),
            tooltip="decrease time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(-1),
            layer=self.layer
            )

        self.plus_arrow_button = Button(win=self.win,
            x=self.clock_icon.get_screen_x() + self.spacing * 2 + self.arrow_size,
            y=self.clock_slider.get_screen_y() - self.clock_slider.get_screen_height() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                get_image("arrow-right.png"), (self.arrow_size, self.arrow_size)),
            tooltip="increase time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(+1),
            layer=self.layer
            )

    def create_slider(self):
        # construct slider_____
        self.spacing_x = 35
        self.clock_slider = Slider(win=self.win,
            x=self.surface_rect.x + self.spacing_x + self.spacing_x,
            y=self.surface_rect.y + int(self.spacing / 2),
            width=self.surface_rect.width - self.spacing - self.spacing_x * 2,
            height=self.clockslider_height,
            min=1, max=50, step=1, handleColour=colors.ui_darker, layer=self.layer)

        self.clock_slider.colour = self.frame_color
        self.clock_slider.setValue(global_params.game_speed)

        # construct texts
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.world_year_text = global_params.app.ui_helper.hms(self.world_year)

    def set_clockslider_value(self, value):
        if value < 0:
            if self.clock_slider.min + 1 < self.clock_slider.getValue() - value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)
        elif value > 0:
            if self.clock_slider.max + 1 > self.clock_slider.getValue() + value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)

    def update_time(self):
        self.world_year += 0.01 * self.time_factor * global_params.game_speed
        global_params.time_factor = self.time_factor

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()

        # reposition
        self.surface_rect.x = width - self.surface.get_width()
        self.clock_icon.screen_x = self.surface_rect.x + (self.spacing / 2)
        self.clock_slider.screen_x = self.surface_rect.x + self.spacing_x + self.spacing_x
        self.minus_arrow_button.screen_x = self.clock_icon.get_screen_x() + self.spacing * 2 + 3
        self.plus_arrow_button.screen_x = self.clock_icon.get_screen_x() + self.spacing * 2 + self.arrow_size + 3

    def draw_clock(self):
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.win.blit(self.time_warp_text,
            (self.surface_rect.x + self.spacing_x, self.clock_icon.screen_y + self.clock_icon.rect.height / 2))
        year_text = str(round(self.world_year, 2))
        # year_text = get_day_month_year_string(offset=0, year= 2000)
        # print (get_day_month_year_string(offset=0))
        self.year_text = self.font.render("year: " + year_text, True, self.frame_color)
        self.win.blit(self.year_text, (self.surface_rect.x + self.spacing_x + self.spacing_x, self.clock_icon.screen_y +
                                       self.clock_icon.get_screen_height() - self.year_text.get_height() + 6))
        self.time_factor = self.clock_slider.getValue()

    def draw_frame(self):
        # frame
        self.surface = pygame.surface.Surface((self.surface_rect.width, self.surface_rect.height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(global_params.ui_panel_alpha)

        self.win.blit(self.surface, self.surface_frame)
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, int(ui_rounded_corner_small_thickness), int(global_params.ui_rounded_corner_radius_small))

    def draw(self):
        """
        draws the ui elements
        """
        self.update_time()
        self.reposition()

        # frame
        self.draw_frame()

        # clock
        self.draw_clock()

        if self._hidden:
            return
