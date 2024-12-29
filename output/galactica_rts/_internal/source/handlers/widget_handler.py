import pygame
from pygame.event import Event

from source.configuration.game_config import config
from source.gui.event_text import event_text

DEFAULT_LAYER = 9
# background = pygame.Surface(config.win.get_size())
# background.set_alpha(25)

class WidgetHandler:
    layers = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    layer_switch = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
    draw_layers = True
    for key, value in layer_switch.items():
        layer_switch[key] = 1

    def draw_layer(events, layer: int) -> None:
        # if not WidgetHandler.draw_layers:
        #     return

        for key, widgetlist in WidgetHandler.layers.items():
            # if not WidgetHandler.layer_switch[str(layer)]:
            #     return

            # if layer == 4:
            #     config.win.blit(background, (0, 0))

            if key == layer:
                for widget in widgetlist:
                    # need to find the correct coordinates, otherwise not all widgets get drawn, specially celestial obj
                    # if level_of_detail.inside_screen((widget.screen_x, widget.screen_y), border=0):


                    widget.draw()

                    if widget.is_sub_widget:
                        if hasattr(widget, "listen"):
                            widget.listen(events)

    @staticmethod
    def get_all_widgets():
        all_widgets = []
        for layer in WidgetHandler.layers.values():
            all_widgets.extend(layer)
        return all_widgets

    @staticmethod
    def add_widget(widget):
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
        if config.text_input_active:
            return

        if not events:
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
                        event_text.set_text(f"changing visibility of WidgetHandler.layer {key}: {WidgetHandler.layer_switch[key]}")
                        return
                    if WidgetHandler.layer_switch[key] == 1:
                        WidgetHandler.layer_switch[key] = 0
                        event_text.set_text(f"changing visibility of WidgetHandler.layer {key}: {WidgetHandler.layer_switch[key]}")
                        return
                if event.key == pygame.K_z:
                    WidgetHandler.draw_layers = not WidgetHandler.draw_layers


def update(events: [Event]):
    WidgetHandler.set_visible(events)
