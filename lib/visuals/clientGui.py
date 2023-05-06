import customtkinter as ctk
from ..net import PianoClient


def start_gui_client():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ClientApp()
    app.run()


class ClientApp(ctk.CTk):

    def __init__(self, connect_callback: callable = None):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.width = 400
        self.height = 300
        self.client = None
        self.on_connect = connect_callback

        self.app = ctk.CTk()
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.resizable(False, False)
        self.app.title("Client Connect")
        # self.iconbitmap("resources/pictures/electric.ico")
        # TODO: Uncomment line above when icon is ready

        frame = ctk.CTkFrame(master=self.app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label_connect = ctk.CTkLabel(master=frame, text='Connect to Server', font=('Ariel', 25))
        self.label_connect.pack(pady=12, padx=10)

        self.ip_entry = ctk.CTkEntry(master=frame, placeholder_text="IP")
        self.ip_entry.pack(pady=12, padx=10)

        self.port_entry = ctk.CTkEntry(master=frame, placeholder_text="Port")
        self.port_entry.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Connect', command=self.connect)
        button.pack(pady=12, padx=10)

    def run(self):
        self.app.mainloop()

    def connect(self):
        self.client = PianoClient(self.getIP(), self.getPort())
        self.client.connect()
        # TODO: add handling for connection failure
        # TODO: add GUI for playing midi

    def getIP(self) -> str:
        return self.ip_entry.get()

    def getPort(self) -> int:
        return int(self.port_entry.get())


if __name__ == '__main__':
    start_gui_client()
