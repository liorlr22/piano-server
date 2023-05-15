from lib.visuals import ClientApp


# TODO: Add Play MIDI
#     - Create Midi FILE
#     - add midi track with same properties
#     - add midi message(s)
#     - Play Midi FILE

class Main:
    def __init__(self) -> None:
        self.app = ClientApp()

    def run_gui(self):
        self.app.run()


if __name__ == '__main__':
    gui = Main()
    gui.run_gui()
