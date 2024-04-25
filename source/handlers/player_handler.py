import os

from source.configuration.game_config import config
from source.game_play.player import Player
from source.handlers.file_handler import load_file


class PlayerHandler:
    def __init__(self):
        self.players = {}
        self.player_colors = {-1: "green", 0: "blue", 1: "red", 2: "orange", 3: "yellow", 4: "pink", 5: "purple"}
        self.player_image_names = {}
        self.get_player_image_names()

    def get_player_colors(self, data):
        self.player_colors = {"-1": "green"}
        for key, value in data.items():
            self.player_colors[key] = value["color"]

    def get_player_image_names(self):
        # setup image dict
        self.player_image_names = {}
        for player_name, dict_ in self.get_players().items():
            for key, value in dict_.items():
                if key == 'image_name':
                    self.player_image_names[player_name] = value

    def create_players(self, data):
        for key, value in list(data.items()):
            player_id = data[key]["player"]
            self.players[player_id] = Player(
                name=data[key]["name"],
                species=data[key]["species"],
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
                owner=player_id,
                enemies=data[key]["enemies"],
                )

            # set active (human) player
            config.app.player = self.players[0]

    def load_players(self) -> None:
        file = load_file("players.json", "config")

        for key, value in file.items():
            self.players["player_" + key] = value

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

    def get_player_color(self, value: int) -> str:
        return self.player_colors[value]

    def reset_players(self):
        config.app.create_players(self.get_players())
        # self.create_players(self.get_players())
        # players = self.get_players()
        #
        # self.create_players(players)
        # setattr(config.app, "auto_economy_edit", None)
        # setattr(config.app, "player", config.app.players[0])

    def set_players_data(self, data):
        if "players" in data.keys():
            for key, value in data["players"].items():
                config.app.players[int(key)].stock = value["stock"]
                config.app.players[int(key)].population = value["population"]

        else:
            print(f"could not found key : 'players' in data!, needs to be in the players dict of the level or game_file!!")


player_handler = PlayerHandler()
