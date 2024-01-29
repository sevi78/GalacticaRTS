import pygame
from pygame_widgets.util import drawText

from source.gui.lod import inside_screen
from source.gui.panels.building_panel_components.building_panel import SPECIAL_FONT_SIZE
from source.gui.panels.building_panel_components.building_panel_draw import SPECIAL_TEXT_COLOR
from source.multimedia_library.gif_handler import GifHandler
from source.multimedia_library.images import get_image
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.color_handler import colors


class PanZoomPlanetDraw:
    def __init__(self, **kwargs):
        self.frame_color = colors.frame_color
        self.gif = kwargs.get("gif", None)
        self.gif_handler = None
        self.setup_gif_handler()
        self.special_images = {}
        self.setup_special_images()

    def setup_special_images(self):
        self.special_images = {}
        for key in self.production.keys():
            self.special_images[key] = get_image(key + '_25x25.png')

    def setup_gif_handler(self):
        if self.gif:
            if self.gif == "sun.gif":
                self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.4)
            else:
                self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.0)

    def draw_text(self):
        if self.get_zoom() > 0.1:
            self.text = self.font.render(self.string, True, colors.frame_color)
            self.text_rect = self.text.get_rect()
            self.text_rect.centerx = self.rect.centerx
            self.text_rect.bottom = self.rect.centery + self.rect.height
            self.win.blit(self.text, self.text_rect)

    def draw_hover_circle(self):
        panzoom = pan_zoom_handler
        pygame.draw.circle(self.win, self.frame_color, self.rect.center,
            (self.rect.height / 2) + 4, int(6 * panzoom.zoom))

    def draw_check_image(self):
        if not self.parent.selected_planet == self and not self.selected:
            return

        if not inside_screen(self.get_position()):
            return

        rect = self.check_image.get_rect()
        rect.x, rect.y = self.get_screen_x(), self.get_screen_y()
        self.win.blit(self.check_image, rect)

    def draw_selection_circle(self):
        if not self.parent.selected_planet == self and not self.selected:
            return

        if not inside_screen(self.get_position()):
            return

        ui_circle_size = 15
        panzoom = pan_zoom_handler

        # Define the maximum size and brightness of the pulse
        max_radius = int(100 * panzoom.zoom)

        if self.selected:
            max_brightness = 150
            pulse_time = 1000
            select_color = pygame.color.THECOLORS["green"]
        else:
            max_brightness = 255
            pulse_time = 2000
            select_color = self.frame_color

        # Calculate the current size and brightness based on time
        time = pygame.time.get_ticks()  # Get the current time in milliseconds
        pulse_progress = (time % pulse_time) / pulse_time  # Calculate the progress of the pulse (0 to 1)
        current_radius = int(ui_circle_size + pulse_progress * (max_radius - ui_circle_size))
        current_brightness = int(pulse_progress * max_brightness)

        # Create a surface for the pulse circle
        pulse_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)

        # Draw the pulse circle on the surface
        color = (select_color[0], select_color[1], select_color[2], current_brightness)
        pygame.draw.circle(pulse_surface, color,
            (
                current_radius, current_radius), current_radius,
            1)

        # Blit the pulse surface onto the window
        self.win.blit(pulse_surface, (self.center[0] - current_radius, self.center[1] - current_radius))

    def draw_specials__(self):
        if not inside_screen(self.get_position()):
            return
        # print ("draw_specials")
        count = 0
        x = self.screen_position[0] + self.screen_width / 2 + 20

        if len(self.specials) > 0:
            for key, value in self.specials_dict.items():
                y = self.rect.centery + (20 * count)
                operator, value = value["operator"], value["value"]
                if not value == 0:
                    if key in self.production.keys():
                        self.win.blit(self.special_images[key], (x, y))

                        if operator == "*":
                            operator = "x"

                        drawText(self.win, f"{operator}{str(value)}", SPECIAL_TEXT_COLOR,
                            (x + 25, y, 50, 20), pygame.font.SysFont("georgiaproblack", SPECIAL_FONT_SIZE), "left")
                        count += 1

    def draw_specials(self):
        if not inside_screen(self.get_position()):
            return
        # Load the font once
        font = pygame.font.SysFont("georgiaproblack", SPECIAL_FONT_SIZE)
        x = self.screen_position[0] + self.screen_width / 2 + 20
        y = self.rect.centery

        if self.alien_population > 0:
            if self.alien_attitude < 50:
                alien_image = pygame.transform.scale(get_image("alien_face_orange.png"), (25, 25))
            else:
                alien_image = pygame.transform.scale(get_image("alien_face_green.png"), (25, 25))
            self.win.blit(alien_image, (self.screen_position[0] - self.screen_width / 2 - 60 * self.get_zoom() , self.rect.centery))


        if self.specials:
            count = 0
            for key, value in self.specials_dict.items():
                operator, value = value["operator"], value["value"]
                if value != 0 and key in self.production.keys():
                    self.win.blit(self.special_images[key], (x, y))

                    if operator == "*":
                        operator = "x"

                    drawText(self.win, f"{operator}{str(value)}", SPECIAL_TEXT_COLOR,
                        (x + 25, y, 50, 20), font, "left")
                    count += 1
                    y += 20  # Increment y for the next draw


    def draw_image(self):
        self.win.blit(self.image, self.rect)
