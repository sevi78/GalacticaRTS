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
PLOTTER_X_POS_DEFAULT = 30
PLOTTER_STEP_X_DEFAULT = 5
PLOTTER_Y_FACTOR_DEFAULT = 1


class ScorePlotter(EditorBase):
    """
    Plotter for the score.

    The ScorePlotter class is a subclass of EditorBase and is used to plot the score data on a surface.
    It allows for customization of the plotter's appearance and behavior through selectors.

    Example Usage
    # Create a ScorePlotter object
    plotter = ScorePlotter(win, x, y, width, height)

    # Set the step size for the plotter
    plotter.selector_callback("step_x", 5, plotter.selector_step_x)

    # Set the y factor for the plotter
    plotter.selector_callback("y_factor", 50, plotter.selector_y_factor)

    # Set the x position for the plotter
    plotter.selector_callback("plotter_x_pos", 0, plotter.selector_plotter_x_pos)

    # Draw the plotter surface
    plotter.draw_plotter_surface()
    Code Analysis
    Main functionalities
    Creates a plotter surface to display the score data.
    Allows customization of the plotter's appearance and behavior through selectors.
    Draws the score lines on the plotter surface based on the data history.
    Handles the calculation of the visible range of the plotter surface.

    Methods
    __init__(self, win, x, y, width, height, **kwargs): Initializes the ScorePlotter object with the specified
    parameters and sets up the plotter surface and selectors.
    create_selectors(self): Creates the selectors for step size, y factor, and x position.
    selector_callback(self, key, value, selector): Callback function called from the selectors to update the plotter's
    properties based on the selected values.
    draw_score_lines(self): Draws the score lines on the plotter surface based on the data history.
    draw_plotter_surface(self): Draws the plotter surface with the score lines.

    Fields
    plotter_surface: Surface object representing the plotter surface.
    selectors: List of Selector objects for customizing the plotter's properties.
    plotter_step_x: Step size for the plotter.
    y_factor: Factor for scaling the y-axis of the plotter.
    plotter_x_pos: X position of the plotter.
    parent: Parent object that contains the ScorePlotter object.
    max_height: Maximum height of the plotter surface.
    font_size: Font size for the text on the plotter surface.
    font: Font object for rendering the text on the plotter surface.
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        EditorBase.__init__(self, win, x, y, width, height, isSubWidget=False, **kwargs)
        self.plotter_surface = pygame.surface.Surface((
            width - PLOTTER_SURFACE_GAP, PLOTTER_SURFACE_HEIGHT))

        self.rect = self.plotter_surface.get_rect()
        self.max_height = PLOTTER_SURFACE_HEIGHT
        self.font_size = 12
        self.font = pygame.font.SysFont(config.font_name, self.font_size - 1)
        self.last_drawn_x = 0

        # selectors
        self.selectors = []
        self.editors = []
        self.selector_plotter_x_pos = None
        self.selector_step_x = None
        self.selector_y_factor = None
        self.plotter_step_x = 5
        self.plotter_step_x_list = [_ for _ in range(1, 500, 1)]
        self.plotter_x_pos_list = [_ for _ in range(-100000, 100000, 10)]
        self.plotter_x_pos = 0
        self.y_factor = 0.5
        self.y_factor_list = [_ for _ in range(1, 1000)]
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
                {"list_name": "step_x_list", "list": self.plotter_step_x_list},
                self,
                FONT_SIZE)
        self.selector_step_x.current_value = PLOTTER_STEP_X_DEFAULT

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
        self.selector_y_factor.current_value = PLOTTER_Y_FACTOR_DEFAULT
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
                FONT_SIZE,
                restrict_list_jump=True,
                repeat_clicks=True)
        self.selector_plotter_x_pos.current_value = PLOTTER_X_POS_DEFAULT
        self.selector_plotter_x_pos.show()

        # set score plotter handler default values
        score_plotter_handler.plotter_x_pos = PLOTTER_X_POS_DEFAULT
        score_plotter_handler.plotter_step_x = PLOTTER_STEP_X_DEFAULT

    def selector_callback(self, key, value, selector):
        """ this is the selector_callback function called from the selector to return the values to the editor:

            The selector_callback method is called from a selector object to update the properties of the ScorePlotter
            object based on the selected values. It updates the step size, y factor, and x position of the plotter,
            and then calculates the visible range of the plotter surface.

            Flow:

            Check the value of the key parameter to determine which property is being updated.
            Update the corresponding property of the ScorePlotter object with the new value.
            Update the corresponding property of the score_plotter_handler object with the new value.
            Print the updated key, value, and selector for debugging purposes.
            Call the calculate_visible_x_range method of the score_plotter_handler object to recalculate the visible
            range of the plotter surface.

        """
        if key == "step_x":
            self.plotter_step_x = value
            score_plotter_handler.plotter_step_x = value
            # print(f"{key}: {value}, {selector}")

        if key == "y_factor":
            self.y_factor = 1 / value
            # print(f"{key}: {value}, {selector}")

        if key == "plotter_x_pos":
            self.plotter_x_pos = value
            score_plotter_handler.plotter_x_pos = value  # + self.plotter_step_x
            # score_plotter_handler.set_x_pos(value)
            # print(f"{key}: {value}, {selector}")

        score_plotter_handler.calculate_visible_x_range(self.plotter_surface.get_width(), self.plotter_x_pos, self.plotter_step_x)

    def adjust_x_pos(self, endpos_x):  # not working :(
        if endpos_x > self.plotter_surface.get_width():
            self.selector_plotter_x_pos.set_current_value(self.selector_plotter_x_pos.current_value - self.plotter_step_x)
            self.plotter_x_pos = self.selector_plotter_x_pos.current_value
            # self.selector_callback("plotter_x_pos", self.selector_plotter_x_pos.current_value, self.selector_plotter_x_pos)
            # self.selector_plotter_x_pos.current_value -=1
            # self.plotter_x_pos = self.selector_plotter_x_pos.current_value
            # score_plotter_handler.plotter_x_pos = self.plotter_x_pos

    def adjust_step_x(self, endpos_x):  # doestnt work either
        if endpos_x > self.plotter_surface.get_width():
            self.selector_step_x.set_current_value(self.selector_step_x.current_value - 1)
            self.selector_callback("step_x", self.selector_step_x.current_value, self.selector_step_x)

    def adjust_y_factor(self, endpos_y):
        if endpos_y < 0.0:
            self.selector_y_factor.set_current_value(self.selector_y_factor.current_value + 1)
            self.selector_callback("y_factor", self.selector_y_factor.current_value, self.selector_y_factor)
            # self.y_factor = 1 / self.selector_y_factor.current_value

    def draw_score_lines(self):
        """
        he draw_score_lines method is responsible for drawing the score lines on the plotter surface based on the data
        history. It calculates the start and end positions for each line and draws them using the pygame.draw.line
        function.

        Flow:

        Calculate the x and y positions for drawing the score lines.
        Iterate over the data history, which contains the score data for each cycle.
        For each cycle, iterate over the player dictionary, which contains the score for each player.
        Check if there is a previous point to draw from by comparing the cycle to 0.
        If there is a previous point, calculate the start and end positions for the line based on the previous score and
        the current score.
        Draw the line using the pygame.draw.line function, with the color based on the player index.
        If the cycle is a multiple of 5, draw the cycle number as text on the plotter surface.
        Otherwise, draw a dot as text on the plotter surface.
        """
        x = self.plotter_surface.get_rect().x + self.plotter_x_pos
        y = self.plotter_surface.get_rect().bottom - 30

        for cycle, player_dict in score_plotter_handler.get_data_history_display().items():
            # calculate x position
            start_pos_x = x + (cycle - 1) * self.plotter_step_x

            # for every player
            for player_index, score in player_dict.items():
                if cycle > 0:  # Ensure there is a previous point to draw from
                    # Check if the previous cycle and player index exist in the data
                    if ((cycle - 1) in score_plotter_handler.data_history_display
                            and player_index in score_plotter_handler.data_history_display[cycle - 1]):
                        # calculate y position
                        start_pos_y = y - score_plotter_handler.data_history_display[cycle - 1][
                            player_index] * self.y_factor
                        endpos_x = x + (cycle * self.plotter_step_x)
                        endpos_y = y - (score * self.y_factor)

                        # draw lines
                        pygame.draw.line(
                                self.plotter_surface,
                                player_handler.get_player_color(player_index),
                                (start_pos_x, start_pos_y),
                                (endpos_x, endpos_y),
                                1)

                        # y_factor to make all visible
                        # self.adjust_x_pos(endpos_x)
                        # self.adjust_step_x(endpos_x)
                        self.adjust_y_factor(endpos_y)

            # draw grid
            if cycle % 5 == 0:
                self.draw_text(start_pos_x, self.plotter_surface.get_rect().bottom - 15, 20, 12, str(cycle), win=self.plotter_surface, font=self.font)
            else:
                self.draw_text(start_pos_x, self.plotter_surface.get_rect().bottom - 15, 20, 12, ".", win=self.plotter_surface, font=self.font)



    def draw_plotter_surface(self):
        """
        The draw_plotter_surface method is responsible for drawing the plotter surface on the screen.
        It fills the surface with a dark color, draws a frame around it, and then calls the draw_score_lines method to
        draw the score lines on the surface. Finally, it blits the plotter surface onto the main window at the specified
        position.

        Flow:
        Fill the plotter surface with a dark color.
        Draw a frame around the plotter surface using the specified frame color.
        Call the draw_score_lines method to draw the score lines on the plotter surface.
        Blit the plotter surface onto the main window at the specified position

        """
        self.plotter_surface.fill((15, 15, 15))
        pygame.draw.rect(self.plotter_surface, self.frame_color, self.plotter_surface.get_rect(), 1, 3)
        self.draw_score_lines()
        self.win.blit(self.plotter_surface, (self.world_x, self.world_y))

    def draw(self):
        if not self._hidden and not self._disabled:
            score_plotter_handler.calculate_visible_x_range(self.plotter_surface.get_width(), self.plotter_x_pos, self.plotter_step_x)
            self.draw_plotter_surface()
