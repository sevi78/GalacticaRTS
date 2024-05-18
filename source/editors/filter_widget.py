import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image

BUTTON_FONT_SIZE = 15


class FilterWidget(EditorBase):
    def __init__(self, win, x, y, width, height, filters, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.button_size = 15
        #  widgets
        self.widgets = []
        self.buttons = []
        self.icons = []
        self.filters = filters
        self.list_name = kwargs.get("list_name", None)

        # create widgets
        self.create_buttons(self.filters)

        self.hide()

    def create_buttons(self, keys):
        x = 0
        y = 0
        button_size = 15
        for key in keys:
            icon = ImageButton(win=self.win,
                    x=self.get_screen_x() + x,
                    y=self.get_screen_y() + y + TOP_SPACING,
                    width=button_size,
                    height=button_size,
                    isSubWidget=False,
                    parent=self,
                    image=pygame.transform.scale(get_image(f"{key}_icon.png"), (button_size, button_size)),
                    tooltip=key,
                    frame_color=self.frame_color,
                    moveable=False,
                    include_text=True,
                    layer=self.layer,
                    onClick=lambda key_=key: self.select_filter(key_),
                    name=key,
                    textColour=self.frame_color,
                    font_size=BUTTON_FONT_SIZE,
                    info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                    textHAlign="right_outside",
                    outline_thickness=0,
                    outline_threshold=1
                    )

            self.buttons.append(icon)
            self.widgets.append(icon)
            x += button_size

        self.max_height = button_size
        self.screen_width = button_size * len(keys)

    def reposition_widgets(self):
        for icon in self.widgets:
            icon.screen_x = self.world_x + self.button_size * self.widgets.index(icon)
            icon.screen_y = self.world_y + TOP_SPACING

    def select_filter(self, key):
        # store the last key to self for toggling
        if not hasattr(self, key):
            setattr(self, key, False)

        if not getattr(self, key):
            setattr(self, key, True)
        else:
            setattr(self, key, False)

        # Print the key and the current list of widgets for debugging purposes
        print("key:", key)
        print("dict: ", self.parent.widgets)

        # Sort the list of widgets based on the specified key (attribute) in descending order
        sorted_widgets = sprite_groups.convert_sprite_groups_to_image_widget_list(
                self.list_name,
                sort_by=key,
                reverse=getattr(self, key))

        # Update the parent's widgets list with the sorted list
        self.parent.set_widgets(sorted_widgets)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        self.reposition_widgets()
        if not self._hidden and not self._disabled:
            self.draw_frame(corner_radius=5, corner_thickness=1)
