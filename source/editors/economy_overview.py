import copy
from collections import OrderedDict

import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.handlers.file_handler import load_file
from source.multimedia_library.images import get_image

BUTTON_SIZE = 30


class EconomyOverview(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        #  widgets
        self.widgets = []
        self.buttons = []

        # create widgets
        self.create_close_button()

        self.data = load_file("buildings.json", "config")
        # hide initially
        self.hide()

        # self.create_buttons()
        self.max_height = 1000

    def draw_buildings__(self):
        data = OrderedDict(self.data)
        for building_name, dict_ in data.items():
            pos = (self.world_x + (BUTTON_SIZE * 2 * list(data).index(building_name)), self.world_y + 200)
            size = (BUTTON_SIZE, BUTTON_SIZE)
            image = get_image(f"{building_name}_25x25.png")
            self.draw_image(pos, size, image)
            for key, value in dict_.items():
                image = get_image(f"{key}_25x25.png")
                pos = (self.world_x + (BUTTON_SIZE * 2 * list(data[building_name]).index(key)) * list(
                        data[building_name]).index(key),
                       self.world_y + (BUTTON_SIZE * 2 * list(data[building_name]).index(key)))
                size = (BUTTON_SIZE, BUTTON_SIZE)
                self.draw_image(pos, size, image)

    def draw_buildings(self):
        x_lines = [1920 / n for n in range(1, 10)]
        y_lines = [1080 / n for n in range(1, 10)]

        data = OrderedDict(self.data)
        for index, (building_name, dict_) in enumerate(data.items()):
            pos = (x_lines[0], y_lines[index])
            size = (BUTTON_SIZE, BUTTON_SIZE)
            image = get_image(f"{building_name}_25x25.png")
            self.draw_image(pos, size, image)

            for key_index, (key, value) in enumerate(dict_.items()):
                image = get_image(f"{key}_25x25.png")
                pos = (x_lines[key_index + 1],
                       y_lines[index])
                self.draw_image(pos, size, image)

    # def create_buttons(self):
    #     y = self.world_y
    #     x = self.world_x
    #     for building_name in self.data.keys():
    #         button =  ImageButton(win=self.win,
    #         x=self.world_x + x,
    #         y=y - BUTTON_SIZE,
    #         width=BUTTON_SIZE,
    #         height=BUTTON_SIZE,
    #         is_sub_widget=False,
    #         parent=self,
    #         image=pygame.transform.scale(
    #             get_image(f"{building_name}_25x25.png"), (BUTTON_SIZE, BUTTON_SIZE)),
    #         tooltip="",  # "show ships",
    #         frame_color=self.frame_color,
    #         moveable=False,
    #         include_text=True, layer=10,
    #         on_click=lambda: None,
    #         name=building_name)
    #         x += BUTTON_SIZE * 1.5
    #         self.buttons.append(button)
    #         self.widgets.append(button)

    def draw_image(self, pos, size, image, **kwargs):

        offset_x = kwargs.get("offset_x", 0)
        offset_y = kwargs.get("offset_y", 0)

        image_copy = copy.copy(image)
        new_image = pygame.transform.scale(image_copy, size)
        image_rect = new_image.get_rect()
        pos = pos[0] + offset_x, pos[1] + offset_y
        image_rect.center = pos
        self.win.blit(new_image, image_rect)

    def listen(self, events):
        self.handle_hovering()
        self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_buildings()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Economy:")
