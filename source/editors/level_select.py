import pygame

from source.gui.event_text import event_text
from source.handlers import file_handler
from source.handlers.file_handler import load_file
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.text.info_panel_text_generator import info_panel_text_generator
from source.text.tooltip_gen import tooltip_generator
from source.gui.widgets.buttons.image_button import ImageButton
from source.multimedia_library.images import get_image
from source.configuration import global_params


class LevelSelect(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.max_height = width
        # lists
        self.data = file_handler.get_level_list()

        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        self.create_icons()

        # hide initially
        self.hide()

    def update_icons(self):
        for i in self.buttons:
            if i.name:
                if i.name.startswith("level"):
                    # set image to icon
                    level = i.name.split('_')[1].split('.json')[0]
                    image_name = f"{i.name.split('.json')[0]}{'.png'}"
                    i.setImage(get_image(image_name))

                    # blit success image onto icon image
                    if not int(level) == 0:
                        success = self.parent.level_handler.level_successes[str(int(level) - 1)]
                    else:
                        success = True

                    if not success:
                        size = (i.image.get_rect().width, i.image.get_rect().height)
                        i.image.blit(pygame.transform.scale(get_image("mission_512x512.png"), size), i.image.get_rect())

                        # set tooltip
                        i.tooltip = "You must first successfully colonize the previous solar systems!"
                    else:
                        i.tooltip = "move to this solar systems"


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
            level_dict = load_file(f"level_{level}.json", folder="levels")
            tooltip = ""  # tooltip_generator.create_level_tooltip(level, level_dict)
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

    def select_level(self, i: str):
        # convert level string to int and reduce -1 to make shure the previous level gets checked for success
        level_number = int(i)
        if level_number != 0:
            level_number -= 1

        # check for success of prevoius level
        if self.parent.level_handler.level_successes[str(level_number)]:
            # if success, load level
            self.parent.level_handler.load_level(f"level_{i}.json", "levels")
            self.hide()
            global_params.tooltip_text = ""
        else:
            # complain
            event_text.text = "You must first successfully colonize the previous solar systems!"

        # reset tooltip
        global_params.tooltip_text = ""

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, "Select Level:")
