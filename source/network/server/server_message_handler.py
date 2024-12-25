import time

from source.network.server.game_handler import game_handler


class ServerMessageHandler:
    def __init__(self, server):
        self.server = server

    def handle_game_start(self):
        # iterate over all games and check if they should start now
        for key, value in game_handler.games.items():

            # if all players are ready, game_start_time is set, so start the game
            if value.start_time:
                countdown = value.start_time - time.time()

                # send the game data for level loading
                if countdown < 5:
                    # print ("Server.handle_game_start: value.state: ", value.state)
                    if value.state == "starting":
                        self.server.broadcast({"f": "set_game_data", "data": value.data})
                        value.state = "loaded_data"

                # finally start the game
                if countdown < 0:
                    if not value.state == "playing":
                        value.state = "playing"
                        self.server.broadcast({"f": "start_game", "game_id": key})

    def handle_message(self, message, notified_socket):
        match message["f"]:
            case "add_game" | "remove_game":
                function = game_handler.add_game if message["f"] == "add_game" else game_handler.remove_game
                function(message, notified_socket)
                games = game_handler.get_games()
                self.server.broadcast({"f": "set_games", "games": games})
                self.server.update_status(message)

            case "join_game":
                game_handler.join_game(message["game_id"], message["client_id"], message["value"])
                games = game_handler.get_games()
                self.server.broadcast({"f": "set_games", "games": games})
                self.server.update_status(message)

            case "add_deal" | "accept_deal" | "decline_deal":
                self.server.market_data.handle_message(message)
                self.server.broadcast(message)
                self.server.update_status(message)

            case "start_game":
                if not self.server.game_start_time:
                    self.server.game_start_time = time.time() + 3
                    message["game_start_time"] = self.server.game_start_time
                    self.server.broadcast(message)
                    self.server.update_status(message)

            case "set_game_speed":
                self.server.game_speed = message["game_speed"]
                self.server.broadcast(message)
                self.server.update_status(message)

            case "handle_update_scene":
                """
                "world_time": self.get_world_time()"""
                self.server.broadcast(message)
                self.server.update_status(message)

            case _:  # all other cases
                self.server.broadcast(message)
                self.server.update_status(message)
