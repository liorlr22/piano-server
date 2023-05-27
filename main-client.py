from lib.visuals import ClientApp

class Main:
    def __init__(self) -> None:
        self.app = ClientApp()

    def run_gui(self):
        self.app.run()


if __name__ == '__main__':
    gui = Main()
    gui.run_gui()
