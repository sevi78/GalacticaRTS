from source.configuration.game_config import config
from source.handlers.file_handler import load_file


class PlayerHandler:
    def __init__(self):
        self.players = {}
        self.load_players()
        self.player_colors = {-1: "green", 0: "blue", 1: "red", 2: "orange", 3: "yellow", 4: "pink", 5: "purple"}
        self.player_image_names = {}
        self.get_player_image_names()

    def get_player_colors(self, data):
        # self.player_colors = {"-1": "green"}
        for key, value in data.items():
            self.player_colors[key] = value["color"]

    def get_player_color(self, value: int) -> str:
        return self.player_colors[value]

    def get_player_image_names(self):
        # setup image dict
        self.player_image_names = {}
        for player_name, dict_ in self.get_players().items():
            for key, value in dict_.items():
                if key == 'image_name':
                    self.player_image_names[player_name] = value

    def load_players(self, **kwargs) -> None:
        """ this is terrible !!!"""
        # reset self players
        self.players = {}

        # get the file
        file = load_file("players.json", "config")

        # get the data
        data = kwargs.get("data", {})

        # delete unused players
        if data:
            new_dict = {}
            for key, value in file.items():
                if key in data.keys():
                    new_dict[key] = value
            file = new_dict

        # refill
        for key, value in file.items():
            self.players["player_" + key] = value

    def get_players(self) -> dict:
        if hasattr(config.app, "level_handler"):
            # self.load_players(data=config.app.level_handler.data["players"])
            self.load_players(data=config.app.level_handler.data["players"])
        return self.players

    def get_current_production(self, player):
        if player is str:
            player = config.app.players.index(player)
        return config.app.players[player].production

    def get_current_stock(self, player):
        return config.app.players[player].get_stock()

    def reset_players(self):
        config.app.create_players(self.get_players())

    def set_players_data(self, data: dict) -> None:
        """
        this function is used to update the players data:

        from level_handler:

        '0': {'stock': {'energy': 8500, 'food': 9000, 'minerals': 8500, 'water': 9750, 'technology': 9500, 'population': 0}, 'population': 0, 'enemies': [1, 2, 3]},
        '1': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'population': 0, 'enemies': [0]},
        '2': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'population': 0, 'enemies': [0]},
        '3': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'population': 0, 'enemies': []},
        '4': {'stock': {'energy': 1000, 'food': 1000, 'minerals': 1000, 'water': 1000, 'technology': 1000, 'population': 0}, 'population': 0, 'enemies': []}}

        from server:

        {'function': 'set_players_data', 'data':
         {'players': {'0': {'stock': {'energy': 8500, 'food': 9000, 'minerals': 8500, 'water': 9750, 'technology': 9500, 'population': 0}, 'enemies': [1, 2, 3]}, '1': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'enemies': [0]}, '2': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'enemies': [0]}, '3': {'stock': {'energy': 10000, 'food': 10000, 'minerals': 10000, 'water': 10000, 'technology': 10000, 'population': 0}, 'enemies': []}, '4': {'stock': {'energy': 1000, 'food': 1000, 'minerals': 1000, 'water': 1000, 'technology': 1000, 'population': 0}, 'enemies': []}}}}


        """
        if "players" in data.keys():
            for key, value in data["players"].items():
                if not int(key) in config.app.players.keys():
                    print(f"player_handler.set_players_data: player {key} not found in players dict")
                    continue
                config.app.players[int(key)].stock = value["stock"]
                config.app.players[int(key)].enemies = value["enemies"]
                if "score" in value.keys():
                    config.app.players[int(key)].score = value["score"]
                # config.app.players[int(key)].population = value["population"]

        else:
            print(f"could not found key : 'players' in data!, needs to be in the players dict of the level or game_file!!")

    def update_network_players(self) -> None:

        """
        players": {
        "0": {
            "stock": {
                "energy": 8500,
                "food": 9000,
                "minerals": 8500,
                "water": 9750,
                "technology": 9500,
                "population": 0
            },
            "population": 0,
            "enemies": [
                1,
                2,
                3
            ]
        },

        """
        data = {"players": {}}

        for key, player in config.app.players.items():
            data["players"][key] = {}
            data["players"][key]["stock"] = player.get_stock()
            data["players"][key]["enemies"] = player.enemies
            data["players"][key]["score"] = player.score

        config.app.game_client.send_message({"f": "set_players_data", "data": data})


player_handler = PlayerHandler()
