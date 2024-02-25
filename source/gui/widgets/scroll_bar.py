import pygame


from source.handlers.color_handler import colors

config = {
    "ui_panel_alpha": 220,
    "ui_rounded_corner_big_thickness": 3,
    "ui_rounded_corner_radius_big": 30,
    "ui_rounded_corner_radius_small": 9,
    "ui_rounded_corner_small_thickness": 1
    }

class ScrollBar:
    def __init__(self, win, x, y, width, height, parent):
        # params
        self.win = win
        self.world_x = x
        self.world_y = y
        self.world_width = width
        self.world_height = height
        self.parent = parent
        self.rect = pygame.Rect(self.world_x, self.world_y, self.world_width, self.world_height)

        # surface
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))

        self.value = 0.0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

        self.draw_surface(value)

    def draw_surface(self, value):
        # update surface
        self.surface.fill((0, 0, 0, 0))

        # draw rounded rect
        pygame.draw.rect(self.surface, colors.ui_darker,
            (0, 0, self.world_width, self.world_height), config.get("ui_rounded_corner_small_thickness"),
            config.get("ui_rounded_corner_radius_small"))

        height = self.world_height / len(self.parent.widgets)
        y = self.world_height * self.value

        # draw inne rect
        pygame.draw.rect(self.surface, colors.ui_darker, (
            0, y, self.world_width, height), 0, config.get("ui_rounded_corner_radius_small"))

    def update_position(self):
        self.world_x = self.parent.world_x + self.parent.world_width - self.world_width
        self.world_y = self.parent.world_y + self.parent.world_height - self.world_height
        self.rect.x, self.rect.y = self.world_x, self.world_y

    def listen(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.value = 1 / self.world_height * (pygame.mouse.get_pos()[1] - self.rect.y)
                    self.parent.scroll_offset_y = int(-self.value * len(self.parent.widgets))
                    print("self.parent.scroll_offset_y:", self.parent.scroll_offset_y)
                    self.parent.reposition_widgets()
                    self.parent.drag_enabled = False
                else:
                    self.parent.drag_enabled = True

    def draw(self):
        self.win.blit(self.surface, self.rect)
