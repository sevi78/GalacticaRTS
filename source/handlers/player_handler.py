import os

from source.configuration.game_config import config
from source.game_play.player import Player
from source.handlers.file_handler import load_file, abs_players_path


class PlayerHandler:
    def __init__(self):

        self.data = load_file("players.json", "")
        self.players = {}
        self.player_colors = {-1: "green", 0: "blue", 1: "red", 2: "orange", 3: "yellow", 4: "pink", 5: "purple"}
        # self.create_players(self.data)

    def get_player_colors(self, data):
        self.player_colors = {"-1": "green"}
        for key, value in data.items():
            self.player_colors[key] = value["color"]

    def create_players__(self, data):
        for key, value in data.items():
            player_id = data[key]["player"]
            self.players[player_id] = Player(
                name=data[key]["name"],
                color=self.get_player_color(player_id),
                stock={
                    "energy": 1000,
                    "food": 1000,
                    "minerals": 1000,
                    "water": 1000,
                    "technology": 1000,
                    "population": 0
                    },
                production={
                    "energy": 0,
                    "food": 0,
                    "minerals": 0,
                    "water": 0,
                    "technology": 0,
                    "population": 0
                    },
                clock=0,
                owner=player_id
                )

        # set active (human) player
        self._human_player = self.players[0]
        # config.app.player = self.players[0]


    def create_players(self, data):# does not work : runtime error
        for key, value  in data.items():
            player_id = data[key]["player"]
            self.players[player_id] = Player(
                name=data[key]["name"],
                color=player_handler.get_player_color(player_id),
                stock={
                    "energy": 1000,
                    "food": 1000,
                    "minerals": 1000,
                    "water": 1000,
                    "technology": 1000,
                    "population": 0
                    },
                production={
                    "energy": 0,
                    "food": 0,
                    "minerals": 0,
                    "water": 0,
                    "technology": 0,
                    "population": 0
                    },
                clock=0,
                owner=player_id
                )

            # set active (human) player
            self.human_player = self.players[0]
            config.app.player = self.players[0]

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

    def reset_players(self):
        config.app.create_players(self.get_players())
        # players = self.get_players()
        #
        # self.create_players(players)
        setattr(config.app, "auto_economy_edit", None)
        setattr(config.app, "player", config.app.players[0])


player_handler = PlayerHandler()
