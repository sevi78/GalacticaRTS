import json
import socket
import struct
import time

import brotli
import select

from source.network.server.market_data_remote import MarketDataRemote
from source.network.server.server_message_handler import ServerMessageHandler

TIME_UPDATE_DURATION = 1
DEBUG = False

"""
192.168.1.22 the mac
"""
class Server:  # original
    def __init__(self, host: str, port: int, status_callback=None) -> None:
        # server connection stuff
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.sockets_list = [self.server_socket]
        self.clients = {}

        # message handler
        self.message_handler = ServerMessageHandler(self)

        # game stuff
        self.games = {}
        self.status_callback = status_callback
        self.running = True
        self.game_start_time = None  # used to start the countdown to start the game
        self.market_data = MarketDataRemote()

        # timing stuff
        self.game_speed = 1
        self.start_time = time.time()  # star time in seconds to calculate world time

        # time update
        self.last_time_update_time = time.time()
        self.time_update_duration = 1 / TIME_UPDATE_DURATION

    def register_client(self) -> None:  # original
        client_socket, client_address = self.server_socket.accept()
        self.send_message(client_socket, {"f": "client_count", "id": len(self.clients)})
        self.sockets_list.append(client_socket)
        self.clients[client_socket] = client_address
        self.update_status(f"GameServer.Accepted new connection from {client_address}")
        # print(f"Server.Accepted new connection from {client_address}")

    def time_update_time_reached(self) -> bool:
        if time.time() - self.last_time_update_time >= self.time_update_duration:
            self.last_time_update_time = time.time()
            return True
        return False

    def get_world_time(self) -> float:
        elapsed = time.time() - self.start_time
        # return int(elapsed * self.game_speed * 10000)

        return int(elapsed * self.game_speed)

    def broadcast(self, message) -> None:
        # print(f"Server.broadcast: {message}")
        for client_socket in self.clients:
            self.send_message(client_socket, message)

    def send_message(self, client_socket, message) -> None:
        try:
            json_data = json.dumps(message).encode('utf-8')
            compressed_data = brotli.compress(json_data)
            message_length = len(compressed_data)
            client_socket.send(struct.pack('!I', message_length))
            client_socket.sendall(compressed_data)
            self.update_status(message)
        except Exception as e:
            self.update_status(f"GameServer.Failed to send message: {e}: {type(message)}")

    def receive_message(self, client_socket) -> dict or None:
        try:
            length_bytes = client_socket.recv(4)
            if not length_bytes:
                return None
            message_length = struct.unpack('!I', length_bytes)[0]
            compressed_data = b''
            while len(compressed_data) < message_length:
                chunk = client_socket.recv(min(message_length - len(compressed_data), 1024))
                if not chunk:
                    return None
                compressed_data += chunk
            decompressed_data = brotli.decompress(compressed_data)
            return json.loads(decompressed_data.decode('utf-8'))
        except Exception as e:
            self.update_status(f"GameServer.Error receiving message: {e}")
            return None

    def start(self) -> None:
        self.update_status(f"Server listening on {self.host}:{self.port}")
        while self.running:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.0)

            if self.time_update_time_reached():
                self.broadcast({"f": "t", "t": self.get_world_time()})
                self.message_handler.handle_game_start()

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    self.register_client()
                else:
                    message = self.receive_message(notified_socket)
                    if message:
                        self.update_status(f"GameServer.Received from {self.clients[notified_socket]}:\n{message}")
                        self.message_handler.handle_message(message, notified_socket)
                    else:
                        self.update_status(f"GameServer.Closed connection from {self.clients[notified_socket]}")
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]

    def stop(self) -> None:
        self.running = False
        self.update_status("Server stopped.")

    def update_status(self, message) -> None:
        if self.status_callback:
            self.status_callback(message)
            if DEBUG:
                print(message)
        else:
            if DEBUG:
                print(message)


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
