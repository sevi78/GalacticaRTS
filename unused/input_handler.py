import pygame
import time

CLICK_DELAY = 0.5


class InputHandler:
    def __init__(self):
        self.inputs = {}
        self.mouse_inputs = {1: "left_mouse_button",
                             2: "middle_mouse_button",
                             3: "right_mouse_button"
                             }

        self.mouse_state = {1: 0,
                            2: 0,
                            3: 0
                            }

        self.double_click_starts = {1: time.time(), 2: time.time(), 3: time.time()}
        self.double_click_delays = {1: 0.5, 2: 0.2, 3: 0.2}

    def __repr__(self):
        return f"InputHandler: {self.mouse_state}"

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
        self.handle_mouse_inputs(events)
        # for event in events:
        #     self.handle_input(event)

    def handle_mouse_input__(self, event):
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

    def handle_mouse_inputs(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_state[event.button] == 0:
                    self.mouse_state[event.button] = 1
                    self.double_click_starts[event.button] = time.time()

                elif self.mouse_state[event.button] == 1:
                    current_time = time.time()
                    start_time = self.double_click_starts[event.button]
                    elapsed_time = current_time - start_time
                    delay = self.double_click_delays[event.button]
                    if elapsed_time < delay:
                        self.mouse_state[event.button] = 2
                        self.double_click_starts[event.button] = time.time()

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_state[event.button] == 2:
                    self.mouse_state[event.button] = 1
                else:
                    self.mouse_state[event.button] = 0

    def is_mouse_button_pressed(self, button):
        return self.mouse_state.get(button, False)

    def reset_mouse_states(self):
        self.mouse_state = {1: 0, 2: 0, 3: 0}


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
        if input_handler.mouse_state.get(1) == 2:
            print(f"Left mouse button is double clicked {input_handler.mouse_state}")

        print(f"clicked {input_handler.mouse_state}")
        pygame.display.flip()

    pygame.quit()
