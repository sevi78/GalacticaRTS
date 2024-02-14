# import time
# from enum import Enum
#
# import pygame
# from pygame import QUIT
#
#
# # class MouseState(Enum):
# #     HOVER = 0
# #     LEFT_CLICK = 1
# #     MIDDLE_CLICK = 2  # New state for middle click
# #     RIGHT_CLICK = 3
# #     LEFT_DRAG = 4
# #
# #
# #     RIGHT_DRAG = 5
# #     MIDDLE_DRAG = 6
# #     RELEASE = 6
# #     RIGHT_RELEASE = 7
# #     MIDDLE_RELEASE = 8  # New state for middle release
# #     DOUBLE_CLICK = 20
#
# class InputHandler:
#     def __init__(self):
#         self.inputs = {}
#         self.mouse_inputs ={1: "left_mouse_button",
#                             2: "middle_mouse_button",
#                             3: "right_mouse_button"
#                             }
#
#         self.mouse_state = {1: {"left_mouse_button": False},
#                             2: {"middle_mouse_button": False},
#                             3: {"right_mouse_button": False}
#                             }
#
#         self.left_mouse_button_pressed = 0
#         self.middle_mouse_button_pressed = 0
#         self.right_mouse_button_pressed = 0
#
#         self.left_double_click_start_time = time.time()
#         self.left_double_click_delay = 0.2
#
#     def __repr__(self):
#         return f"InputHandler:left_mouse_button_pressed: {self.left_mouse_button_pressed}, middle_mouse_button_pressed: {self.middle_mouse_button_pressed}, right_mouse_button_pressed: {self.right_mouse_button_pressed}"
#
#     def handle_input(self, event):
#         if event.type == pygame.KEYDOWN:
#             self.inputs[event.key] = True
#         elif event.type == pygame.KEYUP:
#             self.inputs[event.key] = False
#
#     def is_key_down(self, key):
#         return self.inputs.get(key, False)
#
#     def update(self, events):
#         for event in events:
#             self.handle_input(event)
#             self.handle_mouse_input(events)
#         # print (f"update: {self.inputs}")
#
#
#
#
#     def handle_mouse_input__(self, events):
#         for event in events:
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     self.left_mouse_button_pressed += 1
#
#
#                 if event.button == 2:
#                     self.middle_mouse_button_pressed += 1
#
#                 if event.button == 3:
#                     self.right_mouse_button_pressed += 1
#
#             if event.type == pygame.MOUSEBUTTONUP:
#                 if event.button == 1:
#                     if self.left_mouse_button_pressed == 1:
#                         if time.time() - self.left_double_click_start_time < self.left_double_click_delay:
#                             print ("double click")
#                             self.left_mouse_button_pressed = 0
#                             self.left_double_click_start_time = time.time()
#                         else:
#                             self.left_mouse_button_pressed = 0
#                             self.left_double_click_start_time = time.time()
#
#
#                 if event.button == 2:
#                     self.middle_mouse_button_pressed += 1
#
#                 if event.button == 3:
#                     self.right_mouse_button_pressed += 1
#
#
#
#         print("event.button", self)
#
#
# input_handler = InputHandler()
#
#
# class App:
#     def __init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((640, 480))
#         self.running = True
#
#     def run(self):
#         while self.running:
#             input_handler.update(pygame.event.get())
#
#             pygame.display.get_surface().fill((0, 0, 0))
#
#             for event in pygame.event.get():
#
#                 if event.type == QUIT:
#                     self.running = False
#                     pygame.quit()
#
#             pygame.display.flip()
#
#
# if __name__ == '__main__':
#     app = App()
#     # value_smoother_x = ValueSmoother(VALUE_SMOOTHING_FACTOR)
#     # value_smoother_y = ValueSmoother(VALUE_SMOOTHING_FACTOR)
#     input_handler = InputHandler()
#     app.run()


import pygame
import time

class InputHandler:
    def __init__(self):
        self.inputs = {}
        self.mouse_inputs = {1: "left_mouse_button",
                             2: "middle_mouse_button",
                             3: "right_mouse_button"}

        self.mouse_state = {1: False,
                            2: False,
                            3: False}

        self.left_mouse_button_pressed = 0
        self.middle_mouse_button_pressed = 0
        self.right_mouse_button_pressed = 0

        self.left_double_click_start_time = time.time()
        self.left_double_click_delay = 0.2

    def __repr__(self):
        return f"InputHandler:left_mouse_button_pressed: {self.left_mouse_button_pressed}, middle_mouse_button_pressed: {self.middle_mouse_button_pressed}, right_mouse_button_pressed: {self.right_mouse_button_pressed}"

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.inputs[event.key] = True
        elif event.type == pygame.KEYUP:
            self.inputs[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_input(event)

    def is_key_down(self, key):
        return self.inputs.get(key, False)

    def update(self, events):
        for event in events:
            self.handle_input(event)

    def handle_mouse_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_state[event.button] = True
            if event.button == 1:
                self.left_mouse_button_pressed += 1
            elif event.button == 2:
                self.middle_mouse_button_pressed += 1
            elif event.button == 3:
                self.right_mouse_button_pressed += 1

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_state[event.button] = False
            if event.button == 1:
                if self.left_mouse_button_pressed == 1:
                    if time.time() - self.left_double_click_start_time < self.left_double_click_delay:
                        print("double click")
                    self.left_mouse_button_pressed = 0
                self.left_double_click_start_time = time.time()
            elif event.button == 2:
                self.middle_mouse_button_pressed = 0
            elif event.button == 3:
                self.right_mouse_button_pressed = 0

    def is_mouse_button_pressed(self, button):
        return self.mouse_state.get(button, False)

    def reset_mouse_states(self):
        self.mouse_state = {1: False, 2: False, 3: False}
        self.left_mouse_button_pressed = 0
        self.middle_mouse_button_pressed = 0
        self.right_mouse_button_pressed = 0

# Example usage
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    running = True
    input_handler = InputHandler()

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        input_handler.update(events)
        pygame.display.flip()

    pygame.quit()
