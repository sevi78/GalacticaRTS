import os.path

import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.file_handler import write_file, abs_games_path, \
    generate_json_filename_based_on_datetime, get_games_list, move_file_to_trash
from source.multimedia_library.images import get_image


class SaveGameEdit(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        #  widgets
        self.widgets = []
        self.games_icons = []
        self.current_game = "not set !"
        self.max_height = 700

        # create widgets
        self.create_save_button(lambda: self.save_game(), "save game", name="save_button")
        self.create_load_button(lambda: self.load_game(self.current_game), "load game", name="load_button")
        self.create_delete_button(lambda: self.delete_game(self.current_game), "delete game, no undo !!!", name="delete_button")
        self.create_games_icons()
        self.create_close_button()

        # self.container = ContainerWidget(
        #     win=self.win,
        #     x=self.get_screen_x(),
        #     y=self.get_screen_y(),
        #     width=self.get_screen_width(),
        #     height=self.get_screen_height(),
        #     widgets=self.games_icons,
        #     function=navigate_to_ship_by_offset_index,
        #     parent=self)

        # hide initially
        self.hide()

    def create_delete_button(self, function, tooltip, **kwargs):
        name = kwargs.get("name", "no_name")
        button_size = 32
        delete_icon = ImageButton(win=self.win,
            x=self.get_screen_x() + self.get_screen_width() / 2 + button_size * 3,
            y=self.max_height + button_size / 2,
            width=button_size,
            height=button_size,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                get_image("uncheck.png"), (button_size, button_size)),
            tooltip=tooltip,
            frame_color=self.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=function,
            name="delete_button"
            )

        self.buttons.append(delete_icon)
        self.widgets.append(delete_icon)

    def delete_games_icons(self):
        # delete all image buttons
        for i in self.games_icons:
            i.__del__()
            self.widgets.remove(i)
            self.buttons.remove(i)
        self.games_icons = []
        # if hasattr(self, "container"):
        #     self.container.widgets = self.games_icons  # Add this line

    def create_games_icons(self):
        self.delete_games_icons()

        # create image buttons
        y = 0
        for i in get_games_list():
            name = i
            button_size = 32

            icon = ImageButton(win=self.win,
                x=self.get_screen_x() + button_size,
                y=self.get_screen_y() + TOP_SPACING + button_size * 3 + y,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(
                    get_image("load_icon.png"), (button_size, button_size)),
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=lambda name_=name: self.set_current_game(name_),
                text=i,
                textColour=self.frame_color,
                textHAlign="left_outside",
                name=name
                )
            y += button_size
            # icon.hide()
            self.max_height = self.get_screen_y() + TOP_SPACING + button_size * 3 + y

            self.buttons.append(icon)
            self.widgets.append(icon)
            self.games_icons.append(icon)
            self.reposition_buttons()
        # if hasattr(self, "container"):
        #     self.container.widgets = self.games_icons  # Add this line

    def set_current_game(self, value):
        self.current_game = value
        self.change_icon_tect_color()

    def change_icon_tect_color(self):
        for i in self.games_icons:
            if i.string == self.current_game:
                i.textColour = pygame.color.THECOLORS["darkgreen"]
                i.text = self.font.render(i.string, True, i.textColour)
            else:
                i.textColour = self.frame_color
                i.text = self.font.render(i.string, True, i.textColour)

    def save_game(self):
        filename = generate_json_filename_based_on_datetime(f"galactica level {self.parent.level_handler.data['globals']['level']} ")
        data = self.parent.level_handler.generate_level_dict_from_scene()
        write_file(filename, "games", data)
        self.create_games_icons()

    def load_game(self, value):
        # self.parent.level_handler.load_level(0, data=load_file(self.current_game, folder="games"), current_game= self.current_game)
        self.parent.level_handler.load_level(self.current_game, "games")
        self.parent.level_handler.current_game = self.current_game
        print(f"load game: {value}")

    def delete_game(self, current_game):
        filename = os.path.join(abs_games_path() + os.sep + current_game)
        move_file_to_trash(filename)
        self.create_games_icons()
        print(f"deleting game: {filename}")

    def reposition_buttons(self):
        button_size = 32
        to_reposition = ["save_button", "load_button", "delete_button"]
        for i in self.buttons:
            if i.name in to_reposition:
                i.screen_y = self.max_height + button_size / 2

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            # self.container.listen(events)
            # self.container.widgets = self.games_icons

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 25, f"Current Game: {self.current_game}")

            # self.container.set_x(self.screen_x)
            # self.container.set_y(self.screen_y)
            # self.container.draw()
