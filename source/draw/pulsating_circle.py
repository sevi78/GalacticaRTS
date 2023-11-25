import pygame


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
    pygame.draw.circle(pulse_surface, dim_color,(current_radius, current_radius), current_radius,width)

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


def gradient_color(colors, progress):
    # Calculate the index of the two colors to interpolate between
    index = int(progress * (len(colors) - 1))
    # If progress is 1, return the last color
    if progress == 1:
        return colors[-1]
    # Calculate the progress between the two colors
    color_progress = progress * (len(colors) - 1) - index
    # Interpolate between the two colors
    return (
        int(colors[index][0] * (1 - color_progress) + colors[index + 1][0] * color_progress),
        int(colors[index][1] * (1 - color_progress) + colors[index + 1][1] * color_progress),
        int(colors[index][2] * (1 - color_progress) + colors[index + 1][2] * color_progress),
    )

