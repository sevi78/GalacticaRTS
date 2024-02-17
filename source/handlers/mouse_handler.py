import time
from enum import Enum

import pygame

from source.handlers.pan_zoom_sprite_handler import sprite_groups


class MouseState(Enum):
    HOVER = 0
    LEFT_CLICK = 1
    MIDDLE_CLICK = 2
    RIGHT_CLICK = 3
    LEFT_DRAG = 4
    RIGHT_DRAG = 5
    LEFT_RELEASE = 6
    RIGHT_RELEASE = 7
    MIDDLE_RELEASE = 8
    MIDDLE_DRAG = 9
    MOUSE_WHEEL_UP = 10
    MOUSE_WHEEL_DOWN = 11


class MouseHandler:
    def __init__(self):
        self.double_click_starts = {1: 0, 2: 0, 3: 0}
        self.double_click_delays = {1: 0.5, 2: 0.5, 3: 0.5}  # 0.5 seconds for double-click
        self.double_clicks = None
        self.mouse_states = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self._mouse_state = None
        self.button_names = {1: "left", 2: "middle", 3: "right", 4: "mouse_wheel", 5: "double_clicks"}

    def update_mouse_state(self):
        leftPressed, middlePressed, rightPressed = pygame.mouse.get_pressed()

        if leftPressed:
            if self._mouse_state == MouseState.LEFT_CLICK or self._mouse_state == MouseState.LEFT_DRAG:
                self._mouse_state = MouseState.LEFT_DRAG
            else:
                self._mouse_state = MouseState.LEFT_CLICK

        elif middlePressed:
            if self._mouse_state == MouseState.MIDDLE_CLICK or self._mouse_state == MouseState.MIDDLE_DRAG:
                self._mouse_state = MouseState.MIDDLE_DRAG
            else:
                self._mouse_state = MouseState.MIDDLE_CLICK

        elif rightPressed:
            if self._mouse_state == MouseState.RIGHT_CLICK or self._mouse_state == MouseState.RIGHT_DRAG:
                self._mouse_state = MouseState.RIGHT_DRAG
            else:
                self._mouse_state = MouseState.RIGHT_CLICK
        else:
            if self._mouse_state == MouseState.LEFT_CLICK or self._mouse_state == MouseState.LEFT_DRAG:
                self._mouse_state = MouseState.LEFT_RELEASE

            elif self._mouse_state == MouseState.MIDDLE_CLICK or self._mouse_state == MouseState.MIDDLE_DRAG:
                self._mouse_state = MouseState.MIDDLE_RELEASE

            elif self._mouse_state == MouseState.RIGHT_CLICK or self._mouse_state == MouseState.RIGHT_DRAG:
                self._mouse_state = MouseState.RIGHT_RELEASE

            else:
                if self.mouse_states[4] == -1:
                    self._mouse_state = MouseState.MOUSE_WHEEL_DOWN
                elif self.mouse_states[4] == 1:
                    self._mouse_state = MouseState.MOUSE_WHEEL_UP
                else:
                    self._mouse_state = MouseState.HOVER

    def get_mouse_states(self, **kwargs):
        format_ = kwargs.get("format", None)
        if not format_:
            return self.mouse_states
        else:
            return {self.button_names[key]: self.mouse_states[key] for key in self.mouse_states}

    def get_mouse_state(self):
        return self._mouse_state

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def handle_mouse_inputs(self, events):
        for event in events:
            # if clicked something in the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if event is a button (left, middle, right)
                if event.button in [1, 2, 3]:
                    # set mouse states
                    if self.mouse_states[event.button] == 0:
                        # one time clicked
                        self.mouse_states[event.button] = 1
                        self.double_click_starts[event.button] = time.time()
                    else:
                        current_time = time.time()
                        start_time = self.double_click_starts[event.button]
                        elapsed_time = current_time - start_time
                        delay = self.double_click_delays[event.button]
                        if elapsed_time < delay:
                            # Double-click detected
                            self.double_clicks = event.button
                            self.mouse_states[5] = event.button
                            # Reset state after double-click
                            self.mouse_states[event.button] = 0
                        else:
                            # Not a double-click, reset timer
                            self.double_click_starts[event.button] = time.time()

            # if click released something in the mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                # check if event is a button (left, middle, right)
                if event.button in [1, 2, 3]:
                    if self.mouse_states[event.button] == 1:
                        current_time = time.time()
                        start_time = self.double_click_starts[event.button]
                        elapsed_time = current_time - start_time
                        delay = self.double_click_delays[event.button]
                        if elapsed_time >= delay:
                            # Too much time has passed; it's not a double-click
                            self.mouse_states[event.button] = 0

                    self.double_clicks = None
                    self.mouse_states[5] = 0

            # if mousewheel is used
            elif event.type == pygame.MOUSEWHEEL:
                self.mouse_states[4] = event.y
                if event.y > 0:
                    self._mouse_state = MouseState.MOUSE_WHEEL_DOWN
                else:
                    self._mouse_state = MouseState.MOUSE_WHEEL_UP

            else:
                self.mouse_states[4] = 0

        # update states
        self.update_mouse_state()

    def get_hit_object(self, **kwargs: {list}) -> object or None:
        filter = kwargs.get("filter", [])
        # lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        lists = ["planets", "ships", "ufos", "collectable_items", "celestial_objects"]
        if filter:
            lists -= filter

        for list_name in lists:
            if hasattr(sprite_groups, list_name):
                for obj in getattr(sprite_groups, list_name):
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        return obj
            # else:
            #     hitables = [i for i in [_ for _ in WidgetHandler.get_all_widgets() if hasattr(_, "type")] if i.type == "asteroid"]
            #     for obj in hitables:
            #         if obj.rect.collidepoint(pygame.mouse.get_pos()):
            #             return obj
        return None


mouse_handler = MouseHandler()

# # Example usage
# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode((640, 480))
#     running = True
#     mouse_handler = MouseHandler()
#
#     while running:
#         events = pygame.event.get()
#         mouse_handler.handle_mouse_inputs(events)
#         # print (mouse_handler.get_mouse_state())
#
#         # print (mouse_handler.mouse_states[4] if not mouse_handler.mouse_states[4] == 0 else "")
#         # print (mouse_handler.mouse_states[4])
#         # if mouse_handler.double_clicks:
#         #     print (f"mouse_handler: double_clicks {mouse_handler.double_clicks}")
#
#         #print(mouse_handler.get_mouse_states(format=True))
#         print (mouse_handler.get_mouse_state())
#
#         for event in events:
#             if event.type == pygame.QUIT:
#                 running = False
#
#         pygame.display.flip()
#
#     pygame.quit()
