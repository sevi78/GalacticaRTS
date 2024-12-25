from datetime import datetime

import pygame

from source.configuration.game_config import config
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.slider import Slider
from source.gui.widgets.widget_base_components.widget_base import WidgetBase
from source.handlers.color_handler import colors
from source.handlers.time_handler import time_handler
from source.multimedia_library.images import get_image

FONT_SIZE = 18


class GameTime(WidgetBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        super().__init__(win, x, y, width, height, is_sub_widget, **kwargs)
        self.time_warp_text = None
        self.clockslider_height = 7
        self.world_year = int(datetime.timestamp(datetime.now()))
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(config.ui_panel_alpha)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)

        self.font_size = FONT_SIZE
        self.font = pygame.font.SysFont(config.font_name, self.font_size)
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
                is_sub_widget=False,
                image=self.image,
                tooltip="this is the time, don't waste it !",
                frame_color=self.frame_color,
                transparent=True,
                on_click=lambda: self.reset_game_speed(),
                layer=self.layer
                )

        self.arrow_size = 15
        self.minus_arrow_button = Button(win=self.win,
                x=self.clock_icon.get_screen_x() + self.spacing * 2,
                y=self.clock_slider.get_screen_y() - self.clock_slider.get_screen_height() - 2,
                width=self.image_size[0],
                height=self.image_size[1],
                is_sub_widget=False,
                image=pygame.transform.scale(
                        get_image("arrow-left.png"), (self.arrow_size, self.arrow_size)),
                tooltip="decrease time",
                frame_color=self.frame_color,
                transparent=True,
                on_click=lambda: self.set_clockslider_value(-1),
                layer=self.layer,
                name="minus_arrow_button"
                )

        self.plus_arrow_button = Button(win=self.win,
                x=self.clock_icon.get_screen_x() + self.spacing * 2 + self.arrow_size,
                y=self.clock_slider.get_screen_y() - self.clock_slider.get_screen_height() - 2,
                width=self.image_size[0],
                height=self.image_size[1],
                is_sub_widget=False,
                image=pygame.transform.scale(
                        get_image("arrow-right.png"), (self.arrow_size, self.arrow_size)),
                tooltip="increase time",
                frame_color=self.frame_color,
                transparent=True,
                on_click=lambda: self.set_clockslider_value(+1),
                layer=self.layer,
                name="plus_arrow_button"
                )

    def create_slider(self):
        # construct slider_____
        self.spacing_x = 35
        self.clock_slider = Slider(
                win=self.win,
                x=self.surface_rect.x + self.spacing_x + self.spacing_x,
                y=self.surface_rect.y + int(self.spacing / 2),
                width=self.surface_rect.width - self.spacing - self.spacing_x * 2,
                height=self.clockslider_height,
                min=1,
                max=1000,
                step=1,
                handle_color=colors.ui_darker,
                layer=self.layer,
                function=lambda arg: self.slider_callback(arg))

        self.clock_slider.color = self.frame_color
        self.clock_slider.set_value(time_handler.game_speed)

        # construct texts
        self.time_warp_text = self.font.render(str(self.clock_slider.get_value()) + "x", True, self.frame_color)
        self.world_year_text = config.app.ui_helper.hms(self.world_year)

    def slider_callback(self, value):
        if not time_handler.game_speed == value:
            time_handler.set_game_speed(value)

    def reset_game_speed(self):
        self.clock_slider.set_value(1)

    def set_clockslider_value(self, value):
        if value < 0:
            if self.clock_slider.min + 1 < self.clock_slider.get_value() - value:
                self.clock_slider.set_value(self.clock_slider.get_value() + value)
        elif value > 0:
            if self.clock_slider.max + 1 > self.clock_slider.get_value() + value:
                self.clock_slider.set_value(self.clock_slider.get_value() + value)

    def update_time(self):
        if not config.game_paused:
            if config.app.game_client.connected:
                self.world_year = time_handler.world_time
            else:
                self.world_year += 0.01 * time_handler.game_speed * 10000

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
        if config.game_paused:
            self.clock_icon.image = get_image("sleep.png")
        else:
            self.clock_icon.image = self.image

        self.time_warp_text = self.font.render(str(self.clock_slider.get_value()) + "x", True, self.frame_color)
        self.win.blit(self.time_warp_text,
                (self.surface_rect.x + self.spacing_x, self.clock_icon.screen_y + self.clock_icon.rect.height / 2))

        now = datetime.fromtimestamp(self.world_year)
        new_datetime = f"{now.year + 70000}-{now.strftime(str(now.month))}-{now.strftime(str(now.day))}-{now.hour}"
        self.year_text = self.font.render(f"year:{new_datetime}", True, self.frame_color)
        self.win.blit(self.year_text, (self.surface_rect.x + self.spacing_x + self.spacing_x, self.clock_icon.screen_y +
                                       self.clock_icon.get_screen_height() - self.year_text.get_height() + 6))

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
