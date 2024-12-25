import copy
import math

from source.configuration.game_config import config
from source.gui.event_text import event_text


class ScorePlotterHandler:
    """
    The ScorePlotterHandler class is responsible for managing and plotting score data for players in a game.
    It keeps track of the score data for each cycle and provides methods to update and retrieve the score history.

    Example Usage
    # Create an instance of ScorePlotterHandler
    plotter = ScorePlotterHandler()

    # Set the score data for each player
    plotter.set_data()

    # Set the score history for the current cycle
    plotter.set_data_history()

    # Set the score history display for a specific range of cycles
    plotter.set_data_history_display()

    # Get the score history for all cycles
    history = plotter.get_data_history()

    # Get the score history display for the specified range of cycles
    display_history = plotter.get_data_history_display()

    # Calculate the visible range of cycles based on the surface width
    plotter.calculate_visible_x_range(surface_width, plotter_x_pos, plotter_step_x)

    # Reset the score data and history
    plotter.reset()

    # Update the score data and history for the next cycle
    plotter.update()


    Main functionalities:

    -   The main functionalities of the ScorePlotterHandler class are:
    -   Setting the score data for each player
    -   Keeping track of the score history for each cycle
    -   Setting the score history display for a specific range of cycles
    -   Retrieving the score history for all cycles
    -   Retrieving the score history display for a specified range of cycles
    -   Calculating the visible range of cycles based on the surface width
    -   Resetting the score data and history
    -   Updating the score data and history for the next cycle

    Methods:
    __init__(): Initializes the ScorePlotterHandler object with default values for cycles, data, data history,
                data history display, plotter x position, plotter step x, start cycle, and end cycle.

    set_data(): Sets the score data for each player by iterating over the players in the game configuration and storing
                their scores in the data dictionary.

    set_data_history(): Sets the score history for the current cycle by making a copy of the data dictionary and storing
                        it in the data_history dictionary with the current cycle as the key.

    set_data_history_display(): Sets the score history display for a specific range of cycles by filtering the
                                data_history dictionary based on the start and end cycles and storing the filtered data
                                in the data_history_display dictionary.

    get_data_history(): Returns the score history for all cycles by returning the data_history dictionary.

    get_data_history_display(): Returns the score history display for the specified range of cycles by returning the
                                data_history_display dictionary.

    calculate_visible_x_range(surface_width, plotter_x_pos, plotter_step_x): Calculates the visible range of cycles based
            on the surface width, plotter x position, and plotter step x. Updates the start and end cycles accordingly.

    reset(): Resets the cycles, data, data history, and calls set_data() and set_data_history() to update the score data
             and history.

    update():   Updates the score data and history for the next cycle by calling set_data(), set_data_history(),
                and set_data_history_display(). Increments the cycles counter.

    Fields:

    cycles:                 An integer representing the current cycle.
    data:                   A dictionary storing the score data for each player.
    data_history:           A dictionary storing the score history for each cycle.
    data_history_display:   A dictionary storing the score history display for a specific range of cycles.
    plotter_x_pos:          An integer representing the x position of the plotter.
    plotter_step_x:         An integer representing the step size of the plotter on the x-axis.
    start_cycle:            An integer representing the start cycle for the score history display.
    end_cycle:              An integer representing the end cycle for the score history display.
    """

    def __init__(self) -> None:
        self.cycles = 0
        self.data = {}
        self.data_history = {}
        self.data_history_display = {}
        self.plotter_x_pos = 30
        self.plotter_step_x = 5
        self.start_cycle = 0
        self.end_cycle = 1

    def set_data(self) -> None:
        """
        The set_data method in the ScorePlotterHandler class is responsible for setting the score data for each player
        by iterating over the players in the game configuration and storing their scores in the data dictionary.

        Flow:
        Iterate over the players in the game configuration.
        For each player, get the player index and player object.
        Store the player's score in the data dictionary using the player index as the key
        """
        for player_index, player in config.app.players.items():
            self.data[player_index] = player.score

    def set_data_history(self) -> None:
        """
        he set_data_history method in the ScorePlotterHandler class is responsible for storing a copy of the current
        score data in the data_history dictionary, with the current cycle as the key.

        Flow:

        Create a new key-value pair in the data_history dictionary, with the current cycle as the key.
        Copy the current score data from the data dictionary using the copy.copy() method.
        Store the copied score data as the value for the current cycle key in the data_history dictionary.
        """
        self.data_history[self.cycles] = copy.copy(self.data)

    def set_data_history_display(self) -> None:
        """
        The set_data_history_display method in the ScorePlotterHandler class is responsible for creating a filtered
        dictionary of the score history data based on the specified range of cycles.

        Flow:

        Create an empty dictionary data_history_display.
        Iterate over each cycle in the range from start_cycle to end_cycle.
        Check if the cycle exists in the data_history dictionary.
        If the cycle exists, add the cycle as the key and the corresponding score data as the value to the data_history_display dictionary.
        """
        self.data_history_display = {cycle: self.data_history[cycle] for cycle in
                                     range(self.start_cycle, self.end_cycle) if cycle in self.data_history}

    def get_data_history(self) -> dict:
        return self.data_history

    def get_data_history_display(self) -> dict:
        return self.data_history_display

    def calculate_visible_x_range(self, surface_width, plotter_step_x) -> int:
        range_ = int(surface_width / plotter_step_x)

        return range_

    def calculate_start_and_end_cycle(self, plotter_x_pos, plotter_step_x, range_) -> tuple[int, int]:
        offset = math.floor(plotter_x_pos / plotter_step_x)
        start_cycle = -offset
        if start_cycle < 0:
            start_cycle = 0
        end_cycle = range_ - offset
        max_key = max(self.data_history.keys())
        if end_cycle > max_key:
            end_cycle = max_key
        return start_cycle, end_cycle

    def set_start_and_end_cycles(self, surface_width, plotter_x_pos, plotter_step_x) -> None:
        """ make shure the game is running to avoid nasty errors!!! """

        if not score_plotter_handler.data:
            event_text.set_text("No data to plot! start a game first!! ")
            return

        range_ = self.calculate_visible_x_range(surface_width, plotter_step_x)
        self.start_cycle, self.end_cycle = self.calculate_start_and_end_cycle(plotter_x_pos, plotter_step_x, range_)

    def reset(self) -> None:
        """
        The reset method in the ScorePlotterHandler class is responsible for resetting the cycles, data, and data
        history. It also calls the set_data and set_data_history methods to update the score data and history.

        Flow:

        Set the cycles counter to 0.
        Clear the data dictionary.
        Clear the data history dictionary.
        Call the set_data method to update the score data.
        Call the set_data_history method to update the score history.

        """
        self.cycles = 0
        self.data = {}
        self.data_history = {}
        self.set_data()
        self.set_data_history()

    def update(self) -> None:
        """
        The update method in the ScorePlotterHandler class is responsible for updating the score data, score history,
        and score history display for the next cycle.

        Flow:

        Call the set_data method to update the score data for each player.
        Call the set_data_history method to store a copy of the current score data in the score history dictionary.
        Call the set_data_history_display method to create a filtered dictionary of the score history data based on the
        specified range of cycles.
        Increment the cycles counter by 1.
        """
        self.set_data()
        self.set_data_history()
        self.set_data_history_display()
        self.cycles += 1


score_plotter_handler = ScorePlotterHandler()
