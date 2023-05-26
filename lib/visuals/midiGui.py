import customtkinter as ctk
from ..net import PianoClient
from tkinter import messagebox as msg


class MidiApp(ctk.CTk):
    def __init__(self, client: PianoClient):
        super().__init__()

        self.window_width = 400
        self.window_height = 300
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)
        self.title("Midi Window")
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.client = client

        self.song = "song"
        self.note = "note"

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label_connect = ctk.CTkLabel(master=frame, text='Now Playing:', font=('Ariel', 32))
        self.label_song = ctk.CTkLabel(master=frame, text=f"{self.song}", font=('Ariel', 25))
        self.label_note = ctk.CTkLabel(master=frame, text=f"{self.note}", font=('Ariel', 18))

        self.label_connect.pack(pady=24, padx=10)
        self.label_song.pack(pady=10, padx=10)
        self.label_note.pack(pady=24, padx=10)

    def run(self) -> None:
        self.mainloop()

    def on_closing(self) -> None:
        if msg.askokcancel("Quit", "Are you sure you want to exit?"):
            self.destroy()
            self.client.disconnect()


if __name__ == '__main__':
    app = App()
    app.run()
