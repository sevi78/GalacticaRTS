import random

import pygame

from source.gui.event_text import event_text
from source.gui.lod import level_of_detail
from source.gui.widgets.progress_bar import ProgressBar
from source.handlers.color_handler import colors

STATE_IMAGE_SIZE = 27


class PanZoomShipDraw:
    def __init__(self, kwargs):
        self.frame_color = colors.frame_color

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
            x=self.get_screen_x(),
            y=self.get_screen_y() + self.get_screen_height() + self.get_screen_height() / 5,
            width=self.get_screen_width(),
            height=5,
            progress=lambda: 1 / self.energy_max * self.energy,
            curved=True,
            completedColour=self.frame_color,
            layer=self.layer,
            parent=self
            )

    def flickering(self):
        if not level_of_detail.inside_screen(self.get_screen_position()):
            return
        # make flickering relaod stream :))
        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)
        r1 = random.randint(0, 17)
        r2 = random.randint(0, 9)

        startpos = (self.rect.center[0] + r, self.rect.center[1] + r)
        endpos = (self.energy_reloader.rect.center[0] + r0, self.energy_reloader.rect.center[1] + r0)

        if r0 == 0:
            return

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["yellow"], width=r2)

        if r == 7:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["red"], width=r1)

        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["white"], width=r * 2)

        # pygame.mixer.Channel(2).play (sounds.electricity2)
        # sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
        event_text.text = "reloading spaceship: --- needs a lot of energy!"



    def draw_selection(self):
        pygame.draw.circle(self.win, self.frame_color, self.rect.center, self.get_screen_width(), int(6 * self.get_zoom()))

    def draw_connections(self):
        if self.target:
            if hasattr(self.target, "x"):
                if not self.target.property == "ufo":
                    pygame.draw.line(surface=self.win,
                        start_pos=self.rect.center,
                        end_pos=self.target.center,
                        color=self.frame_color,
                        width=5)
