import pygame


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
        self.hoverBorderColour = pygame.color.THECOLORS["brown"]
        self.pressedBorderColour = pygame.color.THECOLORS["grey"]
        self.frame_color = (55, 130,
                            157)  # (120, 204, 226)  # "#78cce2" #"#4E7988"  #("#38BFC6")# pygame.colordict.THECOLORS["darkslategray1"]"#d3f8ff"
        self.background_color = (0, 7, 13)  # pygame.colordict.THECOLORS["black"]
        self.ui_white = (238, 253, 254)  # "#eefdfe"
        self.ui_dark = (55, 130, 157)  # "#37829d"
        self.ui_darker = (8, 51, 54)
        self.orbit_color = (8, 51, 50)
        self.orbit_color_planet = (9, 30, 20)
        self.orbit_color_moon = (7, 15, 36)
        self.select_color = pygame.color.THECOLORS["cyan"]
        self.outside_screen_color = pygame.color.THECOLORS.get("red")
        self.pygame_color_names = list(pygame.color.THECOLORS.keys())


class PygameColors:
    def __init__(self):
        for key, value in pygame.color.THECOLORS.items():
            setattr(self, key, value)


pygame_colors = PygameColors()
# print(pygame_colors.__dict__)
colors = Colors()


# class Colors:
#     def __init__(self):
#         # set the colors
#         self.hover_color = pygame.color.THECOLORS["blue"]
#         self.pressed_color = pygame.color.THECOLORS["cyan"]
#         self.inactive_color = pygame.color.THECOLORS["red"]
#         self.shadow_color = pygame.color.THECOLORS["orange"]
#         self.text_color = pygame.color.THECOLORS["white"]
#         self.border_color = pygame.color.THECOLORS["purple"]
#         self.hoverBorderColour = pygame.color.THECOLORS["brown"]
#         self.pressedBorderColour = pygame.color.THECOLORS["grey"]
#         self.frame_color = pygame.colordict.THECOLORS["darkslategray1"]
#         self.background_color = pygame.colordict.THECOLORS["black"]
#         self.ui_white = pygame.color.THECOLORS["cyan"]
#         self.ui_dark = pygame.color.THECOLORS["purple"]

def dim_color(color, value, min_value):
    r, g, b = color
    fade_factor = 1 - (value / 255)

    r = max(min_value, min(255, int(r * fade_factor)))
    g = max(min_value, min(255, int(g * fade_factor)))
    b = max(min_value, min(255, int(b * fade_factor)))

    return r, g, b


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


def calculate_gradient_color__(start_color, end_color, percent, **kwargs):  # orig
    """Calculate the color gradient based on the start and end colors and the current progress percentage"""
    ignore_colors = kwargs.get("ignore_colors", [])
    r, g, b = 0, 0, 0
    r = int(start_color[0] + (end_color[0] - start_color[0]) * percent) if not str(r) in ignore_colors else 0
    g = int(start_color[1] + (end_color[1] - start_color[1]) * percent) if not str(g) in ignore_colors else 0
    b = int(start_color[2] + (end_color[2] - start_color[2]) * percent) if not str(b) in ignore_colors else 0

    return r, g, b


def calculate_gradient_color___(start_color, end_color, percent, **kwargs):
    """Calculate the color gradient based on the start and end colors and the current progress percentage"""
    ignore_colors = kwargs.get("ignore_colors", [])

    # Calculate the gradient color
    r = int(start_color[0] + (end_color[0] - start_color[0]) * percent) if not str(
        start_color[0]) in ignore_colors else 0
    g = int(start_color[1] + (end_color[1] - start_color[1]) * percent) if not str(
        start_color[1]) in ignore_colors else 0
    b = int(start_color[2] + (end_color[2] - start_color[2]) * percent) if not str(
        start_color[2]) in ignore_colors else 0

    # Ensure the sum of the colors is always 255
    sum_rgb = r + g + b
    if sum_rgb != 255:
        # Calculate the factor to adjust the components proportionally
        factor = 255 / sum_rgb
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

    return r, g, b


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


def get_average_color(image: pygame.surface.Surface):
    color = pygame.transform.average_color(image, image.get_rect())
    return color
