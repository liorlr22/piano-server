import socket
import threading
from tkinter import messagebox
import customtkinter
import os


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def on_button_click(file_name: str):
    print(file_name)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Remote Pianist")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("../resources/pictures/electric.ico")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.clients_connected_count = 0
        # Check if MIDI directory exists and is not empty
        self.midi_dir = "../resources/midi/"
        if not os.path.exists(self.midi_dir):
            messagebox.showerror("Error", f"MIDI directory '{self.midi_dir}' not found.")
            exit()
        self.midi_files = os.listdir(self.midi_dir)
        if not self.midi_files:
            messagebox.showerror("Error", f"No MIDI files found in directory '{self.midi_dir}'.")
            exit()

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Remote Pianist", anchor="center",
                                                  font=("Ariel", 32))
        self.title_label.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.clients_connected_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                              text=f"Clients: {self.clients_connected_count}",
                                                              anchor="center", font=("Ariel", 25))
        self.clients_connected_label.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w",
                                                            font=("Ariel", 15))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # set default values
        self.appearance_mode_option_menu.set("System")

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Calculate number of columns needed
        self.num_files = len(self.midi_files)
        self.max_rows = 10  # maximum number of rows per column
        self.max_cols = 5  # maximum number of columns
        self.num_cols = min(max(1, self.num_files // self.max_rows), self.max_cols)
        self.num_rows = (self.num_files + self.num_cols - 1) // self.num_cols

        # Add MIDI buttons to the frame
        for i in range(self.num_files):
            btn = customtkinter.CTkButton(self.button_frame, text=self.midi_files[i].rstrip(".mid").capitalize(),
                                          command=lambda name=self.midi_files[i]: on_button_click(name))
            btn.grid(row=(i // self.num_cols) + 1, column=i % self.num_cols, pady=5, padx=10, sticky="nsew")


if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()
