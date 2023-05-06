import threading
import time

from lib.net import PianoClient
from lib.visuals import ClientApp


# Add GUI Client
#     - Where to connect
# Add Play MIDI
#     - Create Midi FILE
#     - add midi track with same properties
#     - add midi message(s)
#     - Play Midi FILE


class Main:
    def __init__(self) -> None:
        self.app = None
        self.client = None
        self.ip, self.port = None, None

    def start(self):
        thread_gui = threading.Thread(target=self.start_gui).start()
        time.sleep(0.1)
        client_thread = threading.Thread(target=self.connect).start()

    def connect(self):
        if self.app.ready:
            self.client = PianoClient(
                host=self.ip,
                port=self.port
            )
            self.client.connect()

    def start_gui(self):
        self.app = ClientApp()
        self.app.run()


if __name__ == '__main__':
    main = Main()
    main.start()
