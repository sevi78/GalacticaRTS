import pygame

from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.utils.colors import gradient_color


def draw_pulsating_circle(win, color_: tuple[3], center, min_radius, max_radius, width, pulse_time):
    max_brightness = 255

    # Calculate the current size and brightness based on time
    time = pygame.time.get_ticks()  # Get the current time in milliseconds
    pulse_progress = (time % pulse_time) / pulse_time  # Calculate the progress of the pulse (0 to 1)
    current_radius = int(min_radius + pulse_progress * (max_radius - min_radius))
    current_brightness = int(pulse_progress * max_brightness)

    # Create a surface for the pulse circle
    pulse_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)

    # Draw the pulse circle on the surface
    dim_color = (color_[0], color_[1], color_[2], current_brightness)
    pygame.draw.circle(pulse_surface, dim_color, (current_radius, current_radius), current_radius, width)

    # Blit the pulse surface onto the window
    win.blit(pulse_surface, (center[0] - current_radius, center[1] - current_radius))


def draw_pulsating_circles(win, color_: tuple[3], center, min_radius, max_radius, width, pulse_time, circles):
    max_brightness = 255

    # Calculate the current size and brightness based on time
    time = pygame.time.get_ticks()  # Get the current time in milliseconds
    pulse_progress = (time % pulse_time) / pulse_time  # Calculate the progress of the pulse (0 to 1)
    current_brightness = int(pulse_progress * max_brightness)

    # Create a surface for the pulse circle
    pulse_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)

    # Draw each pulse circle on the surface
    for i in range(circles):
        radius = min_radius + (max_radius - min_radius) * i / (circles - 1)
        current_radius = int(radius + pulse_progress * (max_radius - radius))
        dim_color = (color_[0], color_[1], color_[2], current_brightness)
        pygame.draw.circle(pulse_surface, dim_color, (max_radius, max_radius), current_radius, width)

    # Blit the pulse surface onto the window
    win.blit(pulse_surface, (center[0] - max_radius, center[1] - max_radius))


def draw_electromagnetic_impulse(win, center, min_radius, max_radius, width, pulse_time, circles):
    # Define the colors for the gradient
    colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (0, 0, 255)]

    # Calculate the current size and brightness based on time
    time = pygame.time.get_ticks()  # Get the current time in milliseconds
    pulse_progress = (time % pulse_time) / pulse_time  # Calculate the progress of the pulse (0 to 1)

    # Create a surface for the pulse circles
    pulse_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)

    # Draw each pulse circle on the surface
    for i in range(circles):
        radius = min_radius + (max_radius - min_radius) * i / (circles - 1)
        current_radius = int(radius + pulse_progress * (max_radius - radius))
        color = gradient_color(colors, i / (circles - 1))
        dim_color = (color[0], color[1], color[2], int(pulse_progress * 255))
        pygame.draw.circle(pulse_surface, dim_color, (max_radius, max_radius), current_radius, width)

    # Blit the pulse surface onto the window
    win.blit(pulse_surface, (center[0] - max_radius, center[1] - max_radius))


def draw_zoomable_circle(surface, color, world_x, world_y, radius):
    screen_x, screen_y = pan_zoom_handler.world_2_screen(world_x, world_y)
    pygame.draw.circle(surface, color,(screen_x, screen_y), radius * pan_zoom_handler.zoom, 1)


def draw_transparent_circle(surface, color, position, radius, alpha):
    circle_surface =pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, color + (alpha,), (radius, radius), radius)
    surface.blit(circle_surface, (position[0] - radius, position[1] - radius))
