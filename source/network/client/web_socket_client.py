from source.network.client.client_message_handler import ClientMessageHandler

network_config = {
    "host": "192.168.1.41",
    "port": 5555
    }

#
# class WebSocketClient:
#     def __init__(self):
#         self.thread = None
#         self.id = 0
#         self.ip = network_config["host"]
#         self.is_host = False
#         self.game_state = None
#         self.connected = False
#         self.message_handler = ClientMessageHandler(self)
#
#     def run_in_thread(self, host, port):
#         self.loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(self.loop)
#         self.loop.run_until_complete(self.connect_to_server(host, port))
#
#     def start_connection(self, host, port):
#         self.thread = threading.Thread(target=self.run_in_thread, args=(host, port))
#         self.thread.start()
#
#     def stop_connection(self):
#         if hasattr(self, 'loop') and self.loop.is_running():
#             self.loop.call_soon_threadsafe(self.loop.stop)
#         if hasattr(self, 'thread'):
#             self.thread.join()
#
#     async def connect_to_server(self, host: str, port: int):
#         async with websockets.connect(f"ws://{host}:{port}") as websocket:
#
#             try:
#                 print("Connected to server")
#
#                 # Receive client ID from server
#                 initial_message = await websocket.recv()
#                 initial_data = json.loads(initial_message)
#                 self.id = initial_data["client_id"]
#                 self.is_host = self.id == 0
#                 print(f"Received client ID: {self.id}")
#                 self.connected = True
#                 while True:
#                     # Simulate client making changes to its game state
#                     await self.make_changes(websocket)
#
#                     # Receive updated game state from server
#                     message = await websocket.recv()
#                     self.game_state = json.loads(message)
#                     self.display_game_state()
#
#                     # Wait a bit before next update
#                     await asyncio.sleep(random.uniform(1, 3))
#
#             except websockets.exceptions.ConnectionClosedError as e:
#                 print(f"WebSocketClient {self.id} connection closed: {e}")
#
#     async def make_changes(self, websocket):
#         # Simulate client making changes to its game state
#         new_score = random.randint(1, 10)
#         changes = {"score": new_score}
#         await websocket.send(json.dumps(changes))
#         print(f"WebSocketClient {self.id} sent changes: {changes}")
#
#     def display_game_state(self):
#         print(f"\nClient {self.id} received game state:")
#         print(f"My state: {self.game_state['client_states'].get(str(self.id), 'Not found')}")
#         print(f"All client states: {self.game_state['client_states']}")
#         print("---")
#
#     def send_message(self, message):
#         pass
#
# async def connect_clients(num_clients):
#     tasks = [WebSocketClient().connect_to_server(network_config["host"], network_config["port"]) for _ in range(num_clients)]
#     await asyncio.gather(*tasks)
#
# async def connect_client():
#     task = WebSocketClient().connect_to_server(network_config["host"], network_config["port"])
#     await task
#
# if __name__ == "__main__":
#     num_clients = 3
#     asyncio.run(connect_clients(num_clients))


import asyncio
import json
import websockets
import threading


class WebSocketClient:
    def __init__(self):
        self.id = 0
        self.ip = network_config["host"]
        self.host = None
        self.port = None
        self.is_host = False
        self.game_state = None
        self.connected = False
        self.message_handler = ClientMessageHandler(self)
        self.websocket = None
        self.loop = None
        self.thread = None

    # async def connect_to_server(self, host: str, port: int):
    #     self.websocket = await websockets.connect(f"ws://{host}:{port}")
    #     print("Connected to server")
    #     initial_message = await self.websocket.recv()
    #     initial_data = json.loads(initial_message)
    #     self.id = initial_data["client_id"]
    #     self.is_host = self.id == 0
    #     print(f"Received client ID: {self.id}")
    #     self.connected = True
    #     self.host = host
    #     self.port = port

    async def connect_to_server(self, host: str, port: int):
        async with websockets.connect(f"ws://{host}:{port}") as websocket:
            try:
                print("Connected to server")
                initial_message = await websocket.recv()
                initial_data = json.loads(initial_message)
                self.id = initial_data["client_id"]
                self.is_host = self.id == 0
                print(f"Received client ID: {self.id}")
                self.connected = True

                heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=30)
                        self.game_state = json.loads(message)
                        self.display_game_state()
                    except asyncio.TimeoutError:
                        # No message received, but continue the loop
                        continue

            except websockets.exceptions.ConnectionClosed as e:
                print(f"WebSocketClient {self.id} connection closed: {e}")
            finally:
                heartbeat_task.cancel()

    async def send_heartbeat(self, websocket):
        while True:
            await asyncio.sleep(20)  # Send heartbeat every 20 seconds
            await websocket.send(json.dumps({"type": "heartbeat"}))

    async def receive_messages(self):
        while True:
            try:
                message = await self.websocket.recv()
                self.game_state = json.loads(message)
                self.message_handler.handle_messages(json.loads(message))
                self.display_game_state()
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"WebSocketClient {self.id} connection closed: {e}")
                break

    def run_client(self, host, port):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_to_server(host, port))
        self.loop.create_task(self.receive_messages())
        self.loop.run_forever()

    def start_client(self, host, port):
        self.thread = threading.Thread(target=self.run_client, args=(host, port))
        self.thread.start()

    def stop_client(self):
        print ("Stopping client...")
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread:
            self.thread.join()

    async def send_message_async(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))

    def send_message(self, message):
        if self.loop and self.websocket:
            asyncio.run_coroutine_threadsafe(self.send_message_async(message), self.loop)

    def display_game_state(self):
        pass
        # print(f"\nClient {self.id} received game state:")
        # print(f"My state: {self.game_state['client_states'].get(str(self.id), 'Not found')}")
        # print(f"All client states: {self.game_state['client_states']}")
        # print("---")


"""
new ping-pong version : 


import asyncio
import json
import websockets

class WebSocketClient:
    # ... (other methods remain the same)

    async def connect_to_server(self, host: str, port: int):
        async with websockets.connect(f"ws://{host}:{port}") as websocket:
            try:
                print("Connected to server")
                initial_message = await websocket.recv()
                initial_data = json.loads(initial_message)
                self.id = initial_data["client_id"]
                self.is_host = self.id == 0
                print(f"Received client ID: {self.id}")
                self.connected = True

                heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=30)
                        self.game_state = json.loads(message)
                        self.display_game_state()
                    except asyncio.TimeoutError:
                        # No message received, but continue the loop
                        continue

            except websockets.exceptions.ConnectionClosed as e:
                print(f"WebSocketClient {self.id} connection closed: {e}")
            finally:
                heartbeat_task.cancel()

    async def send_heartbeat(self, websocket):
        while True:
            await asyncio.sleep(20)  # Send heartbeat every 20 seconds
            await websocket.send(json.dumps({"type": "heartbeat"}))

    # ... (other methods remain the same)

"""