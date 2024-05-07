import pygame

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.gui.widgets.selector import Selector
from source.handlers.player_handler import player_handler
from source.handlers.score_plotter_handler import score_plotter_handler

ARROW_SIZE = 20
FONT_SIZE = int(ARROW_SIZE * .8)
SELECTOR_SPACING = 100
PLOTTER_SURFACE_HEIGHT = 500
PLOTTER_SURFACE_GAP = 10


class ScorePlotter(EditorBase):
    """
    Plotter for the score.
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.plotter_surface = pygame.surface.Surface((
            width - PLOTTER_SURFACE_GAP, PLOTTER_SURFACE_HEIGHT))

        self.rect = self.plotter_surface.get_rect()
        self.max_height = PLOTTER_SURFACE_HEIGHT
        self.font_size = 12
        self.font = pygame.font.SysFont(config.font_name, self.font_size - 1)

        # selectors
        self.selectors = []
        self.editors = []
        self.selector_plotter_x_pos = None
        self.selector_step_x = None
        self.selector_y_factor = None
        self.step_x = 5
        self.step_x_list = [_ for _ in range(1, 50)]
        self.plotter_x_pos_list = [_ for _ in range(-10000, 10000, 10)]
        self.plotter_x_pos = 0
        self.y_factor = 0.5
        self.y_factor_list = [_ for _ in range(1, 50)]
        self.create_selectors()

        # register
        self.parent.editors.append(self)

        # hide initially
        self.hide()

    def create_selectors(self):
        x = self.world_x + self.world_width / 2 - ARROW_SIZE / 2
        y = self.world_y + self.plotter_surface.get_rect().height + 60
        self.selector_step_x = Selector(
                self.win,
                x,
                y,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "step_x_list", "list": self.step_x_list},
                self,
                FONT_SIZE)
        self.selector_step_x.current_value = 10
        self.selector_step_x.show()

        self.selector_y_factor = Selector(
                self.win,
                x,
                y - 20,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "y_factor_list", "list": self.y_factor_list},
                self,
                FONT_SIZE)
        self.selector_y_factor.current_value = 50
        self.selector_y_factor.show()

        self.selector_plotter_x_pos = Selector(
                self.win,
                x,
                y - 40,
                ARROW_SIZE,
                self.frame_color,
                9,
                SELECTOR_SPACING,
                {"list_name": "plotter_x_pos_list", "list": self.plotter_x_pos_list},
                self,
                FONT_SIZE)
        self.selector_plotter_x_pos.current_value = 0
        self.selector_plotter_x_pos.show()

    def selector_callback(self, key, value, selector):
        """this is the selector_callback function called from the selector to return the values to the editor"""
        # if key == "step_x":
        #     self.step_x = value
        #     print(f"{key}: {value}, {selector}")

        if key == "y_factor":
            self.y_factor = 1 / value
            print(f"{key}: {value}, {selector}")

        # if key == "plotter_x_pos":
        #     self.plotter_x_pos = value
        #     # score_plotter_handler.set_x_pos(value)
        #     print(f"{key}: {value}, {selector}")

        if key in ["step_x", "plotter_x_pos"]:
            getattr(self, f"selector_{key}").current_value = value
            start_cycle, end_cycle = self.calculate_visible_range()
            score_plotter_handler.update_data_history_display(start_cycle, end_cycle)
            self.draw_plotter_surface()

        # start_cycle, end_cycle = self.calculate_visible_range()
        # score_plotter_handler.update_data_history_display(start_cycle, end_cycle)
        # self.draw_plotter_surface()

    def calculate_visible_range(self):
        width = self.plotter_surface.get_width()
        start_cycle = max(0, int((-self.plotter_x_pos) / self.step_x))
        end_cycle = start_cycle + int(width / self.step_x) + 1

        pygame.draw.line(self.win, self.frame_color, (start_cycle, 20), (end_cycle, 20))
        return start_cycle, end_cycle

    def draw_score_lines__(self):
        x = self.plotter_surface.get_rect().x + self.plotter_x_pos
        y = self.plotter_surface.get_rect().bottom - 30

        for cycle, player_dict in score_plotter_handler.get_data_history().items():
            # calculate x position
            start_pos_x = x + (cycle - 1) * self.step_x

            # for every player
            for player_index, score in player_dict.items():
                if cycle > 0:  # Ensure there is a previous point to draw from

                    # calculate y position
                    start_pos_y = y - score_plotter_handler.data_history[cycle - 1][player_index] * self.y_factor
                    endpos_x = x + (cycle * self.step_x)
                    endpos_y = y - (score * self.y_factor)

                    # draw lines
                    pygame.draw.line(
                            self.plotter_surface,
                            player_handler.get_player_color(player_index),
                            (start_pos_x, start_pos_y),
                            (endpos_x, endpos_y),
                            1)

            # draw grid
            if cycle % 5 == 0:
                self.draw_text(start_pos_x, self.plotter_surface.get_rect().bottom - 15, 20, 12, str(cycle), win=self.plotter_surface, font=self.font)
            else:
                self.draw_text(start_pos_x, self.plotter_surface.get_rect().bottom - 15, 20, 12, ".", win=self.plotter_surface, font=self.font)

    def draw_score_lines(self):
        x = self.plotter_surface.get_rect().x + self.plotter_x_pos
        y = self.plotter_surface.get_rect().bottom - 30

        for cycle, player_dict in score_plotter_handler.get_data_history_display().items():
            start_pos_x = x + (cycle - 1) * self.step_x

            for player_index, score in player_dict.items():
                if cycle > 0 and (cycle - 1) in score_plotter_handler.get_data_history_display().items():
                    start_pos_y = y - score_plotter_handler.get_data_history_display()[cycle - 1][
                        player_index] * self.y_factor
                    endpos_x = x + (cycle * self.step_x)
                    endpos_y = y - (score * self.y_factor)

                    pygame.draw.line(
                            self.plotter_surface,
                            player_handler.get_player_color(player_index),
                            (start_pos_x, start_pos_y),
                            (endpos_x, endpos_y),
                            1)

    def draw_plotter_surface(self):
        self.plotter_surface.fill((15, 15, 15))
        pygame.draw.rect(self.plotter_surface, self.frame_color, self.plotter_surface.get_rect(), 1, 3)
        self.draw_score_lines()
        self.win.blit(self.plotter_surface, (self.world_x, self.world_y))

    def draw(self):
        if not self._hidden and not self._disabled:
            self.draw_plotter_surface()


# propmt
"""
we have two classes: score_plotter_handler and score_plotter. score_plotter draws the content of score_plotter_handler.data_history. i want you to write functions that allows to limit the data displayed on screen. based on score_plotter.step_x and score_plotter.plotter_x_pos. the amount of cycles loaded should be determined. use score_plotter_handler.data_history_display to store only the data that is visible on score_plotter.plotter_surface, based on score_plotter.step_x and score_plotter.plotter_x_pos
"""
