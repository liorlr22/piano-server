import threading
from tkinter import messagebox
import mido
from pickle import dumps, loads
from lib.net import PianoServer
from lib.visuals import ServerApp
from lib.visuals.updateGui import UpdateGui


# Select port
# Select host
# Add Index splitting logics


class Main:
    def __init__(self) -> None:
        self.host = "0.0.0.0"
        self.port = 5000
        self.listenCount = 5
        self.server = PianoServer(
            host=self.host,
            listen=self.listenCount,
            port=self.port,
            buffer_size=2048
        )

        self.app = ServerApp(self.server)
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start(self) -> None:
        threads = [
            self.server.create_thread(),
            UpdateGui(self.app, self.server).create_thread()
        ]

        for thread in threads:
            thread.start()

        self.app.mainloop()

    def on_closing(self) -> None:
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?\nServer will be closed too"):
            self.app.destroy()
            self.server.stop_server()


if __name__ == '__main__':
    main = Main()
    main.start()
