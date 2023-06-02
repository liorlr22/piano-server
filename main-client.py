from lib.visuals.client.clientGui import ClientApp


class Main:
    def __init__(self) -> None:
        self.app = ClientApp()

    def run_gui(self):
        """
        Starts the GUI application by running the app's main loop.
        """
        self.app.run()


if __name__ == '__main__':
    gui = Main()
    gui.run_gui()
