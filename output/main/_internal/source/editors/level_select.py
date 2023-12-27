import os
import pygame

from source.database.file_handler import load_file
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.text.info_panel_text_generator import info_panel_text_generator
from source.text.tooltip_gen import tooltip_generator
from source.gui.widgets.buttons.image_button import ImageButton
from source.multimedia_library.images import get_image
from source.utils import global_params


class LevelSelect(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.max_height = width
        # lists
        self.data = self.get_data()

        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        self.create_icons()

        # hide initially
        self.hide()

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

    def update_icons(self):
        for i in self.buttons:
            if i.name:
                if i.name.startswith("level"):
                    image_name = f"{i.name.split('.json')[0]}{'.png'}"
                    i.setImage(get_image(image_name))

                    print("update_icons", image_name)

    def create_icons(self):
        rows = 3
        columns = 3
        max_button_height = pygame.display.get_surface().get_height() - (TOP_SPACING + self.text_spacing * 3)
        available_height = max_button_height - (rows - 1) * self.text_spacing * 3
        max_button_size = available_height // rows
        button_size = min(190, max_button_size)  # Set the initial button size
        data = sorted(self.data, key=lambda x: int(x.split('_')[1].split('.')[0]))
        x = self.text_spacing * 3  # Add a border on the left
        y = self.text_spacing * 3  # Add a border on the top

        for index, i in enumerate(data):
            level = i.split('_')[1].split('.json')[0]
            level_dict = load_file(f"level_{level}.json")
            tooltip = tooltip_generator.create_level_tooltip(level, level_dict)
            infotext = info_panel_text_generator.create_create_info_panel_level_text(level, level_dict)

            icon = ImageButton(win=self.win,
                x=self.get_screen_x() + x,
                y=self.get_screen_y() + y + TOP_SPACING,
                width=button_size,
                height=button_size,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(get_image(f"{i.split('.json')[0]}.png"), (button_size, button_size)),
                tooltip=tooltip,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=lambda level_=level: self.select_level(level_),
                name=i,
                text=level,
                textColour=self.frame_color,
                font_size=50,
                info_text=infotext,
                info_panel_alpha=255
                )
            self.buttons.append(icon)
            self.widgets.append(icon)

            x += button_size  # Add the button size and the border for the next column

            # Reset x and increment y to start a new row
            if (index + 1) % columns == 0:
                x = self.text_spacing * 3  # Reset x to add the border on the left for the new row
                y += button_size  # Add the button size and the border for the next row

        # Calculate the max height based on the number of icons created
        self.max_height = 900  # self.world_y + 200 + min(y + button_size + self.text_spacing * 3, max_button_height)

    def select_level(self, i):
        self.parent.level_edit.load_level(i)
        self.hide()
        global_params.tooltip_text = ""

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Select Level:")
