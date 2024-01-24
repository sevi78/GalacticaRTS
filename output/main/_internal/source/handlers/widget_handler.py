from pprint import pprint

import pygame
from pygame.event import Event
from pygame_widgets import Mouse

from source.configuration import global_params


class WidgetHandler:
    """Main functionalities:
    The WidgetHandler class is responsible for managing and displaying widgets in a layered manner.
    It allows for widgets to be added to specific layers and for layers to be toggled on and off using keyboard input.
    The class also provides a method for retrieving all widgets currently being managed.

    Methods:
    - main(events): the main method of the class, responsible for iterating through all widgets and drawing them to the
      screen. It also listens for input to toggle layers on and off.
    - get_all_widgets(): returns a list of all widgets currently being managed.
    - addWidget(widget): adds a widget to the appropriate layer.
    - set_visible(events): listens for input to toggle layers on and off.

    Fields:
    - layers: a dictionary containing lists of widgets for each layer.
    - layer_switch: a dictionary containing a binary value for each layer,
      indicating whether the layer is currently visible or not."""

    print("WidgetHandler: init")
    layers = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: []}
    layer_switch = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0}

    for key, value in layer_switch.items():
        layer_switch[key] = 1

    layer_switch["2"] = 0
    layer_switch["10"] = 0

    """
    layers: 
    0 = background
    1 = universe
    2 = 
    3 = planets
    4 = 
    5 = fog of war
    6 = 
    7 =
    8 = ships
    9 = ui 
    10 = tooltip
    """

    @staticmethod
    def main(events: [Event]) -> None:
        # WidgetHandler.set_visible(events)
        # 0:[...]
        #pprint (WidgetHandler.layers.items())
        for key, widgetlist in WidgetHandler.layers.items():
            #print (f"layer: {key}\n widgetlist: {[_.name for _ in widgetlist]}")
            # get widget
            for widget in widgetlist:
                widget.draw()

                if widget.isSubWidget:
                    if hasattr(widget, "listen"):
                        widget.listen(events)

    @staticmethod
    def get_all_widgets():
        all_widgets = []
        for layer in WidgetHandler.layers.values():
            all_widgets.extend(layer)
        return all_widgets

    @staticmethod
    def addWidget(widget):
        if str(widget.layer) == "None":
            WidgetHandler.layers[9].append(widget)
        else:
            WidgetHandler.layers[widget.layer].append(widget)

    def remove_widget(obj):
        for key, widgetlist in WidgetHandler.layers.items():
            # get widget
            for widget in widgetlist:
                if widget == obj:
                    widgetlist.remove(widget)

    def set_visible(events):
        numbers = [49, 50, 51, 52, 53, 54, 55, 56, 57, 48]
        others = [39]  # ,94]
        key = None
        # ignore all inputs while any text input is active
        if global_params.text_input_active:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                # 1-0
                if event.key in numbers:
                    number = event.key - 48
                    key = str(number)

                    # set value
                    if WidgetHandler.layer_switch[key] == 0:
                        WidgetHandler.layer_switch[key] = 1
                        return
                    if WidgetHandler.layer_switch[key] == 1:
                        WidgetHandler.layer_switch[key] = 0
                        return
                if event.key == pygame.K_z:
                    if WidgetHandler.layer_switch[str(9)] == 1:
                        WidgetHandler.layer_switch[str(9)] = 0
                    else:
                        WidgetHandler.layer_switch[str(9)] = 1
                # next

                # elif event.key in others:
                #     key = "9"
                #
                #     # set value
                #     if WidgetHandler.layer_switch[key] == 0:
                #         WidgetHandler.layer_switch[key] = 1
                #         return
                #     if WidgetHandler.layer_switch[key] == 1:
                #         WidgetHandler.layer_switch[key] = 0
                #         return


def update(events: [Event]):
    """Objective:
    The 'update' function is responsible for updating the state of the mouse and managing and displaying widgets using
    the 'WidgetHandler' class. Its main objective is to provide an interface for updating the GUI elements of a game
    or application.

    Inputs:
    - events: a list of pygame events that have occurred since the last update.

    Flow:
    1. Call the 'updateMouseState' method of the 'Mouse' class to update the state of the mouse.
    2. Call the 'main' method of the 'WidgetHandler' class to manage and display widgets based on the provided events.

    Outputs:
    None

    Additional aspects:
    - The 'update' function assumes that the 'Mouse' and 'WidgetHandler' classes have been properly initialized
      and imported.
    - The 'update' function is typically called once per game loop iteration to update the GUI elements of the game or
      application."""
    Mouse.updateMouseState()
    WidgetHandler.main(events)
