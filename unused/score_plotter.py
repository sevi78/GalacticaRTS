from pprint import pprint

import pygame

from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import ARROW_SIZE, FONT_SIZE, TOP_SPACING
from source.gui.widgets.buttons.image_button import ImageButton
from source.handlers.player_handler import player_handler
from source.handlers.score_plotter_handler import score_plotter_handler
from source.multimedia_library.images import get_image

BUTTONSIZE = 20
SPACING_X = 25
LEGEND_LINE_WIDTH = 60


class ScorePlotter(EditorBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)

        self.data = player_handler.get_players()


        self.zero_point = [self.world_x + self.world_width, self.world_y + self.world_height - TOP_SPACING]
        #  widgets
        self.widgets = []

        # create widgets
        self.create_close_button()
        self.create_player_buttons()
        # self.create_save_button(lambda: self.save_font(self.current_font), "save font")

        # hide initially
        # self.hide()

        # set max_height, important to remove the default value of 200 after create_widgets() !!!
        # otherwise the display is terribly wrong !!
        # self.max_height = 800
        self.show()

    def create_player_buttons(self):
        BUTTONSIZE = 20
        h = BUTTONSIZE + 3
        x = 0
        y = TOP_SPACING
        SPACING_X = 25

        # Define the desired order of keys including 'name' and 'color'
        order = ["name", "color", "water", "energy", "food", "minerals", "technology", "population"]
        production_order = ["production_" + key for key in order if key not in ["name", "color"]]
        all_keys = order + production_order

        # Create a new dictionary with ordered keys for each player
        ordered_data = {
            player: {key: self.data[player][key] for key in all_keys if key in self.data[player]}
            for player in self.data
            }

        # define filter
        resources = ["water", "energy", "food", "minerals", "technology", "population"]

        # create items
        for player in ordered_data.keys():
            player_index = int(player.split("_")[1])

            # create player image button
            image_name = player_handler.player_image_names[player]

            icon = ImageButton(win=self.win,
                x=self.world_x + int(SPACING_X),
                y=self.world_y + TOP_SPACING + y,
                width=BUTTONSIZE,
                height=BUTTONSIZE,
                isSubWidget=False,
                parent=self,
                image=pygame.transform.scale(get_image(image_name), (BUTTONSIZE, BUTTONSIZE)),
                tooltip=player,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                onClick=lambda: print("no function"),
                name=player_handler.get_player_color(player_index),
                textColour=self.frame_color,
                font_size=12,
                info_text="",  # info_panel_text_generator.create_info_panel_weapon_text(key),
                textHAlign="right_outside",
                outline_thickness=0,
                outline_threshold=1
                )

            self.buttons.append(icon)
            self.widgets.append(icon)

            y += h

        self.max_height = self.world_y + y

    def draw_legend_lines(self):
        for i in self.buttons:
            if i.name in player_handler.player_colors.values():
                # draw lines for legend
                pygame.draw.line(
                    self.win,
                    i.name,
                    (i.world_x + i.world_width, i.rect.centery),
                    (i.world_x + LEGEND_LINE_WIDTH, i.rect.centery),
                    3)

    def draw_score_lines(self):
        self.zero_point = [self.rect.x, self.rect.y + self.rect.height - TOP_SPACING]
        x, y = self.zero_point
        step_x = 10

        for cycle, player_dict in score_plotter_handler.data_history.items():
            for player_index, score in player_dict.items():
                if cycle > 0:  # Ensure there is a previous point to draw from
                    pygame.draw.line(
                        self.win,
                        player_handler.get_player_color(player_index),
                        (x + ((cycle - 1) * step_x),
                         y - score_plotter_handler.data_history[cycle - 1][player_index]),  # Previous score point
                        (x + (cycle * step_x), y - score),  # Current score point
                        1)

    def update(self):
        pprint(f"ScorePlotter.update: {score_plotter_handler.update()}")

    def listen(self, events):
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, 15, "ScorePlotter:")
            self.draw_legend_lines()
            self.draw_score_lines()


"""
this function:
    def draw_score_lines(self):
        x,y  = self.zero_point
        step_x = 10

        for cycle, player_dict in score_plotter_handler.data_history.items():
            for player_index, score in player_dict.items():

                pygame.draw.line(
                    self.win,
                    player_handler.get_player_color(player_index),
                    (x + (cycle-1 * step_x), y + score),
                    (x + (cycle * step_x), y),
                    1)
                    
should plot the data from :
('ScorePlotter.update: {0: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, 1: {0: 0, 1: 43, 2: '
 '0, 3: 0, 4: 0}, 2: {0: 0, 1: 43, 2: 0, 3: 0, 4: 0}, 3: {0: 0, 1: 43, 2: 0, '
 '3: 0, 4: 0}, 4: {0: 0, 1: 43, 2: 0, 3: 0, 4: 0}, 5: {0: 0, 1: 43, 2: 0, 3: '
 '0, 4: 0}, 6: {0: 0, 1: 43, 2: 0, 3: 0, 4: 0}, 7: {0: 0, 1: 43, 2: 0, 3: 0, '
 '4: 0}, 8: {0: 0, 1: 20, 2: 0, 3: 0, 4: 0}, 9: {0: 0, 1: 19, 2: 0, 3: 0, 4: '
 '0}, 10: {0: 0, 1: 18, 2: 0, 3: 0, 4: 0}, 11: {0: 0, 1: 17, 2: 0, 3: 0, 4: '
 '0}}')
 
 into lines using pygame.draw.line()
 the first level of the dict are the cycles. the keys of the second level are the player_indexes. the corresponding values are the scores
 fix it !

"""