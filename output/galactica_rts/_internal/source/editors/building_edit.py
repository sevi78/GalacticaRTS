import ast

import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.factories.building_factory import building_factory
from source.gui.widgets.buttons.button import Button
from source.gui.widgets.inputbox import InputBox
from source.handlers.file_handler import write_file, load_file
from source.multimedia_library.images import get_image

ICON_SIZE = 25
TEXT_HEIGHT = 30


class BuildingEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.input_boxes_value = []
        self.input_boxes_key = []
        self.plus_arrow = None
        self.minus_arrow = None
        self.widgets = []
        self.icons = []
        self.input_boxes = []
        self.enabled_input_boxes = []
        self.active_input_box = None
        self.selectors = []

        # lists
        self.category = None
        self.building = "spring"  # just a default to make shure buttons gets created
        self.category = building_factory.get_category_by_building(self.building)
        self.building_dict = building_factory.get_building_dict_from_buildings_json(self.building)
        self.data = load_file("buildings.json", "config")

        # create widgets
        self.buttonsize = 15
        self.create_close_button()
        self.max_height = 200  # default
        self.create_input_boxes()

        # for some reason this must be called last
        self.create_save_button(lambda: self.save_buildings(), "save buildings")
        # hide initially
        self.hide()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
        # print("BuildingEdit.category.setter:", self.category)

    @property
    def building(self):
        return self._building

    @building.setter
    def building(self, value):
        self._building = value
        self.building_dict = building_factory.get_building_dict_from_buildings_json(self.building)
        self.update_inputboxes_values()

    def update_inputboxes_values(self):
        for key, value in self.building_dict.items():
            for i in self.input_boxes:
                if i.key == key:
                    if i._disabled:
                        if not i in self.input_boxes_value:
                            i.set_text(key)
                        else:
                            i.set_text(str(value))
                    else:
                        i.set_text(str(value))

    def create_input_boxes(self):
        text_height = int(TEXT_HEIGHT / 1.5)
        x = self.world_x + self.text_spacing
        y = self.world_y + TOP_SPACING + self.text_spacing + text_height + self.text_spacing
        input_box_key_width = self.screen_width - self.text_spacing * 6
        input_box_value_width = 160

        for key, value in self.building_dict.items():
            input_box_key = InputBox(self.win, x, y, input_box_key_width, text_height,
                text=key, parent=self, key=key, disabled=True, text_input_type=str, draw_frame=False)
            self.input_boxes_key.append(input_box_key)

            disabled = False
            if type(value) == str:
                disabled = True
            input_box_value = InputBox(self.win, x + input_box_key_width / 2 + self.buttonsize * 2, y, input_box_value_width, text_height,
                text=str(value), parent=self, key=key, text_input_type=type(value), disabled=disabled)

            self.input_boxes_value.append(input_box_value)

            if type(value) == int:
                minus_arrow = Button(win=pygame.display.get_surface(),
                    x=input_box_value.world_x - self.buttonsize,
                    y=input_box_value.world_y,
                    width=self.buttonsize,
                    height=self.buttonsize,
                    isSubWidget=False,
                    image=pygame.transform.scale(
                        get_image("arrow-left.png"), (self.buttonsize, self.buttonsize)),
                    frame_color=self.frame_color,
                    transparent=True,
                    parent=input_box_value,
                    layer=self.layer,
                    name="minus_arrow",
                    addition_value=1
                    )

                plus_arrow = Button(win=pygame.display.get_surface(),
                    x=input_box_value.world_x + input_box_value_width / 2,
                    y=input_box_value.world_y,
                    width=self.buttonsize,
                    height=self.buttonsize,
                    isSubWidget=False,
                    image=pygame.transform.scale(
                        get_image("arrow-right.png"), (self.buttonsize, self.buttonsize)),
                    frame_color=self.frame_color,
                    transparent=True,
                    parent=input_box_value,
                    layer=self.layer,
                    name="plus_arrow",
                    addition_value=-1
                    )

                self.buttons.append(minus_arrow)
                self.buttons.append(plus_arrow)
                self.widgets.append(minus_arrow)
                self.widgets.append(plus_arrow)

            self.widgets.append(input_box_key)
            self.input_boxes.append(input_box_key)
            self.widgets.append(input_box_value)
            self.input_boxes.append(input_box_value)
            y += text_height

        self.max_height = y + text_height
        self.enabled_input_boxes = [_ for _ in self.input_boxes if not _._disabled]

    def update_input_boxes(self, events):
        for i in self.input_boxes:
            i.update()
            i.handle_events(events)

    def get_input_box_values(self, obj, key, value):
        try:
            # Try to evaluate the value as a Python expression
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            # If the value is not a valid Python expression, keep it as a string
            pass
            # print(f"get_input_box_values:{ValueError},{SyntaxError}  unable to eval string: {value}")

        # Set the value into the dictionary
        self.building_dict[key] = value

    def select_next_input_box(self, event):
        if event.key == pygame.K_TAB:
            active_input_boxes = [_ for _ in self.enabled_input_boxes if _.active]
            if len(active_input_boxes) == 0:
                return

            self.active_input_box = [_ for _ in self.enabled_input_boxes if _.active][0]
            index = self.enabled_input_boxes.index(self.active_input_box)
            next_index = (index + 1) % len(self.enabled_input_boxes)
            self.active_input_box.active = False
            self.active_input_box = self.enabled_input_boxes[next_index]
            self.active_input_box.active = True

            for i in self.input_boxes:
                if self.active_input_box == i:
                    i.active = True

    def listen(self, events):
        self.update_input_boxes(events)
        self.handle_hovering()
        self.drag(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.select_next_input_box(event)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200,
                TEXT_HEIGHT, f"Building Edit: {self.category}")

    def save_buildings(self):
        self.data[self.category][self.building] = self.building_dict
        write_file("buildings.json", "config", self.data)
