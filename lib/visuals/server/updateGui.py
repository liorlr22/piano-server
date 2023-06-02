import threading
import time
from lib.net import PianoServer
from lib.visuals import ServerApp


class UpdateGui:
    def __init__(self, gui_app: ServerApp, server: PianoServer):
        self.app = gui_app
        self.server = server

    def update(self):
        """
        Updates reactive information in the gui of the app based on changes on the server
        """
        self.app.clients_connected_label.configure(text=f"Clients: {self.server.connected_clients}")
        time.sleep(1)

    def create_thread(self):
        def mainloop():
            while True:
                self.update()

        return threading.Thread(target=mainloop)
