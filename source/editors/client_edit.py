import json

from source.configuration.game_config import config
from source.editors.editor_base.editor_base import EditorBase
from source.editors.editor_base.editor_config import TOP_SPACING
from source.gui.container.container_config import WIDGET_SIZE
from source.gui.container.container_widget import ContainerWidget
from source.gui.container.container_widget_item import ContainerWidgetItem
from source.gui.container.container_widget_item_button import ContainerWidgetItemButton
from source.gui.container.filter_widget import FilterWidget
from source.gui.event_text import event_text
from source.gui.widgets.buttons.image_button import ImageButton
from source.gui.widgets.inputbox import InputBox
from source.handlers.file_handler import load_file, write_file
from source.multimedia_library.images import get_image, overblit_button_image, scale_image_cached
from source.network.server.game_handler import Game
from source.text.text_formatter import validate_text_format

INPUTBOX_WIDTH = 200
INPUTBOX_HEIGHT = 18
network_config = {
    "host": "192.168.1.41",
    "port": 5555
    }


class ClientEdit(EditorBase):
    def __init__(self, win, x, y, width, height, is_sub_widget=True, **kwargs) -> None:
        EditorBase.__init__(self, win, x, y, width, height, is_sub_widget=False, **kwargs)
        self.client = config.app.game_client

        #  widgets
        self.connect_button = None
        self.container = None
        self.server_inputbox = None
        self.port_inputbox = None
        self.widgets = []

        self.players = 2
        self.level = 0
        self.joined = False
        self.game_id = None
        self.games = None

        # data
        conf = load_file("network_config.json", "config")
        self.host = conf["host"]
        self.port = conf["port"]
        self.format_dict = {'server': 'xxx.xxx.x.xx', 'port': '0000'}

        # create widgets
        self.create_close_button()
        self.create_inputboxes()
        self.create_connect_button()
        self.create_container()

        self.create_add_game_button(lambda: self.add_game(), "add game")
        self.create_save_button(lambda: self.save_client(), "save client", y=self.world_y + TOP_SPACING * 2)

        # attach to parent
        self.parent.editors.append(self)

        # hide initially
        self.connect_to_server()
        self.hide()

    def create_inputboxes(self) -> None:
        y = self.world_y + TOP_SPACING * 2
        self.server_inputbox = InputBox(
                self.win,
                self.world_x + 130,
                y,
                150,
                INPUTBOX_HEIGHT,
                self.host,
                delete_text_on_first_input=True,
                parent=self,
                text_input_type=None,
                key="server",
                max_letters=12)

        self.widgets.append(self.server_inputbox)
        y += INPUTBOX_HEIGHT

        self.port_inputbox = InputBox(
                self.win,
                self.world_x + 130,
                y,
                60,
                INPUTBOX_HEIGHT,
                str(self.port),
                delete_text_on_first_input=True,
                parent=self,
                text_input_type=int,
                key="port",
                max_letters=4)

        self.widgets.append(self.port_inputbox)

        y += INPUTBOX_HEIGHT
        self.max_height = y

    def create_container(self) -> None:
        container_width = self.world_width - INPUTBOX_HEIGHT * 2
        container_height = 260

        self.container = ContainerWidget(
                config.app.win,
                self.world_x + INPUTBOX_HEIGHT,
                self.world_y + INPUTBOX_HEIGHT * 10,
                container_width,
                container_height,
                [],
                function=None,
                layer=9,
                list_name="games",
                name="games_container",
                drag_enabled=False,
                save=False,

                filter_widget=FilterWidget(
                        config.app.win,
                        self.world_x,
                        self.world_y,
                        container_width,
                        container_height,
                        ["players", "level", "state"],
                        parent=config.app,
                        layer=10,
                        list_name="games",
                        name="games_container_filter",
                        ignore_other_editors=True,
                        save=False
                        )
                )
        self.containers.append(self.container)
        self.max_height += container_height + INPUTBOX_HEIGHT * 2

    def create_connect_button(self) -> None:
        button_size = 32
        self.connect_button = ImageButton(
                win=self.win,
                x=self.world_x + 300,
                y=self.world_y + TOP_SPACING * 2,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(get_image("connect_icon.png"), (button_size, button_size)),
                tooltip="Connect to server",
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=self.connect_to_server,
                name="connect_button"
                )
        self.buttons.append(self.connect_button)
        self.widgets.append(self.connect_button)

    def create_add_game_button(self, function: callable, tooltip: str, **kwargs) -> ImageButton:
        name = kwargs.get("name", "no_name")
        button_size = 32
        self.add_game_button = ImageButton(win=self.win,
                x=self.get_screen_x() + self.get_screen_width() / 2 - button_size / 2,
                y=self.max_height + button_size / 2,
                width=button_size,
                height=button_size,
                is_sub_widget=False,
                parent=self,
                image=scale_image_cached(
                        get_image("plus_icon.png"), (button_size, button_size)),
                tooltip=tooltip,
                frame_color=self.frame_color,
                moveable=False,
                include_text=True,
                layer=self.layer,
                on_click=function,
                name=name
                )
        self.add_game_button.hide()

        self.buttons.append(self.add_game_button)
        self.widgets.append(self.add_game_button)
        return self.add_game_button

    def connect_to_server(self) -> None:
        if self.client.connected:
            self.client.disconnect_from_server()
            self.connect_button.tooltip = "Connect to server"
            event_text.set_text("Disconnected from server")
            print("Disconnected from server")

        else:
            # await asyncio.to_thread(self.client.connect_to_server)
            self.client.connect_to_server()
            # asyncio.run(self.client.connect_to_server(network_config["host"], network_config["port"]))
            # self.client.start_connection(network_config["host"], network_config["port"])
            # self.client.start_client(network_config["host"], network_config["port"])
            if self.client.connected:
                config.app.handle_pause_game()
                self.connect_button.tooltip = "Disconnect from server"
                event_text.set_text("connected to server")
                print(f"ClientEdit.connect_to_server: connecting to server: self.client: {self.client.host}, self.client.port: {self.client.port}")

        overblit_button_image(self.connect_button, "check.png", not self.client.connected)

    def get_input_box_values(self, obj: object, key: str, value: any) -> None:
        """ this is called from inputbox,  """
        setattr(self, key, value)

    def save_client(self) -> None:
        """ saves client connection data to network_config.json """
        text = {"server": self.host, "port": self.port}
        text_string = json.dumps(text)
        text_validation = validate_text_format(text_string, self.format_dict)

        if text_validation == "Valid":
            write_file("network_config.json", "config", text)
            event_text.set_text(text_validation)
        else:
            event_text.set_text(text_validation)

    def add_game(self) -> None:
        self.client.send_message({"f": "add_game", "host_id": self.client.id, "data": config.app.level_handler.data})

    def remove_game(self, game_id: str) -> None:
        self.client.send_message({"f": "remove_game", "host_id": self.client.id, "index": game_id})

    def join_game(self, game_id: str) -> None:
        if not self.joined:
            self.joined = True
            self.game_id = game_id
        else:
            self.joined = False
            self.game_id = None

        self.client.send_message({
            "f": "join_game",
            "client_id": self.client.id,
            "game_id": game_id,
            "value": self.joined
            })

    def set_games(self, games: list[dict]) -> None:
        self.games = games
        self.container.set_widgets(self.convert_games_into_container_widget_item(games))
        for i in self.container.widgets:
            # update countdown and text
            i.set_text_and_state_image()

    def start_game(self, game_id: str):
        # print(f"starting game: {game_id}")
        self.client.send_message({"f": "start_game", "game_id": game_id})

    def convert_games_into_container_widget_item(
            self, games: list[dict], sort_by: str = None, reverse: bool = True, **kwargs
            ) -> list[ContainerWidgetItem]:
        """
        Convert a list of games into ContainerWidgetItem objects for display in the UI.

        This method creates a ContainerWidgetItem for each game, including buttons for joining
        and (if the current user is the host) removing the game.

        Args:
            games (list): A list of dictionaries containing game information.
            sort_by (str, optional): Key to sort the games by. Not implemented yet.
            reverse (bool, optional): Whether to reverse the sort order. Defaults to True.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            list: A list of ContainerWidgetItem objects representing the games.
        """
        widgets = []
        button_size = 30  # Size of the join/remove buttons

        # TODO: Implement sorting functionality
        if sort_by is not None:
            pass

        for index_, game in enumerate(games):
            # Create a Game object from the dictionary data
            game_ = Game(
                    host_id=game["host_id"],
                    level_id=game["level_id"],
                    max_players=game["max_players"],
                    players=game["players"],
                    state=game["state"],
                    start_time=game["start_time"],
                    data=game["data"],
                    id=game["id"])

            # Create closures for join and remove functions to capture current game context
            def create_join_function(game_id):
                return lambda: self.join_game(game_id)

            def create_remove_function(game_id):
                return lambda: self.remove_game(game_id)

            def create_start_function(game_id):
                return lambda: self.start_game(game_id)

            # Create the ContainerWidgetItem for the game
            container_item = ContainerWidgetItem(
                    config.app.win,
                    0,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    WIDGET_SIZE,
                    image=get_image(config.app.players[game["host_id"]].image_name),
                    obj=game_,
                    index=index_ + 1,
                    item_buttons=[
                        # Add join button for all games
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "join_game",
                                "thumps_up.png",
                                container_name="game_container",
                                container=self.container,
                                function=create_join_function(game_.id),
                                tooltip="join game")
                        ],
                    parent=None,
                    container=self.container,
                    container_name="game_container")

            # Add the remove button only if the current user is the host of the game
            if self.client.id == game["host_id"]:
                container_item.item_buttons.append(
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "remove_game",
                                "minus_icon.png",
                                container_name="game_container",
                                container=self.container,
                                function=create_remove_function(game_.id),
                                tooltip="remove game")
                        )

                container_item.item_buttons.append(
                        ContainerWidgetItemButton(
                                config.app.win,
                                0,
                                0,
                                button_size,
                                button_size,
                                "start_game",
                                "play_icon.png",
                                container_name="game_container",
                                container=self.container,
                                function=create_start_function(game_.id),
                                tooltip="start game")
                        )

            widgets.append(container_item)

        return widgets

    def set_container_widget_text(self) -> None:
        # print ("self.joined:", self.joined)

        for i in self.container.widgets:
            i.set_text_and_state_image()

    def disable_container_widget_buttons(self) -> None:
        for i in self.container.widgets:
            for j in i.item_buttons:
                j.disable()

    def listen(self, events) -> None:
        if not self._hidden and not self._disabled:
            self.handle_hovering()
            self.drag(events)
            self.server_inputbox.handle_events(events)
            self.port_inputbox.handle_events(events)
            self.set_container_widget_text()

    def draw(self) -> None:
        if not self._hidden and not self._disabled:
            self.container.reposition(self.world_x, self.world_y)
            self.draw_frame()
            self.draw_text(self.world_x + self.text_spacing, self.world_y + TOP_SPACING + self.text_spacing, 200, INPUTBOX_HEIGHT, "connect to server:")
            self.draw_text(self.world_x + self.text_spacing, self.server_inputbox.world_y, 200, INPUTBOX_HEIGHT, "server:")
            self.draw_text(self.world_x + self.text_spacing, self.port_inputbox.world_y, 200, INPUTBOX_HEIGHT, "port:")
            self.server_inputbox.draw()
            self.port_inputbox.draw()
