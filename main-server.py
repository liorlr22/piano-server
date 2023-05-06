import threading
from tkinter import messagebox
import mido
from pickle import dumps, loads
from lib.net import PianoServer
from lib.midi import MidiStreamer
from lib.visuals import ServerApp


# Select port
# Select host
# Add Index splitting logics


class Main:
    def __init__(self) -> None:
        self.app = None
        self.host = "0.0.0.0"
        self.port = 5000
        self.listenCount = 5
        self.server = PianoServer(
            host=self.host,
            listen=self.listenCount,
            port=self.port,
            buffer_size=2048
        )

    def start(self) -> None:
        thread_Gui = threading.Thread(target=self.start_gui)
        thread_Gui.start()
        server_thread = self.server.start_server_thread()
        print(f"Server started at {self.host}:{self.port}")

        midi = mido.MidiFile(r"resources\midi\rush E.mid")
        streamer = MidiStreamer(midi)
        for msg in streamer.get_midi_file():
            self.server.broadcast(dumps(msg))

        server_thread.join()
        print("Server stopped")

    def start_gui(self) -> None:
        self.app = ServerApp()
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?\nServer will be closed too"):
            self.server.stop_server()
            self.app.destroy()


if __name__ == '__main__':
    main = Main()
    main.start()
