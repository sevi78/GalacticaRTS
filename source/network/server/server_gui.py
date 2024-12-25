import threading
import tkinter as tk

from source.network.server.server import Server


class GameServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Galactica RTS: Game Server GUI")
        self.master.geometry("800x600")
        self.server = None
        self.server_thread = None
        self.message_buffer = {
            "t": [],# set world time
            'add_game': [],
            'join_game': [],
            'set_screen_tiled': [],
            'get_explored': [],
            'set_players_data': [],
            'set_target': [],
            'add_deal': [],
            'trade_technology_to_the_bank': [],
            'build': [],
            'set_game_speed': [],
            'pause_game': [],
            'accept_deal': [],
            'decline_deal': [],
            'build_immediately': [],
            'destroy_building': [],
            "others": [],
            "u": [],
            }

        self.message_buffer_states = {
            "t": False,# set world time
            'add_game': False,
            'join_game': False,
            'set_screen_tiled': False,
            'get_explored': False,
            'set_players_data': False,
            'set_target': False,
            'add_deal': False,
            'trade_technology_to_the_bank': False,
            'build': False,
            'set_game_speed': False,
            'pause_game': False,
            'accept_deal': False,
            'decline_deal': False,
            'build_immediately': False,
            'destroy_building': False,
            "others": False,
            "u": False,# udate scene
            }
        self.checkboxes = {}
        self.filter_vars = {}
        self.last_message_count = {key: 0 for key in self.message_buffer}
        self.create_widgets()
        self.start_server()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Host input
        tk.Label(self.master, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.host_entry = tk.Entry(self.master)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Port input
        tk.Label(self.master, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = tk.Entry(self.master)
        self.port_entry.insert(0, "5555")
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Start server button
        self.start_button = tk.Button(self.master, text="Start Server", command=self.start_server)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=0)

        # Filter frame
        self.filter_frame = tk.Frame(self.master)
        self.filter_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        # Create checkboxes in the filter frame
        for i, (key, value) in enumerate(self.message_buffer.items()):
            var = tk.BooleanVar(value=self.message_buffer_states[key])
            self.filter_vars[key] = var
            checkbox = tk.Checkbutton(self.filter_frame, text=key, variable=var)
            checkbox.grid(row=i // 3, column=i % 3, sticky="w", padx=5, pady=2)
            self.checkboxes[key] = checkbox

        # Status display
        self.status_text = tk.Text(self.master, state="disabled", wrap=tk.WORD)
        self.status_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Scrollbar for status_text
        self.scrollbar = tk.Scrollbar(self.master, command=self.status_text.yview)
        self.scrollbar.grid(row=5, column=2, sticky="ns")
        self.status_text.config(yscrollcommand=self.scrollbar.set)

        # Configure grid
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(5, weight=1)

    def start_server(self):
        if not self.server:
            host = self.host_entry.get()
            port = int(self.port_entry.get())
            self.update_status(f"Starting server on {host}:{port}")

            # Create and start the server in a new thread
            self.server = Server(host, port, status_callback=self.update_status)
            self.server_thread = threading.Thread(target=self.server.start)
            self.server_thread.start()

            self.start_button.config(text="stopp server")
        else:
            self.stop_server()
            self.start_button.config(text="start server")

    def stop_server(self):
        if self.server:
            self.update_status("Stopping server...")
            self.server.stop()
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5)
            self.server = None
            self.server_thread = None
            self.update_status("Server stopped.")

    def on_closing(self):
        if self.server:
            self.stop_server()
        self.master.destroy()

    def get_size_str(self, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"

    def update_status(self, message):
        self.status_text.config(state="normal")

        if isinstance(message, dict):
            function = message.get("f", "others")
        else:
            function = "others"

        # calculate size
        size_bytes = len(str(message).encode('utf-8'))
        size_str = self.get_size_str(size_bytes)
        total_size = size_bytes * len(self.message_buffer[function])

        self.message_buffer[function].append((message, size_str))
        self.checkboxes[
            function].config(text=f"{function} ({len(self.message_buffer[function])}, size: {self.get_size_str(total_size)})")

        # Determine if we need to auto-scroll
        should_autoscroll = self.scrollbar.get()[1] == 1.0

        for function_name, messages in self.message_buffer.items():
            if self.filter_vars[function_name].get():
                new_messages = messages[self.last_message_count[function_name]:]
                for new_message, size in new_messages:
                    self.status_text.insert(tk.END, f"{new_message} [Size: {size}]\n")
                self.last_message_count[function_name] = len(messages)

        # Auto-scroll if we were at the bottom before adding new content
        if should_autoscroll:
            self.status_text.see(tk.END)

        self.status_text.config(state="disabled")
        self.master.update_idletasks()


def main():
    root = tk.Tk()
    app = GameServerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
