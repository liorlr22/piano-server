import os
import shutil
import socket
import struct
import threading
from typing import Union
from music21 import converter, midi
import pygame
from pickle import loads as pickle_loads
from ..visuals.client.midiGui import MidiApp


class PianoClient:
    def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
        """
        Initializes a new instance of the PianoClient class.

        Args:
            host (str): The host address of the piano server.
            port (int): The port number of the piano server.
            buffer_size (int): The maximum number of bytes to receive at once.
        """
        self.midi_player = None
        self.app = None
        self.buffer_size = buffer_size
        self.host: str = host
        self.port: int = port
        self.id: Union[int, None] = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run: bool = False

        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2)
        pygame.mixer.init()

        # TODO: check for running again without delay

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
                self.run = False

                folder_path = "recv/"
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                os.makedirs(folder_path)

                filename: str = self.sock.recv(1024).decode()
                message_header = self.sock.recv(8)
                message_length = struct.unpack('>Q', message_header)[0]

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
                if not self.run:
                    mid = f"recv/{filename}.mid"
                    # threading.Thread(target=self.handle_stop_music).start()
                    self.handle_midi_file(mid)
                    print("out")
                    self.run = True
                continue

    def disconnect(self) -> None:
        """
        Disconnects the piano client from the piano server.
        """
        # Close the socket.
        self.sock.close()

    def handle_midi_file(self, filename: str) -> None:
        def play_midi_file(filename: str) -> None:
            print("playing file")
            score = converter.parse(filename)
            self.midi_player = midi.realtime.StreamPlayer(score)
            self.midi_player.play()
            print("stopped playing file")
            self.app.stop()

        music_thread = threading.Thread(target=play_midi_file, args=[filename])
        music_thread.start()

        print("running midi")
        self.app = MidiApp()
        filename = str(filename).rstrip(".mid")
        if len(filename) > 20 and ' ' in filename:
            words = filename.split()
            filename = '\n'.join(words)
        filename = filename.split("/")[1].split("--")[0]
        self.app.label_song.configure(text=filename)
        self.app.run()

    def handle_stop_music(self) -> None:
        print("in")
        self.app.stop()
        self.midi_player.stop()

