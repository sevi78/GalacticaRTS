import enum
import errno
import json
import socket
import struct

import brotli

from source.configuration.game_config import config
from source.handlers.screen_handler import screen_handler
from source.network.client.client_message_handler import ClientMessageHandler

DEBUG = True


class FeedbackType(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    EXCEPTION = "exception"
    CONNECTION = "connection"
    MESSAGE = "message"


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.ip = socket.gethostbyname(socket.gethostname())
        self.host = host
        self.port = port
        self.socket = None
        self.is_host = False
        self.connected = False
        self.feedback = {}
        self.feedback_filters = set()
        self.add_feedback_filter(FeedbackType.INFO)
        self.add_feedback_filter(FeedbackType.WARNING)
        self.add_feedback_filter(FeedbackType.ERROR)
        self.add_feedback_filter(FeedbackType.EXCEPTION)
        self.add_feedback_filter(FeedbackType.CONNECTION)
        self.set_feedback(f"Client.__init__: Initializing GameClient with host: {self.host}, port: {self.port}", FeedbackType.INFO)

        if self.check_internet_connection():
            self.set_feedback(f"Client.__init__: Connected to internet: self.ip: {self.ip}", FeedbackType.CONNECTION)
        else:
            self.set_feedback("Client.__init__: No internet connection.", FeedbackType.WARNING)

        self.id = 0
        self.game_start_time = None
        self.message_handler = ClientMessageHandler(self)

        # self.send_message({"f": "set_game_speed", "game_speed": config.game_speed})

    def check_internet_connection(self) -> bool:
        self.set_feedback("Client.check_internet_connection: Checking internet connection... using host (google.com) : '8.8.8.8' and port : 53", FeedbackType.CONNECTION)
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3.0)
            self.set_feedback("Client.check_internet_connection: Internet connection detected.", FeedbackType.CONNECTION)
            return True
        except OSError:
            self.set_feedback("Client.check_internet_connection: No internet connection.", FeedbackType.ERROR)
            return False

    def connect_to_server(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.setblocking(False)
            self.connected = True
            self.set_feedback(f"Client.connect_to_server: Connected to server: self.socket: {self.socket}, dir: {self.socket.__dir__()}", FeedbackType.CONNECTION)
        except Exception as e:
            self.set_feedback(f"Client.connect_to_server: Failed to connect to server: {e}", FeedbackType.EXCEPTION)
            self.connected = False
            self.is_host = True
            if self.socket:
                self.socket.close()
                self.socket = None

    def disconnect_from_server(self) -> None:
        if self.connected:
            try:
                if self.socket:
                    self.socket.close()
                    self.socket = None
                self.connected = False
                self.is_host = True  # Reset to host mode
                self.set_feedback("Disconnected from server successfully", FeedbackType.CONNECTION)
            except Exception as e:
                self.set_feedback(f"Error while disconnecting from server: {e}", FeedbackType.EXCEPTION)
        else:
            self.set_feedback("Client.disconnect_from_server: Not connected to any server", FeedbackType.WARNING)

        # Reset client state
        self.reset_client_state()

    def reset_client_state(self) -> None:
        self.id = 0
        self.game_start_time = None
        self.set_feedback(f"Client.reset_client_state: Reseting client state: self.id: {self.id}", FeedbackType.INFO)

    def set_id(self, id: int) -> None:
        self.id = id
        config.player = self.id
        config.app.player = config.app.players[self.id]

        if self.id == 0:
            self.is_host = True
        else:
            self.is_host = False

        if self.connected:
            screen_handler.set_screen_tiled(1920, 1080, 2, self.id, 1)

        self.set_feedback(f"Client.set_id: Client ID set to {self.id}", FeedbackType.INFO)

    def set_feedback(self, message: str, feedback_type: FeedbackType = FeedbackType.INFO) -> None:
        self.feedback = {
            "type": feedback_type.value,
            "message": message
            }
        self.print_feedback()

    def print_feedback(self) -> None:
        if DEBUG:
            if not self.feedback_filters or self.feedback["type"] in self.feedback_filters:
                print(f"[{self.feedback['type'].upper()}] {self.feedback['message']}")

    def add_feedback_filter(self, feedback_type: FeedbackType) -> None:
        self.feedback_filters.add(feedback_type.value)

    def remove_feedback_filter(self, feedback_type: FeedbackType) -> None:
        self.feedback_filters.discard(feedback_type.value)

    def clear_feedback_filters(self) -> None:
        self.feedback_filters.clear()

    def send_message(self, message) -> None:
        if not self.connected or not self.socket:
            # self.set_feedback(f"Client.send_message: Client not connected: self.connected: {self.connected}, self.socket:{self.socket} ", FeedbackType.WARNING)
            return
        try:
            json_data = json.dumps(message).encode('utf-8')
            compressed_data = brotli.compress(json_data)
            message_length = len(compressed_data)
            self.socket.send(struct.pack('!I', message_length))
            self.socket.sendall(compressed_data)
            self.set_feedback(f"Client({self.id}).Sent message: {message}", FeedbackType.MESSAGE)
        except socket.error as e:
            if e.errno in [errno.ECONNRESET, errno.ENOTCONN, errno.ESHUTDOWN]:
                self.set_feedback(f"Client({self.id})send_message: Serious connection error: {e}. Disconnecting.", FeedbackType.ERROR)
                self.disconnect_from_server()
            else:
                self.set_feedback(f"Client({self.id})send_message: Failed to send message: {e}. Will retry on next attempt.", FeedbackType.WARNING)
        except Exception as e:
            self.set_feedback(f"Client({self.id})send_message: Unexpected error while sending message: {e}", FeedbackType.EXCEPTION)

    def receive_message(self) -> dict | None:
        if not self.connected or not self.socket:
            return None
        try:
            length_bytes = self.socket.recv(4)
            if not length_bytes:
                self.disconnect_from_server()
                return None
            message_length = struct.unpack('!I', length_bytes)[0]
            compressed_data = b''
            while len(compressed_data) < message_length:
                chunk = self.socket.recv(min(message_length - len(compressed_data), 1024))
                if not chunk:
                    self.disconnect_from_server()
                    return None
                compressed_data += chunk
            decompressed_data = brotli.decompress(compressed_data)
            message = json.loads(decompressed_data.decode('utf-8'))
            self.set_feedback(f"Client({self.id}).receive_messageReceived message: {message}", FeedbackType.MESSAGE)
            return message
        except socket.error as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                self.set_feedback(f"Client{self.id}.receive_message: Socket error: {e}", FeedbackType.ERROR)
                self.disconnect_from_server()
        except json.JSONDecodeError as e:
            self.set_feedback(f"Client{self.id}.receive_message: Invalid JSON received: {e}", FeedbackType.ERROR)
        except Exception as e:
            self.set_feedback(f"Client{self.id}.receive_message: An unexpected error occurred: {e}", FeedbackType.EXCEPTION)
            self.disconnect_from_server()
        return None
