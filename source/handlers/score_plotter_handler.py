import copy

from source.configuration.game_config import config


class ScorePlotterHandler:
    def __init__(self):
        self.cycles = 0
        self.data = {}
        self.data_history = {}
        self.data_history_display = {}

    def set_data(self):
        for player_index, player in config.app.players.items():
            self.data[player_index] = player.score

    def set_data_history(self):
        self.data_history[self.cycles] = copy.copy(self.data)

    def get_data_history(self):
        return self.data_history

    def reset(self):
        self.cycles = 0
        self.data = {}
        self.data_history = {}
        self.set_data()
        self.set_data_history()

    def update(self):
        self.set_data()
        self.set_data_history()
        self.cycles += 1


score_plotter_handler = ScorePlotterHandler()
