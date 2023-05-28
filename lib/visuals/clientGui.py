import customtkinter as ctk
from ..net import PianoClient
from tkinter import messagebox as msg
import re


def start_gui_client() -> None:
    """
    Starts the GUI client.
    """
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ClientApp()
    app.run()


class ClientApp(ctk.CTk):
    def __init__(self) -> None:
        """
        Initializes the client GUI.
        """
        super().__init__()
        self.window_width = 400
        self.window_height = 300
        self.client = None

        # Configure window
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)
        self.title("Client Connect")
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create frame
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        # Create widgets
        self.label_connect = ctk.CTkLabel(master=frame, text='Connect to Server', font=('Ariel', 25))
        self.ip_entry = ctk.CTkEntry(master=frame, placeholder_text="IP")
        self.port_entry = ctk.CTkEntry(master=frame, placeholder_text="Port")
        self.button = ctk.CTkButton(master=frame, text='Connect', command=self.connect)

        # Bind events
        self.bind('<KeyPress>', self.on_key_press)
        self.ip_entry.bind('<Tab>', self.focus_next_widget)
        self.port_entry.bind('<Tab>', self.focus_next_widget)

        # Pack widgets
        self.label_connect.pack(pady=12, padx=10)
        self.ip_entry.pack(pady=12, padx=10)
        self.port_entry.pack(pady=12, padx=10)
        self.button.pack(pady=12, padx=10)

    def run(self) -> None:
        """
        Runs the client GUI.
        """
        self.mainloop()

    def connect(self) -> None:
        """
        Connects to the server.
        """
        try:
            if not re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", self.getIP()):
                msg.showerror("Error", "Not a valid IP format")
                raise
            elif not (0 <= self.getPort() < 65535):
                msg.showerror("Error", "Port number must be between 0 and 65535")
                raise
            self.client = PianoClient(self.getIP(), self.getPort())
            self.client.connect()
            self.destroy()
        except ConnectionRefusedError:
            msg.showerror("Error", f"Couldn't connect to server\ncheck ip and port again (connection refused)")

    def getIP(self) -> str:
        """
        Retrieves the entered IP.
        """
        return self.ip_entry.get()

    def getPort(self) -> int:
        """
        Retrieves the entered port number.
        """
        return int(self.port_entry.get())

    def on_key_press(self, event):
        """
        Handles key press events.
        """
        if event.keysym == 'Return' and self.getIP() and self.getPort():
            self.button.invoke()

    def focus_next_widget(self, event) -> str:
        """
        Focuses on the next widget when the Tab key is pressed.
        """
        event.widget.tk_focusNext().focus()
        return "break"

    def on_closing(self) -> None:
        """
        Handles the closing event of the window.
        """
        if msg.askokcancel("Quit", "Are you sure you want to exit?"):
            self.destroy()
