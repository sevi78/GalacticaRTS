import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.event_text import event_text
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers import file_handler
from source.handlers.file_handler import load_file
from source.multimedia_library.images import get_image
from source.text.info_panel_text_generator import info_panel_text_generator


class LevelSelect(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.max_height = width
        # lists
        self.data = file_handler.get_level_list()

        # display_rect
        self.button_display_rect = pygame.Rect(
                self.world_x + self.text_spacing,
                self.world_y + TOP_SPACING + self.text_spacing * 3,
                self.frame.get_rect().width - self.text_spacing * 2,
                self.frame.get_rect().height - self.text_spacing - (self.text_spacing * 3)
                )

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
        # get data:
        data = sorted(self.data, key=lambda x: int(x.split('_')[1].split('.')[0]))
        item_amount = len(data)
        rows, columns, item_width, item_height = self.calculate_grid(item_amount, self.button_display_rect.width + self.text_spacing * 2, self.button_display_rect.height + self.text_spacing * 2)

        # arrange in rows and colums
        for row in range(rows):
            for col in range(columns):
                item_index = row * columns + col
                if item_index >= item_amount:
                    break

                # get data from item_index
                i = data[item_index]
                level = i.split('_')[1].split('.json')[0]
                level_dict = load_file(f"level_{level}.json", folder="levels")
                tooltip = ""  # tooltip_generator.create_level_tooltip(level, level_dict)
                infotext = info_panel_text_generator.create_create_info_panel_level_text(level, level_dict)

                icon = ImageButton(
                        win=self.win,
                        x=self.get_screen_x() + (col * item_height) + self.text_spacing,
                        y=self.get_screen_y() + (row * item_height) + TOP_SPACING + self.text_spacing * 3,
                        width=item_height,
                        height=item_height,
                        isSubWidget=False,
                        parent=self,
                        image=pygame.transform.scale(get_image(f"{i.split('.json')[0]}.png"), (
                            item_height, item_height)),
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

        # set max_height of editor
        self.max_height = (rows * item_height) + self.text_spacing * 3 + TOP_SPACING

    def select_level(self, i: str):
        # convert level string to int and reduce -1 to make sure the previous level gets checked for success
        previous_level_number = int(i)
        if previous_level_number != 0:
            previous_level_number -= 1

        # check for success of previous level
        if self.parent.level_handler.level_successes[str(previous_level_number)]:
            # if success, load level
            self.parent.level_handler.load_level(f"level_{i}.json", "levels")
            self.hide()
            config.tooltip_text = ""
        else:
            # complain
            event_text.text = "You must first successfully colonize the previous solar systems!"

        # reset tooltip
        config.tooltip_text = ""

        # set config level
        config.level = int(i)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 30, f"Select Level:    (current level: {config.level}) ")

            self.button_display_rect = pygame.Rect(
                    self.world_x + self.text_spacing,
                    self.world_y + TOP_SPACING + self.text_spacing * 3,
                    self.frame.get_rect().width - self.text_spacing * 2,
                    self.frame.get_rect().width - self.text_spacing * 2
                    )

            # pygame.draw.rect(self.win, colors.outside_screen_color, self.button_display_rect, 1)
