import threading
import time

from lib.net import PianoClient
from lib.visuals import ClientApp


# TODO: Add GUI Client
#     - Where to connect
# TODO: Add Play MIDI
#     - Create Midi FILE
#     - add midi track with same properties
#     - add midi message(s)
#     - Play Midi FILE


class Main:
    def __init__(self, ip: str, port: int) -> None:
        self.app = None
        self.client = None
        self.ip, self.port = ip, port

    def connect(self):
        if self.client is None:
            self.client = PianoClient(self.ip, self.port)
        self.client.connect()


class ClientGui:
    def __init__(self, app: ClientApp):
        self.main = Main(ip="", port=0)
        self.app = app
        self.app.run()

    def connect(self):
        if self.app.ready:
            self.main = Main(ip=self.app.getIP(), port=self.app.getPort())
            self.main.connect()


def run_client_gui():
    gui = ClientGui(app)
    gui.app.run()


if __name__ == '__main__':
    app = ClientApp()
    app.run()

    while True:
        if app.ready:
            print("ready")
            gui_thread = threading.Thread(target=run_client_gui)
            gui_thread.start()
            break
        print(False)
        time.sleep(0.1)
