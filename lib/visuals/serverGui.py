import threading
from tkinter import messagebox
import customtkinter as ctk
import os


def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)


def on_button_click(file_name: str):
    print(file_name)


def start_gui_server():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ServerApp()
    app.run()


class ServerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.width = 1100
        self.height = 580

        # configure window
        self.title("Remote Pianist")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.clients_connected_count = 0
        # Check if MIDI directory exists and is not empty
        self.midi_dir = "resources/midi/"
        if not os.path.exists(self.midi_dir):
            messagebox.showerror("Error", f"MIDI directory '{self.midi_dir}' not found.")
            exit()
        self.midi_files = os.listdir(self.midi_dir)
        if not self.midi_files:
            messagebox.showerror("Error", f"No MIDI files found in directory '{self.midi_dir}'.")
            exit()

        # create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # add title and clients connected label to the sidebar frame
        self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Remote Pianist", anchor="center",
                                        font=("Ariel", 32))
        self.title_label.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.clients_connected_label = ctk.CTkLabel(self.sidebar_frame,
                                                    text=f"Clients: {self.clients_connected_count}",
                                                    anchor="center", font=("Ariel", 25))
        self.clients_connected_label.grid(row=3, column=0, padx=20, pady=(10, 10))

        # add appearance mode label and option menu to the sidebar frame
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w",
                                                  font=("Ariel", 15))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                             values=["Light", "Dark", "System"],
                                                             command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # set default values
        self.appearance_mode_option_menu.set("System")

        # create button frame
        self.button_frame = ButtonFrame(self, "resources/midi/")
        self.button_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def run(self):
        self.mainloop()


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, midi_files):
        super().__init__(parent)
        self.midi_dir = os.listdir(midi_files)

        # Calculate number of columns needed
        self.num_files = len(self.midi_dir)
        self.max_rows = 9
        self.max_cols = 5
        self.num_cols = 1
        self.num_rows = 0

        # Add MIDI buttons to the frame
        for i in range(self.num_files):
            # Check if current column is full
            if self.num_rows >= self.max_rows:
                self.num_cols += 1
                self.num_rows = 0

            btn = ctk.CTkButton(self, text=self.midi_dir[i].rstrip(".mid"),
                                command=lambda name=self.midi_dir[i]: on_button_click(name), width=30,
                                height=50)
            btn.grid(row=self.num_rows + 1, column=self.num_cols - 1, pady=5, padx=10, sticky="nsew")

            self.num_rows += 1


if __name__ == '__main__':
    window_thread = threading.Thread(target=start_gui_server())

    window_thread.start()
