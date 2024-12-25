import time
import uuid
from typing import Any


class Game:
    def __init__(self, host_id, level_id, max_players, players, state, start_time, data, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.host_id = host_id
        self.level_id = level_id
        self.max_players = max_players
        self.players = players
        self.state = state
        self.start_time = start_time
        self.data = data

    def to_dict(self):
        return {
            "id": self.id,
            "host_id": self.host_id,
            "level_id": self.level_id,
            "max_players": self.max_players,
            "players": self.players,
            "state": self.state,
            "start_time": self.start_time,
            "data": self.data
            }

    def get_player_status_str(self) -> str:
        """
        'players': {'0': {'ready': True}, '1': {'ready': False}
        """
        str_ = ""
        for key, value in self.players.items():
            str_ += f"Player {key} is ready!  " if value["ready"] else f"Player {key} is not ready!  "

        return str_

    def get_container_widget_string(self) -> tuple[str, Any]:
        str_ = f"Game id: {self.id},    " \
               f"Host: {self.host_id},    " \
               f"Level: {self.level_id},    " \
               f"Max players: {self.max_players},    " \
               f"Players: {self.get_player_status_str()}    "

        if self.state == "starting":
            countdown = round(self.start_time - time.time(), 1)
            if countdown > 0:
                str_ += f"Game starts in {countdown} seconds!"
            else:
                str_ += f"Game has started {countdown * -1} seconds ago!"

        return str_, self.players

    def add_player(self, client_id):
        if len(self.players) < self.max_players:
            self.players[client_id] = {"ready": False}
            return True
        return False

    def remove_player(self, client_id):
        if client_id in self.players:
            del self.players[client_id]
            if client_id == self.host_id and self.players:
                self.host_id = next(iter(self.players))
            return True
        return False

    def player_ready(self, client_id, value):
        if client_id in self.players:
            self.players[client_id]["ready"] = value
            return self.all_players_ready()
        return False

    def all_players_ready(self):
        return all(player["ready"] for player in self.players.values())

    def start_game(self):
        self.state = "starting"
        self.start_time = time.time() + 5  # 5 seconds countdown


class GameHandler:
    def __init__(self):
        self.games = {}

    def add_game(self, message, notified_socket):
        host_id = message["host_id"]
        level_id = message["data"]["globals"]["level"]
        max_players = message["data"]["globals"]["players"]
        players = {i: {"ready": False} for i in range(max_players)}

        new_game = Game(host_id, level_id, max_players, players, "waiting for players", None, data=message["data"])
        self.games[new_game.id] = new_game
        return new_game.id

    def get_games(self):
        return [game.to_dict() for game in self.games.values()]

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id)

    def remove_game(self, message, notified_socket):
        game_id = message["index"]
        game = self.games.get(game_id)

        if game and game.host_id == message["host_id"]:
            del self.games[game_id]
            return True
        return False

    def client_is_already_in_game(self, client_id: int) -> bool:
        for game in self.games.values():
            if client_id in game.players and game.players[client_id]["ready"]:
                return True
        return False

    def join_game(self, game_id: str, client_id: int, value: bool):
        game = self.get_game(game_id)
        if not game:
            return False

        if value:
            if not self.client_is_already_in_game(client_id):
                game.add_player(client_id)
                game.player_ready(client_id, value)
        else:
            game.player_ready(client_id, value)

        if game.all_players_ready():
            game.start_game()

        return True


game_handler = GameHandler()


def main():
    game = Game(0, 1, 2)
    game.add_player(0)
    game.add_player(1)
    print(game)


if __name__ == "__main__":
    main()
