import os
import shutil
import socket
import struct
import threading
from typing import Union
from music21 import converter, midi
from pickle import loads as pickle_loads
from ..visuals import midiGui


class PianoClient:
    def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
        """
        Initializes a new instance of the PianoClient class.

        Args:
            host (str): The host address of the piano server.
            port (int): The port number of the piano server.
            buffer_size (int): The maximum number of bytes to receive at once.
        """
        self.buffer_size = buffer_size
        self.host: str = host
        self.port: int = port
        self.id: Union[int, None] = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Connects the piano client to the piano server.
        Starts a new thread to receive messages from the server.
        """
        self.sock.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

        # Start a new thread to listen for incoming messages from the server.
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self) -> None:
        """
        Receives messages from the piano server
        """
        while True:
            try:
                folder_path = "recv/"
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                os.makedirs(folder_path)

                filename: str = self.sock.recv(1024).decode()
                message_header = self.sock.recv(8)
                message_length = struct.unpack('>Q', message_header)[0]
                #
                serialized = b''
                while len(serialized) < message_length:
                    remaining = message_length - len(serialized)
                    data = self.sock.recv(min(remaining, 2048))
                    if not data:
                        break
                    serialized += data
                print("stop data")
                # Save the received MIDI data to a file
                with open(f"{folder_path}{filename}.mid", "wb+") as file:
                    file.write(pickle_loads(serialized))
                    file.close()

                print(f"MIDI file received: {filename}")

            except Exception as e:
                print(f"Error occurred: {str(e)}")
            finally:
                mid = f"recv/{filename}.mid"
                play_midi_file(mid)
                continue

    def disconnect(self) -> None:
        """
        Disconnects the piano client from the piano server.
        """
        # Close the socket.
        self.sock.close()


def play_midi_file(filename: str) -> None:
    app = midiGui.MidiApp()
    app.label_song.configure(text=filename)
    app_thread = threading.Thread(target=app.run)
    app_thread.start()

    score = converter.parse(filename)
    midi_player = midi.realtime.StreamPlayer(score)
    midi_player.play()
