import pygame
from pygame.event import Event
from pygame_widgets import Mouse

from source.configuration import global_params
from source.gui.event_text import event_text

DEFAULT_LAYER = 9


class WidgetHandler:
    layers = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    layer_switch = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
    draw_layers = True
    for key, value in layer_switch.items():
        layer_switch[key] = 1

    def draw_layer(events, layer: int) -> None:
        if not WidgetHandler.draw_layers:
            return

        for key, widgetlist in WidgetHandler.layers.items():
            # if not WidgetHandler.layer_switch[str(layer)]:
            #     return
            if key == layer:
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

    def show_layer(layer_):
        if WidgetHandler.layer_switch[str(layer_)] == 1:
            WidgetHandler.layer_switch[str(layer_)] = 0
        else:
            WidgetHandler.layer_switch[str(layer_)] = 1
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
                        event_text.text = f"changing visibility of WidgetHandler.layer {key}: {WidgetHandler.layer_switch[key]}"
                        return
                    if WidgetHandler.layer_switch[key] == 1:
                        WidgetHandler.layer_switch[key] = 0
                        event_text.text = f"changing visibility of WidgetHandler.layer {key}: {WidgetHandler.layer_switch[key]}"
                        return
                if event.key == pygame.K_z:
                    WidgetHandler.draw_layers = not WidgetHandler.draw_layers


def update(events: [Event]):
    Mouse.updateMouseState()
    WidgetHandler.set_visible(events)
