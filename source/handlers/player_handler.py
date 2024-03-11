import os

from source.configuration.game_config import config
from source.handlers.file_handler import load_file, abs_players_path




class PlayerHandler:
    def __init__(self):
        self.players = {}
        self.load_players()
        self.player_colors = {-1: "green", 0: "blue", 1: "red", 2: "orange", 3: "yellow"}

    def load_players(self) -> None:
        for file in os.listdir(abs_players_path()):
            self.players[file.split('.')[0]] = load_file(file, "players")

    def get_players(self) -> dict:
        if not self.players:
            self.load_players()
        return self.players

    def get_current_production(self, player):
        if player is str:
            player = config.app.players.index(player)
        return config.app.players[player].production

    def get_current_stock(self, player):
        return config.app.players[player].get_stock()

    def get_player_color(self, value):
        return self.player_colors[value]


player_handler = PlayerHandler()
