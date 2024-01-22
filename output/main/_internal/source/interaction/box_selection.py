import pygame

from source.configuration import global_params
from source.handlers.color_handler import colors
from source.configuration.global_params import ui_rounded_corner_small_thickness

"""
code generated by perplexity.ai, what an amazing tool!!!
"""


class BoxSelection:
    """
    Full Explanation
    The BoxSelection class is used to implement a box selection tool in a Pygame window. It takes two parameters in its
    constructor: window, which represents the Pygame window, and selectable_objects, which is a list of objects that can
    be selected.

    The class has several methods:

    draw_fancy_lines(): This method is used to draw lines between the selected objects. It iterates over the selected
    objects and draws a line between each pair of objects using the pygame.draw.line() function.

    draw(): This method is used to draw the box selection on the Pygame window. It checks if the mouse button is pressed
    and if the start and end positions of the selection are defined. If so, it calculates the position and size of the
    rectangle based on the start and end positions, and draws the rectangle using the pygame.draw.rect() function.

    check_selection(): This method is used to check which objects are selected within the box selection. It creates a
    pygame.Rect object based on the start and end positions of the selection, and then checks if each object's image
    rectangle intersects with the selection rectangle using the colliderect() method. The selected objects are stored
    in a list and returned.

    select_objects(): This method is used to select the objects within the box selection. It iterates over the selected
    objects and calls their select() method with True as the argument to indicate that they are selected. It also
    iterates over all the selectable objects and calls their select() method with False as the argument to indicate that
     they are not selected.

    deselect_objects(): This method is used to deselect the objects within the box selection. It takes a list of
    selected objects as a parameter. It iterates over the selected objects and toggles their selected attribute.
    If an object is not selected, it is removed from the selected_objects list. If an object is selected,
    it is added to the selected_objects list.

    listen(): This method is used to listen for events and update the box selection accordingly. It takes a list of
    events as a parameter. It first calls the draw() method to draw the box selection. Then, it iterates over the events
    and checks the type of each event. If the left mouse button is pressed and the Ctrl key is not held down, it sets
    the start position of the selection to the current mouse position. If the left mouse button is released and the
    Ctrl and Shift keys are not held down, it sets the end position of the selection to the current mouse position,
    calculates the correct start and end positions based on the minimum and maximum values, checks the selected objects
    using the check_selection() method, and selects the objects using the select_objects() method.
    If the left mouse button is released and the Shift key is held down, it checks the selected objects using the
    check_selection() method and deselects the objects using the deselect_objects() method. Finally,
    it resets the start and end positions of the selection.

    The BoxSelection class also has attributes for the selected objects, start position, end position, and color of the
    box selection.
    The __repr__() method returns the length of the selected_objects list when the BoxSelection object is printed.
    """

    def __init__(self, window, selectable_objects):
        self.window = window
        self.selectable_objects = selectable_objects
        self.selected_objects = set()
        self.start_pos = None
        self.end_pos = None
        self.frame_color = colors.frame_color
        self.color = self.frame_color

    def __repr__(self):
        return str(len(self.selected_objects))

    def draw_fancy_lines(self):
        """
        This method is used to draw lines between the selected objects. It iterates over the selected
        objects and draws a line between each pair of objects using the pygame.draw.line() function.
        """
        for i in self.selected_objects:
            for ii in self.selected_objects:
                if i is not ii:
                    pygame.draw.line(self.window, colors.ui_dark, i.center, ii.center, 1)

    def draw(self):
        """
        This method is used to draw lines between the selected objects. It iterates over the selected
        objects and draws a line between each pair of objects using the pygame.draw.line() function.
        """
        if self.start_pos is not None and self.end_pos is not None and pygame.mouse.get_pressed()[0]:
            rect_pos = (min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]))
            rect_size = (abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1] - self.start_pos[1]))
            pygame.draw.rect(self.window, self.color, (
                rect_pos,
                rect_size), int(ui_rounded_corner_small_thickness), int(global_params.ui_rounded_corner_radius_small))

        # self.draw_fancy_lines()

    def check_selection(self):
        """
        This method is used to check which objects are selected within the box selection. It creates a
        pygame.Rect object based on the start and end positions of the selection, and then checks if each object's image
        rectangle intersects with the selection rectangle using the colliderect() method. The selected objects are
        stored in a list and returned.
        """

        if self.start_pos is not None and self.end_pos is not None:
            rect = pygame.Rect(min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]),
                abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1] - self.start_pos[1]))
            selected_objects = [obj for obj in self.selectable_objects if rect.colliderect(obj.rect)]
            return selected_objects
        else:
            return []

    def select_objects(self):
        """
        This method is used to select the objects within the box selection. It iterates over the selected
        objects and calls their select() method with True as the argument to indicate that they are selected. It also
        iterates over all the selectable objects and calls their select() method with False as the argument to indicate
        that they are not selected.
        """
        # select or deselect
        [selected.select(True) for selected in self.selected_objects]
        [other.select(False) for other in self.selectable_objects if other not in self.selected_objects and other != global_params.app.ship]

        # set selected planet
        selected_planets = [i for i in self.selected_objects if i.property == "planet"]

        if len(selected_planets) > 0:
            global_params.app.set_selected_planet(selected_planets[0])

    def deselect_objects(self, selected):
        """
        This method is used to deselect the objects within the box selection. It takes a list of
        selected objects as a parameter. It iterates over the selected objects and toggles their selected attribute.
        If an object is not selected, it is removed from the selected_objects list. If an object is selected,
        it is added to the selected_objects list.
        """
        for obj in selected:
            if obj in self.selected_objects:
                obj.selected = not obj.selected
                if not obj.selected:
                    self.selected_objects.remove(obj)
            else:
                obj.selected = True
                self.selected_objects.append(obj)

    def listen(self, events):
        """
        This method is used to listen for events and update the box selection accordingly. It takes a list of
        events as a parameter. It first calls the draw() method to draw the box selection. Then, it iterates over the
        events and checks the type of each event. If the left mouse button is pressed and the Ctrl key is not held down,
        it sets the start position of the selection to the current mouse position. If the left mouse button is released
        and the Ctrl and Shift keys are not held down, it sets the end position of the selection to the current mouse
        position, calculates the correct start and end positions based on the minimum and maximum values, checks the
        selected objects using the check_selection() method, and selects the objects using the select_objects() method.
        If the left mouse button is released and the Shift key is held down, it checks the selected objects using the
        check_selection() method and deselects the objects using the deselect_objects() method. Finally,
        it resets the start and end positions of the selection.
        """
        self.draw()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and not pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.start_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                mods = pygame.key.get_mods()
                if event.button == pygame.BUTTON_LEFT and not mods & pygame.KMOD_CTRL and not mods & pygame.KMOD_SHIFT:
                    self.end_pos = event.pos
                    if self.start_pos is not None and self.end_pos is not None:
                        self.start_pos = (
                            min(self.start_pos[0], self.end_pos[0]), min(self.start_pos[1], self.end_pos[1]))
                        self.end_pos = (
                            max(self.start_pos[0], self.end_pos[0]), max(self.start_pos[1], self.end_pos[1]))

                    self.selected_objects = self.check_selection()
                    self.select_objects()

                if event.button == pygame.BUTTON_LEFT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    selected = self.check_selection()
                    self.deselect_objects(selected)

                self.start_pos = None
                self.end_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] and not pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.end_pos = event.pos

#
# # Set up the display
# pygame.init()
# win = pygame.display.set_mode((640, 480))
# pygame.display.set_caption("Box Selection_perpl_2")
#
# # Create objects to select from
# class SelectableObject:
#     def __init__(self, rect):
#         self.rect = rect
#     def draw(self, surface):
#         pygame.draw.rect(surface, (0, 0, 255), self.rect)
#
# objects = [SelectableObject(pygame.Rect(100, 100, 50, 50)),
#            SelectableObject(pygame.Rect(200, 200, 50, 50)),
#            SelectableObject(pygame.Rect(300, 300, 50, 50))]
#
# # Create an instance of the BoxSelection class
# box_selection = BoxSelection(win)
#
# # Main game loop
# running = True
# while running:
#     # Clear the screen
#     win.fill((255, 255, 255))
#     events = pygame.event.get()
#     box_selection.listen(events)
#     box_selection.draw()
#
#     for event in events:
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Draw the objects
#     for obj in objects:
#         obj.draw(win)
#
#     # Update the screen
#     pygame.display.update()
#
# # Quit the game
# pygame.quit()