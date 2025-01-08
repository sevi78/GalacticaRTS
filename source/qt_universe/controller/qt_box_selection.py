import random
from typing import List, Tuple, Optional

import pygame


class DummyObject:
    def __init__(self, x, y, width=10, height=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.selected = False


class BoxSelection:
    """
    A class to handle box selection of objects in a pygame window.

    This class manages the selection of objects by clicking or dragging a box around them.
    It supports both single and multi-selection modes.
    """

    def __init__(self, window: pygame.Surface, selectable_objects: List[object]):
        """
        Initialize the BoxSelection object.

        Args:
            window (pygame.Surface): The pygame window surface to draw on.
            selectable_objects (List[object]): A list of objects that can be selected.
        """
        self.window: pygame.Surface = window
        self.selectable_objects: List[object] = selectable_objects
        self.start_pos: Optional[Tuple[int, int]] = None
        self.end_pos: Optional[Tuple[int, int]] = None
        self.selecting: bool = False
        self.click_threshold: int = 5  # Pixels to consider as a click vs. drag

    def set_selectable_objects(self, selectable_objects: List[object]) -> None:
        """
        Update the list of selectable objects.

        Args:
            selectable_objects (List[object]): A new list of objects that can be selected.
        """
        self.selectable_objects = selectable_objects

    def listen(self, events: List[pygame.event.Event]) -> None:
        """
        Listen for and handle pygame events related to selection.

        Args:
            events (List[pygame.event.Event]): A list of pygame events to process.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.start_selection(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.end_selection(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.update_selection(event.pos)

    def start_selection(self, pos: Tuple[int, int]) -> None:
        """
        Start the selection process when the mouse button is pressed.

        Args:
            pos (Tuple[int, int]): The (x, y) position where the selection started.
        """
        self.selecting = True
        self.start_pos = pos
        self.end_pos = pos

    def end_selection(self, pos: Tuple[int, int]) -> None:
        """
        End the selection process when the mouse button is released.

        Args:
            pos (Tuple[int, int]): The (x, y) position where the selection ended.
        """
        self.selecting = False
        self.end_pos = pos
        if self.is_click():
            self.handle_click(pos)
        else:
            self.update_selected_objects()

    def update_selection(self, pos: Tuple[int, int]) -> None:
        """
        Update the selection area as the mouse moves.

        Args:
            pos (Tuple[int, int]): The current (x, y) position of the mouse.
        """
        if self.selecting:
            self.end_pos = pos

    def is_click(self) -> bool:
        """
        Determine if the selection action was a click or a drag.

        Returns:
            bool: True if the action was a click, False if it was a drag.
        """
        if not self.start_pos or not self.end_pos:
            return False
        dx = abs(self.end_pos[0] - self.start_pos[0])
        dy = abs(self.end_pos[1] - self.start_pos[1])
        return dx <= self.click_threshold and dy <= self.click_threshold

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle object selection when a click is detected.

        Args:
            pos (Tuple[int, int]): The (x, y) position of the click.
        """
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
        clicked_object = None

        # Find the first object that collides with the click position
        for obj in self.selectable_objects:
            if obj.rect.collidepoint(pos):
                clicked_object = obj
                break

        if clicked_object:
            if shift_pressed:
                # Toggle selection of clicked object if shift is pressed
                clicked_object.selected = not clicked_object.selected
            else:
                # Select only the clicked object if shift is not pressed
                for obj in self.selectable_objects:
                    obj.selected = (obj == clicked_object)
        elif not shift_pressed:
            # Deselect all objects if clicking empty space without shift
            for obj in self.selectable_objects:
                obj.selected = False

    def update_selected_objects(self) -> None:
        """
        Update the selection status of objects based on the selection rectangle.
        """
        selection_rect = self.get_selection_rect()
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT

        for obj in self.selectable_objects:
            if selection_rect.collidepoint(obj.rect.center):
                if shift_pressed:
                    # Toggle selection if shift is pressed
                    obj.selected = not obj.selected
                else:
                    # Select object if it's in the selection rectangle
                    obj.selected = True
            elif not shift_pressed:
                # Deselect object if it's outside the selection rectangle and shift is not pressed
                obj.selected = False

    def get_selection_rect(self) -> pygame.Rect:
        """
        Get the rectangle representing the current selection area.

        Returns:
            pygame.Rect: A rectangle representing the selection area.
        """
        if not self.start_pos or not self.end_pos:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(min(self.start_pos[0], self.end_pos[0]),
                min(self.start_pos[1], self.end_pos[1]),
                abs(self.end_pos[0] - self.start_pos[0]),
                abs(self.end_pos[1] - self.start_pos[1]))

    def draw(self) -> None:
        """
        Draw the selection rectangle on the window if a selection is in progress.
        """
        if self.selecting:
            pygame.draw.rect(self.window, (0, 0, 255), self.get_selection_rect(), 1)


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Box Selection Demo")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Generate random positions for objects
    num_objects = 20
    objects = [DummyObject(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_objects)]

    # Create BoxSelection instance
    box_selection = BoxSelection(screen, objects)
    # Main game loop
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        box_selection.listen(events)

        # Clear the screen
        screen.fill(WHITE)

        # Draw objects
        for obj in objects:
            color = RED if obj.selected else BLACK
            pygame.draw.rect(screen, color, obj.rect)

        # Draw selection box
        box_selection.draw()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
