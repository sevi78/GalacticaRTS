import pygame

from source.gui.lod import inside_screen
from source.multimedia_library.gif_handler import GifHandler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils.colors import colors


class PanZoomPlanetDraw:
    def __init__(self, **kwargs):
        self.frame_color = colors.frame_color
        self.gif = kwargs.get("gif", None)
        self.gif_handler = None
        self._atmosphere_name = ""
        self.has_atmosphere = kwargs.get("has_atmosphere", 0)

        self.atmosphere = None
        self.atmosphere_raw = None

        if self.gif:
            if self.gif == "sun.gif":
                self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.4)
            else:
                self.gif_handler = GifHandler(self, self.gif, loop=True, relative_gif_size=1.0)

    def draw_text(self):
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



    def draw_image(self):
        self.win.blit(self.image, self.rect)
