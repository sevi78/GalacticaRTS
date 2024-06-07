import pygame

from source.configuration.game_config import config


def dim_color(color, value, min_value, maximize=False):
    """
    Dim a color based on a given value.

    Args:
        color (tuple): RGB values of the color to be dimmed.
        value (int): Value to dim the color by (0 to 255).
        min_value (int): Minimum value for the dimmed color components.
        maximize (bool): Flag to indicate whether to maximize the color values.

    Returns:
        tuple: Dimmed RGB values of the color.
    """
    # Function to dim a color based on the provided value
    r, g, b = color[:3]
    max_color = max(r, g, b)

    if maximize:
        if max_color > 0:
            r = 255 / max_color * r
            g = 255 / max_color * g
            b = 255 / max_color * b

    fade_factor = 1 - (value / 255)

    r = max(min_value, min(255, int(r * fade_factor)))
    g = max(min_value, min(255, int(g * fade_factor)))
    b = max(min_value, min(255, int(b * fade_factor)))

    return r, g, b


class Colors:
    def __init__(self):
        # set the colors
        self.emp_color = (123, 123, 123, 123)
        self.hover_color = pygame.color.THECOLORS["darkgreen"]
        self.pressed_color = pygame.color.THECOLORS["cyan"]
        self.inactive_color = pygame.color.THECOLORS["red"]
        self.shadow_color = pygame.color.THECOLORS["orange"]
        self.text_color = pygame.color.THECOLORS["white"]
        self.border_color = pygame.color.THECOLORS["purple"]
        self.hover_border_color = pygame.color.THECOLORS["brown"]
        self.pressed_border_color = pygame.color.THECOLORS["grey"]
        self.frame_color = (55, 130,
                            157)  ##37829D# (120, 204, 226)  # "#78cce2" #"#4E7988"  #("#38BFC6")# pygame.colordict.THECOLORS["darkslategray1"]"#d3f8ff"
        self.background_color = (0, 7, 13)  # pygame.colordict.THECOLORS["black"]
        self.ui_white = (238, 253, 254)  # "#eefdfe"
        self.ui_dark = (55, 130, 157)  # "#37829d"
        self.ui_darker = (8, 51, 54)
        self.orbit_color = (8, 51, 50)
        self.orbit_color_planet = (9, 32, 20)
        self.orbit_color_moon = (7, 15, 32)

        self.select_color = pygame.color.THECOLORS["cyan"]
        self.outside_screen_color = pygame.color.THECOLORS.get("red")
        self.pygame_color_names = list(pygame.color.THECOLORS.keys())

        self.orbit_colors = {}
        self.set_orbit_colors()

    def set_orbit_colors(self):
        self.orbit_colors = {
            "orbit_color": dim_color(self.orbit_color, -config.ui_orbit_color_brightness * 2.55, 0, maximize=False),
            "planet_orbit_color": dim_color(self.orbit_color_planet, -config.ui_planet_orbit_color_brightness * 2.55, 0, maximize=False),
            "moon_orbit_color": dim_color(self.orbit_color_moon, -config.ui_moon_orbit_color_brightness * 2.55, 0, maximize=False)
            }

    def get_orbit_color(self, type_):
        if type_ == "sun":
            return self.orbit_colors["orbit_color"]
        elif type_ == "planet":
            return self.orbit_colors["planet_orbit_color"]
        elif type_ == "moon":
            return self.orbit_colors["moon_orbit_color"]
        else:
            return self.orbit_colors["orbit_color"]


# class PygameColors:
#     def __init__(self):
#         for key, value in pygame.color.THECOLORS.items():
#             setattr(self, key, value)
#
#
# pygame_colors = PygameColors()
# print(pygame_colors.__dict__)
colors = Colors()


def gradient_color(colors_, progress):
    # Calculate the index of the two colors to interpolate between
    index = int(progress * (len(colors_) - 1))
    # If progress is 1, return the last color
    if progress == 1:
        return colors_[-1]
    # Calculate the progress between the two colors
    color_progress = progress * (len(colors_) - 1) - index
    # Interpolate between the two colors
    return (
        int(colors[index][0] * (1 - color_progress) + colors_[index + 1][0] * color_progress),
        int(colors[index][1] * (1 - color_progress) + colors_[index + 1][1] * color_progress),
        int(colors[index][2] * (1 - color_progress) + colors_[index + 1][2] * color_progress),
        )


def calculate_gradient_color(start_color, end_color, percent, **kwargs):
    """Calculate the color gradient based on the start and end colors and the current progress percentage"""
    ignore_colors = kwargs.get("ignore_colors", [])

    # Calculate the gradient color
    r = int(start_color[0] + (end_color[0] - start_color[0]) * percent) if not str(
            start_color[0]) in ignore_colors else 0
    g = int(start_color[1] + (end_color[1] - start_color[1]) * percent) if not str(
            start_color[1]) in ignore_colors else 0
    b = int(start_color[2] + (end_color[2] - start_color[2]) * percent) if not str(
            start_color[2]) in ignore_colors else 0

    # Ensure the maximum RGB value matches the maximum value in the end color
    max_rgb = max(r, g, b)
    max_end_color = max(end_color)
    if max_rgb != max_end_color:
        # Calculate the factor to adjust the components proportionally
        factor = max_end_color / max_rgb
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

    return r, g, b


def get_average_color(image: pygame.surface.Surface, **kwargs):
    consider_alpha = kwargs.get("consider_alpha", False)
    color = pygame.transform.average_color(image, image.get_rect(), consider_alpha)
    return color
