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

        self._value = 0.0
        self.value = 0.0

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value
        self.draw_surface()
        # self.parent.update_scroll_position_from_scrollbar(value)

    def draw_surface(self) -> None:
        """
        Draws the surface of the scroll bar based on the current value.

        This function updates the surface, draws a rounded rectangle, calculates the height and position of the inner
        rectangle, and then draws the inner rectangle on the surface.
        """

        # update surface
        self.surface.fill((0, 0, 0, 0))

        # draw rounded rect
        pygame.draw.rect(self.surface, colors.ui_darker,
                (0, 0, self.world_width, self.world_height), config.get("ui_rounded_corner_small_thickness"),
                config.get("ui_rounded_corner_radius_small"))

        # calculate height of the inner rect
        height = self.world_height / (len(self.parent.widgets) - self.parent.visible_index_range + 1)

        # calculate the position of the inner rect
        y = self.world_height * self.value

        # draw inner rect
        pygame.draw.rect(self.surface, colors.ui_darker, (
            0, y, self.world_width, height), 0, config.get("ui_rounded_corner_radius_small"))

    def update_position(self)->None:
        """sets the position of the widget to the bottom right corner of the parent"""
        self.world_x = self.parent.world_x + self.parent.world_width - self.world_width
        self.world_y = self.parent.world_y + self.parent.world_height - self.world_height
        self.rect.x, self.rect.y = self.world_x, self.world_y

    def listen(self, events)->None:
        """
        Listens for mouse events and updates the scrollbar value based on the click position.

        Parameters:
            events (list): A list of pygame.event.Event objects representing mouse events.

        Returns:
            None
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # Calculate the relative position of the click within the scrollbar
                    click_position = event.pos[1] - self.rect.y
                    # Normalize the click position to a value between 0 and 1
                    self.value = click_position / self.rect.height
                    self.parent.update_scroll_position_from_scrollbar(self.value)

    def draw(self):
        self.win.blit(self.surface, self.rect)
