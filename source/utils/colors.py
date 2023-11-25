import pygame


class Colors:
    def __init__(self):
        # set the colors
        self.emp_color = (123, 123, 123, 123)
        self.hover_color = pygame.color.THECOLORS["green"]
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
        self.select_color = pygame.color.THECOLORS["cyan"]
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
