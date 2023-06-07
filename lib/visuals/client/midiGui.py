import socket

import customtkinter as ctk
from tkinter import messagebox as msg


class MidiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.window_width = 400
        self.window_height = 300
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)
        self.title("Midi Window")
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.song = "song"

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label_play = ctk.CTkLabel(master=frame, text='Now Playing:', font=('Ariel', 32))
        self.label_song = ctk.CTkLabel(master=frame, text=f"{self.song.capitalize()}", font=('Ariel', 25))

        self.label_play.pack(pady=24, padx=10)
        self.label_song.pack(pady=15, padx=10)

    def run(self) -> None:
        self.mainloop()

    def on_closing(self) -> None:
        if msg.askokcancel("Quit", "Are you sure you want to exit?"):
            self.destroy()

    def stop(self) -> None:
        self.destroy()
