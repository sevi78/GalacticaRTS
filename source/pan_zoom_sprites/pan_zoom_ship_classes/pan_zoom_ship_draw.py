import random

import pygame

from source.gui.event_text import event_text
from source.gui.lod import inside_screen
from source.gui.widgets.progress_bar import ProgressBar
from source.utils import global_params
from source.utils.colors import colors
from source.multimedia_library.images import get_image
from source.multimedia_library.sounds import sounds

STATE_IMAGE_SIZE = 27


class PanZoomShipDraw:
    """

    """

    def __init__(self, kwargs):
        self.frame_color = colors.frame_color

        # state images
        self.noenergy_image = get_image("noenergy_25x25.png")
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.get_screen_height()

        self.moving_image = pygame.transform.scale(
            get_image("moving.png"), (STATE_IMAGE_SIZE - 5, STATE_IMAGE_SIZE - 5))
        self.sleep_image = pygame.transform.scale(
            get_image("sleep.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))
        self.orbit_image = pygame.transform.scale(
            get_image("orbit_icon.png"), (STATE_IMAGE_SIZE, STATE_IMAGE_SIZE))

        self.rank_image_pos = (self.rect.centerx + self.get_screen_width() / 2 / self.get_zoom(),
                               self.rect.centery - self.get_screen_height() / 2 / self.get_zoom())

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
        if not inside_screen(self.get_screen_position()):
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

    def draw_rank_image(self):
        # if not global_params.app.build_menu_visible:
        image = self.rank_images[self.rank]
        self.rank_image_pos = (self.rect.centerx + self.get_screen_width() / 2 / self.get_zoom(),
                               self.rect.centery - self.get_screen_height() / 2 / self.get_zoom())

        self.win.blit(image, self.rank_image_pos)

    def draw_image(self):
        if inside_screen(self.get_screen_position()):
            self.win.blit(self.image, self.rect)

    def draw_scope(self):
        """
        draws line to mouse position and draws the scope
        """
        if global_params.hover_object != None:
            color = colors.hover_color
            # print("draw_scope", global_params.hover_object,global_params.hover_object.name )
        else:
            color = self.frame_color

        # draw line from selected object to mouse cursor
        if self.selected:
            pygame.draw.line(surface=self.win, start_pos=self.rect.center, end_pos=pygame.mouse.get_pos(), color=color)

            # scope
            pos = pygame.mouse.get_pos()
            size_x = 30
            size_y = 30
            arrow = pygame.draw.arc(self.win, color, (
                (pos[0] - size_x / 2, pos[1] - size_y / 2), (size_x, size_y)), 2, 10, 2)

            arrow = pygame.draw.arc(self.win, color, (
                (pos[0] - size_x, pos[1] - size_y), (size_x * 2, size_y * 2)), 2, 10, 2)

            # horizontal line
            factor = size_x / 12
            x = pos[0] - size_x * factor / 2
            y = pos[1]
            x1 = x + size_x * factor
            y1 = y
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
                x1, y1), color=color)

            # vertical line
            x = pos[0]
            y = pos[1] - size_x * factor / 2
            x1 = x
            y1 = y + size_x * factor
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
                x1, y1), color=color)

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

    def get_state_image_position(self):
        x = self.rect.centerx
        y = self.rank_image_pos[1] - self.moving_image.get_rect().height
        return x, y

    def draw_moving_image(self):
        self.win.blit(self.moving_image, self.get_state_image_position())

    def draw_sleep_image(self):
        self.win.blit(self.sleep_image, self.get_state_image_position())

    def draw_orbit_image(self):
        self.win.blit(self.orbit_image, self.get_state_image_position())

    def draw_state(self):
        if self.move_stop > 0:
            self.draw_noenergy_image()
            return
        if self.moving:
            self.draw_moving_image()
        elif self.orbiting:
            self.draw_orbit_image()
        else:
            self.draw_sleep_image()

    def draw_noenergy_image(self):
        if not self._disabled:
            self.win.blit(self.noenergy_image, (
                self.rect.centerx + self.noenergy_image_x, self.rect.centery + self.noenergy_image_y))

    def draw__(self):
        self.progress_bar.set_progressbar_position()
        self.draw_scope()

        if inside_screen(self.get_screen_position()):
            self.draw_state()
            self.draw_rank_image()

        if self.selected:
            self.draw_selection()
            self.set_info_text()

        # travel
        if self.target:
            if self.energy > 0:
                self.move_to_connection()
                self.draw_connections()

        if self.energy_reloader:
            # reload ship
            self.reload_ship()

        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop += 1

            sounds.stop_sound(self.sound_channel)
            self.draw_noenergy_image()
            self.set_experience(-1)

        self.low_energy_warning()
