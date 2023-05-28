import shutil
from tkinter import messagebox
import customtkinter as ctk
import os
from lib.midi import MidiStreamer
from lib.net.server import PianoServer


def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)


class ServerApp(ctk.CTk):
    """
    Creates the server GUI window.
    """
    def __init__(self, server: PianoServer):
        super().__init__()

        # Initialize variables
        self.chosen_song: str = ""
        self.width = 1100
        self.height = 580
        self.server = server

        # Configure window
        self.title("Remote Pianist")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Check if MIDI directory exists and is not empty
        self.midi_dir = "resources/midi/"
        if not os.path.exists(self.midi_dir):
            messagebox.showerror("Error", f"MIDI directory '{self.midi_dir}' not found.")
            exit()
        self.midi_files = os.listdir(self.midi_dir)
        if not self.midi_files:
            messagebox.showerror("Error", f"No MIDI files found in directory '{self.midi_dir}'.")
            exit()

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Add title and clients connected label to the sidebar frame
        self.title_label = ctk.CTkLabel(self.sidebar_frame, text="Remote Pianist", anchor="center",
                                        font=("Ariel", 32))
        self.title_label.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.clients_connected_label = ctk.CTkLabel(self.sidebar_frame,
                                                    text=f"Clients: 0",
                                                    anchor="center", font=("Ariel", 25))
        self.clients_connected_label.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.chosen_song_label = ctk.CTkLabel(self.sidebar_frame,
                                              text=self.chosen_song,
                                              anchor="w",
                                              font=("Ariel", 20))
        self.chosen_song_label.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.start_sending_button = ctk.CTkButton(self.sidebar_frame, text="send", anchor="center",
                                                  font=("Ariel", 15), command=lambda: self.on_start_button())
        self.start_sending_button.grid(row=5, column=0, padx=20)

        # Add appearance mode label and option menu to the sidebar frame
        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                             values=["Light", "Dark", "System"],
                                                             command=change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Set default values
        self.appearance_mode_option_menu.set("System")

        # Create button frame
        self.button_frame = ButtonFrame(self, "resources/midi/")
        self.button_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

    def on_closing(self):
        """
        Handles the closing event of the window.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def run(self):
        """
        Runs the server GUI.
        """
        self.mainloop()

    def on_button_click(self, file_name: str):
        """
        Handles the button click event.
        """
        self.chosen_song = file_name
        print(f"Chosen song: {self.chosen_song}")

        label_text = str(self.chosen_song).rstrip(".mid")
        if len(label_text) > 20 and ' ' in label_text:
            words = label_text.split()
            label_text = '\n'.join(words)

        self.chosen_song_label.configure(text=label_text)

    def on_start_button(self):
        """
        Handles the start button click event.
        """
        connected_clients = int(self.clients_connected_label.cget("text").split(' ')[1])
        print(f"Connected clients: {connected_clients}")
        if connected_clients > 0:
            if self.chosen_song == "":
                messagebox.showerror("Error", "Please choose a song.")
            else:
                self.start_sending_button.pack_forget()
                clients = self.server.clients
                folder_path = "files_to_send/"
                streamer = MidiStreamer(f"resources/midi/{self.chosen_song}")
                midis = streamer.generate_players_midi(connected_clients)

                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                os.makedirs(folder_path)

                for i, midi in enumerate(midis):
                    midi.save(f"{folder_path}{streamer.name}-{i}.mid")
                    print(f"Saved {streamer.name}-{i}.mid")
                for i, client in enumerate(clients):
                    with open(f"{folder_path}{streamer.name}-{i}.mid", "rb") as f:
                        self.server.send(f.read(), client, f"{streamer.name}--{i}")
        else:
            messagebox.showerror("Error", "Cannot be done without clients connected.")


class ButtonFrame(ctk.CTkFrame):
    """
    Adds buttons to the server GUI based on the number of existing MIDI files.
    """

    def __init__(self, parent: ServerApp, midi_files: str):
        super().__init__(parent)
        self.midi_dir = os.listdir(midi_files)

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

            btn = ctk.CTkButton(self, text=self.midi_dir[i].rstrip(".mid").capitalize(),
                                command=lambda name=self.midi_dir[i]: parent.on_button_click(name), width=30,
                                height=50)
            btn.grid(row=self.num_rows + 1, column=self.num_cols - 1, pady=5, padx=10, sticky="nsew")

            self.num_rows += 1
