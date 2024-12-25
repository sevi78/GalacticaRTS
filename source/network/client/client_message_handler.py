import time

from source.configuration.game_config import config
from source.factories.building_factory import building_factory
from source.gui.event_text import event_text
from source.handlers.diplomacy_handler import diplomacy_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.handlers.screen_handler import screen_handler
from source.handlers.time_handler import time_handler
from source.player.player_handler import player_handler
from source.trading.market import market
from source.trading.trade import Trade


class ClientMessageHandler:
    def __init__(self, client):
        self.client = client

    def handle_messages(self) -> None:
        data = self.client.receive_message()
        if not data:
            return

        function = data["f"]
        self.client.print_feedback()

        match function:
            case "t":  # set_world_time
                time_handler.set_world_time(data["t"] * 10000)

            case "client_count":
                self.client.set_id(data["id"])

            case "start_game":
                config.app.handle_pause_game()
                config.app.client_edit.set_visible()
                config.app.client_edit.disable_container_widget_buttons()

            case "set_games":
                config.app.client_edit.set_games(data["games"])

            case "set_game_data":
                config.app.level_handler.load_level(filename="", folder="", data=data["data"])
                config.app.level_handler.on_players_changed(data["data"]["globals"]["players"])

            case "pause_game":
                config.app.handle_pause_game()

            case "select_level":
                # if self.client.is_host:
                config.app.level_select.handle_select_level(data["level"])

            case "set_game_speed":
                time_handler.handle_set_game_speed(data)

            case "set_screen_tiled":
                screen_handler.handle_set_screen_tiled(
                        data["width"], data["height"], data["tiles"], data["tile_index"], data["alignment"])

            case "set_players_data":
                player_handler.set_players_data(data["data"])

            case "u":  # update scene
                """
                f = function : u = update
                p = planets
                s = ships
                """
                if self.client.is_host:
                    return


                # start_time = time.time()
                for planet in sprite_groups.planets.sprites():
                    if str(planet.id) not in data["p"].keys():
                        print(f"client_message_handler({self.client.id}).handle_messages({function}): planet {planet.id} not found")
                        continue
                    planet.world_x = data["p"][str(planet.id)]["x"]
                    planet.world_y = data["p"][str(planet.id)]["y"]
                    planet.economy_agent.population = data["p"][str(planet.id)]["p"]

                # end_time = time.time()
                # print (f"update planets took: {end_time - start_time}s")

                for ship in sprite_groups.ships.sprites():
                    if str(ship.id) not in data["s"].keys():
                        print (f"client_message_handler({self.client.id}).handle_messages({function}): ship {ship.id} not found")
                        continue
                    ship.world_x = data["s"][str(ship.id)]["x"]
                    ship.world_y = data["s"][str(ship.id)]["y"]
                    ship.experience = data["s"][str(ship.id)]["e"]

            case "set_target":
                objects = [_ for _ in getattr(sprite_groups, data["object_sprite_group"]) if _.id == data["object_id"]]
                if objects:
                    object = objects[0]
                else:
                    print("set_target.object not found")
                    return
                targets = [_ for _ in getattr(sprite_groups, data["target_sprite_group"]) if _.id == data["target_id"]]
                if targets:
                    target = targets[0]
                else:
                    print("set_target.target not found")
                    return
                if target and target.type == "target object":
                    target.world_x = data["target_world_x"]
                    target.world_y = data["target_world_y"]
                getattr(object, function)(target=target, from_server=True)

            case "get_explored":
                planet = [_ for _ in getattr(sprite_groups, data["sprite_group"]) if _.id == data["planet_id"]][0]
                planet.handle_get_explored(data["owner"])

            case "build":
                building_factory.handle_build(data)

            case "build_immediately":
                building_factory.handle_build_immediately(data["cue_id"])

            case "destroy_building":
                building_factory.handle_destroy_building(data)

            case "send_text":
                event_text.set_text(data["text"])

            case "add_deal":
                trade = Trade(owner_index=int(data["trade"]["owner_index"]), offer=data["trade"]["offer"], request=
                data["trade"]["request"])
                market.add_deal(trade, from_server=True)

            case "accept_deal":
                market.accept_deal(data["deal_index"], data["buyer_index"], from_server=True)

            case "decline_deal":
                market.decline_deal(data["deal_index"], from_server=True)

            case "trade_technology_to_the_bank":
                offer_value = data["offer_value"]
                request_resource = data["request_resource"]
                request_value = data["request_value"]
                player_index = data["player_index"]
                player = config.app.players[player_index]
                player.trade_assistant.trade_technology_to_the_bank(offer_value, request_resource, request_value, player_index, from_server=True)

            case "update_diplomacy_status":
                diplomacy_handler.handle_update_diplomacy_status(
                        data["player_index"], data["enemy_index"], data["status"])

            case _:
                print(f"Unrecognized function: {function}")

    def handle_messages__websocket(self, data) -> None:
        if not data:
            return

        function = data["f"]
        self.client.print_feedback()

        match function:
            case "t":  # set_world_time
                time_handler.set_world_time(data["t"] * 10000)

            case "client_count":
                self.client.set_id(data["id"])

            case "start_game":
                config.app.handle_pause_game()
                config.app.client_edit.set_visible()
                config.app.client_edit.disable_container_widget_buttons()

            case "set_games":
                config.app.client_edit.set_games(data["games"])

            case "set_game_data":
                config.app.level_handler.load_level(filename="", folder="", data=data["data"])
                config.app.level_handler.on_players_changed(data["data"]["globals"]["players"])

            case "pause_game":
                config.app.handle_pause_game()

            case "select_level":
                if self.client.is_host:
                    config.app.level_select.handle_select_level(data["level"])

            case "set_game_speed":
                time_handler.handle_set_game_speed(data)

            case "set_screen_tiled":
                screen_handler.handle_set_screen_tiled(
                        data["width"], data["height"], data["tiles"], data["tile_index"], data["alignment"])

            case "set_players_data":
                player_handler.set_players_data(data["data"])

            case "u":  # update scene
                """
                f = function : u = update
                p = planets
                s = ships
                """
                if self.client.is_host:
                    return

                for planet in sprite_groups.planets.sprites():
                    planet.world_x = data["p"][str(planet.id)]["x"]
                    planet.world_y = data["p"][str(planet.id)]["y"]
                    planet.economy_agent.population = data["p"][str(planet.id)]["p"]

                for ship in sprite_groups.ships.sprites():
                    ship.world_x = data["s"][str(ship.id)]["x"]
                    ship.world_y = data["s"][str(ship.id)]["y"]
                    ship.experience = data["s"][str(ship.id)]["e"]

            case "set_target":
                objects = [_ for _ in getattr(sprite_groups, data["object_sprite_group"]) if _.id == data["object_id"]]
                if objects:
                    object = objects[0]
                else:
                    print("set_target.object not found")
                    return
                targets = [_ for _ in getattr(sprite_groups, data["target_sprite_group"]) if _.id == data["target_id"]]
                if targets:
                    target = targets[0]
                else:
                    print("set_target.target not found")
                    return
                if target and target.type == "target object":
                    target.world_x = data["target_world_x"]
                    target.world_y = data["target_world_y"]
                getattr(object, function)(target=target, from_server=True)

            case "get_explored":
                planet = [_ for _ in getattr(sprite_groups, data["sprite_group"]) if _.id == data["planet_id"]][0]
                planet.handle_get_explored(data["owner"])

            case "build":
                building_factory.handle_build(data)

            case "build_immediately":
                building_factory.handle_build_immediately(data["cue_id"])

            case "destroy_building":
                building_factory.handle_destroy_building(data)

            case "send_text":
                event_text.set_text(data["text"])

            case "add_deal":
                trade = Trade(owner_index=int(data["trade"]["owner_index"]), offer=data["trade"]["offer"], request=
                data["trade"]["request"])
                market.add_deal(trade, from_server=True)

            case "accept_deal":
                market.accept_deal(data["deal_index"], data["buyer_index"], from_server=True)

            case "decline_deal":
                market.decline_deal(data["deal_index"], from_server=True)

            case "trade_technology_to_the_bank":
                offer_value = data["offer_value"]
                request_resource = data["request_resource"]
                request_value = data["request_value"]
                player_index = data["player_index"]
                player = config.app.players[player_index]
                player.trade_assistant.trade_technology_to_the_bank(offer_value, request_resource, request_value, player_index, from_server=True)

            case "update_diplomacy_status":
                diplomacy_handler.handle_update_diplomacy_status(
                        data["player_index"], data["enemy_index"], data["status"])

            case _:
                print(f"Unrecognized function: {function}")
    def update_clients(self):
        """
        this creates the message to send to the server:
        f = function
        u = update
        p = planets
        s = ships

        {"f":"u","p": {}, "s": {}}
        """
        if not self.client.is_host:
            return
        # data_ = {"planets": {}, "ships": {}}
        message = {"f": "u", "p": {}, "s": {}}
        for planet in sprite_groups.planets.sprites():
            message["p"][planet.id] = planet.get_network_data("position_update")
        for ship in sprite_groups.ships.sprites():
            message["s"][ship.id] = ship.get_network_data("position_update")
        self.client.send_message(message)
