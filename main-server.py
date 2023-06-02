from tkinter import messagebox
from lib.net import PianoServer
from lib.visuals import ServerApp
from lib.visuals.server.updateGui import UpdateGui


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
        """
        Prompt user to confirm quitting and closing the server.
        If the user confirms, the application window is destroyed,
        and the server is stopped.
        """
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?\nServer will be closed too"):
            self.app.destroy()
            self.server.stop_server()


if __name__ == '__main__':
    main = Main()
    main.start()
