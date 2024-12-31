import math
from typing import List, Set, Tuple, Optional

import pygame

from source.configuration.game_config import config
from source.debug.function_disabler import disabler, auto_disable
from source.draw.scope import scope
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.screenshot import capture_screenshot
from source.text.text_formatter import format_number


#
# disabled_functions = []
# for i in disabled_functions:
#     disabler.disable(i)
#
#
# @auto_disable
class BoxSelection:
    """
    Implements a box selection tool in a Pygame window.
    Allows selecting objects by drawing a box around them or by clicking on them directly.
    Supports both selection and deselection using the Shift key modifier.
    """

    def __init__(self, window: pygame.Surface, selectable_objects: List[pygame.sprite.Sprite]):
        self.window = window
        self.selectable_objects = selectable_objects
        self.selected_objects: Set[pygame.sprite.Sprite] = set()
        self.start_pos: Optional[Tuple[int, int]] = None
        self.end_pos: Optional[Tuple[int, int]] = None
        self.frame_color = colors.frame_color
        self.color = self.frame_color
        self.debug = False

    def __repr__(self) -> str:
        return str(len(self.selected_objects))

    def _should_ignore_hover_object(self) -> bool:
        """Determine if the hover object should be ignored based on its properties."""
        return config.hover_object and (not hasattr(config.hover_object, "property") or
                                        hasattr(config.hover_object, "drag_enabled"))

    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button down events for object selection and box selection initiation."""
        if event.button == pygame.BUTTON_LEFT:
            mods = pygame.key.get_mods()
            clicked_object = self._get_clicked_object(event.pos)

            if clicked_object:
                self._toggle_object_selection(clicked_object, mods)
            elif not mods & pygame.KMOD_CTRL:
                self._start_box_selection(event.pos, mods)

    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button up events to finalize box selection."""
        mods = pygame.key.get_mods()
        if event.button == pygame.BUTTON_LEFT and not mods & pygame.KMOD_CTRL:
            self._finish_box_selection(event.pos, mods)

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Update the end position of the selection box during mouse motion."""
        if event.buttons[0] and not pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.end_pos = event.pos

    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """Handle key down events, currently only for capturing screenshots."""
        if event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self._capture_screenshot()

    def _get_clicked_object(self, pos: Tuple[int, int]) -> Optional[pygame.sprite.Sprite]:
        """Return the first object at the given position, if any."""
        return next((obj for obj in self.selectable_objects if obj.rect.collidepoint(pos)), None)

    def _toggle_object_selection(self, obj: pygame.sprite.Sprite, mods: int) -> None:
        """Toggle the selection state of an object based on modifier keys."""
        if obj in self.selected_objects:
            if mods & pygame.KMOD_SHIFT:
                self.selected_objects.remove(obj)
        else:
            if not mods & pygame.KMOD_SHIFT:
                self.selected_objects.clear()
            self.selected_objects.add(obj)
        self.select_objects()

    def _start_box_selection(self, pos: Tuple[int, int], mods: int) -> None:
        """Initialize the box selection process."""
        self.start_pos = pos
        if not mods & pygame.KMOD_SHIFT:
            self.selected_objects.clear()
            self.select_objects()

    def _finish_box_selection(self, pos: Tuple[int, int], mods: int) -> None:
        """Finalize the box selection and update selected objects."""
        self.end_pos = pos
        if self.start_pos is not None and self.end_pos is not None:
            rect = self._get_selection_rect()
            objects_in_rect = self._get_objects_in_rect(rect)

            if mods & pygame.KMOD_SHIFT:
                self._toggle_objects_in_rect(objects_in_rect)
            else:
                self.selected_objects = set(objects_in_rect)

            self.select_objects()
        self.start_pos = None
        self.end_pos = None

    def _get_selection_rect(self) -> pygame.Rect:
        """Create a Rect object representing the current selection area."""
        return pygame.Rect(
                min(self.start_pos[0], self.end_pos[0]),
                min(self.start_pos[1], self.end_pos[1]),
                abs(self.end_pos[0] - self.start_pos[0]),
                abs(self.end_pos[1] - self.start_pos[1])
                )

    def _get_objects_in_rect(self, rect: pygame.Rect) -> List[pygame.sprite.Sprite]:
        """Return a list of objects whose centers are within the given rectangle."""
        return [obj for obj in self.selectable_objects if rect.collidepoint(obj.rect.center)]

    def _toggle_objects_in_rect(self, objects: List[pygame.sprite.Sprite]) -> None:
        """Toggle the selection state of objects within the selection rectangle."""
        for obj in objects:
            if obj in self.selected_objects:
                self.selected_objects.remove(obj)
            else:
                self.selected_objects.add(obj)

    def _capture_screenshot(self) -> None:
        """Capture a screenshot of the current selection area."""
        if not self.start_pos or not self.end_pos:
            return

        rect_pos = (min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]))
        rect_size = (abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1] - self.start_pos[1]))
        capture_screenshot(self.window, "tmp.png", (rect_pos, rect_size), rect_size)

    def debug_object(self) -> None:
        """Print the number of selected objects for debugging purposes."""
        print(f"selected_objects: {len(self.selected_objects)}")

    def draw_fancy_lines(self) -> None:
        """Draw lines between the centers of all selected objects."""
        for i in self.selected_objects:
            for ii in self.selected_objects:
                if i is not ii:
                    pygame.draw.line(self.window, colors.ui_dark, i.rect.center, ii.rect.center, 1)

    def draw(self) -> None:
        """Draw the selection rectangle and update the scope."""
        if self.start_pos and self.end_pos and pygame.mouse.get_pressed()[0]:
            rect_pos = (min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]))
            rect_size = (abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1] - self.start_pos[1]))
            pygame.draw.rect(self.window, self.color, (rect_pos, rect_size),
                    config.ui_rounded_corner_small_thickness, config.ui_rounded_corner_radius_small)

        if self.debug:
            self.debug_object()
        self.draw_scope()

    def draw_scope(self) -> None:
        """Draw the scope for selected objects, including range and energy use information."""
        if config.app.weapon_select._hidden:
            for obj in self.selected_objects:
                scope.update_scope(obj.rect.center, obj.get_max_travel_range(),
                        lists=["planets", "ships", "ufos", "collectable_items"])
                if obj.selected:
                    scope.draw_lines_from_startpos_to_mouse_pos(pygame.mouse.get_pos(), obj.rect.center)


                if obj == config.app.ship and obj.selected:

                    # this is a bottle neck !!!
                    scope.draw_range(obj)
                    mouse_pos = pygame.mouse.get_pos()
                    pre_calculated_energy_use = obj.energy_use * math.dist(obj.rect.center, mouse_pos) / pan_zoom_handler.zoom
                    info = {"energy use": format_number(pre_calculated_energy_use, 1)}
                    scope.draw_scope_circles_with_text_and_warning_image(
                            info, mouse_pos, scope.is_in_range(mouse_pos, obj.get_max_travel_range(), obj.rect.center))

    def select_objects(self) -> None:
        """Update the selection state of all selectable objects."""
        for obj in self.selectable_objects:
            obj.select(obj in self.selected_objects)
            # config.app.ship = None

    def listen(self, events: List[pygame.event.Event]) -> None:
        # print (f"box selection, disabled functons:: {disabler} ")
        self.selectable_objects = sprite_groups.ships.sprites()
        """
        Process incoming events to handle box selection and object selection.

        This method is the main entry point for handling user interactions with the selection tool.
        It delegates to specific handler methods based on the event type.
        """
        if self._should_ignore_hover_object():
            return
        self.draw()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                self._handle_key_down(event)
