import os
import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.multimedia_library.images import get_image


class LevelSelect(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        # lists
        self.data = self.get_data()

        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        self.create_icons()

        # hide initially
        self.hide()
        self.max_height = width

    def get_data(self):
        """
        Get a list of all files in the database directory which starts with "level_".

        Parameters:
        database_directory (str): The path to the database directory.

        Returns:
        list: A list of filenames that start with "level_".
        """
        try:
            # Get the path of the file the code is written
            current_file_path = os.path.abspath(__file__)

            # Go back two directories
            database_path = os.path.abspath(os.path.join(current_file_path, '..', '..', '..', 'database'))

            file_list = [file for file in os.listdir(database_path) if file.startswith("level_")]
            return file_list
        except Exception as e:
            print("An error occurred: ", e)
            return []

    def create_icons(self):
        rows = 3
        columns = 3
        button_size = 190
        tooltip = "select level"
        x = 0
        y = 0
        for index, i in enumerate(self.data):
            icon = ImageButton(win=self.win,
                x=self.get_screen_x() + x + self.text_spacing * 3,
                y=self.get_screen_y() + y + TOP_SPACING + self.text_spacing * 3,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(get_image(f"{i.split('.json')[0]}.png"), (button_size, button_size)),
                tooltip=f"{tooltip} {i.split('_')[1].split('.json')[0]}",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=lambda index=index: self.select_level(index),  # Capture the current value of i
                name=i
                )

            self.buttons.append(icon)
            self.widgets.append(icon)

            x += button_size  # Move to the next column

            # Reset x and increment y to start a new row
            if (index + 1) % columns == 0:
                x = 0
                y += button_size

    def select_level(self, i):
        self.parent.level_edit.load_level(i)
        self.hide()

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Select Level:")
