import socket
import threading
import os
import time

from music21 import *
import tkinter as tk
from tkinter import messagebox

# List to hold connected clients
clients = []
notes_to_parse = None
part_stream = None

to_play = []


def play(f):
    global to_play
    us = environment.UserSettings()
    us.autoDownload = 'allow'
    # Load the XML file
    file = f'resources/midi/{f}'
    score = converter.parse(file)

    # Extract the notes and other musical elements

    # Find the first part in the score
    try:
        part_stream = score.parts.stream()[0]
    except:
        part_stream = score

    # Get all the notes and chords in the score
    notes_to_parse = part_stream.flat.notesAndRests
    # Iterate over notes and print pitch and duration
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            to_play.append((element.pitch.nameWithOctave, element.duration.quarterLength))
        elif isinstance(element, chord.Chord):
            to_play.append((element.pitchedCommonName, element.duration.quarterLength))

    # midi_file = 'output.mid'
    # midi_player = midi.realtime.StreamPlayer(score)
    # midi_player.play()
    # score.write('midi', fp=midi_file)


def handle_client(clientsocket, clientaddr):
    # This function will handle each client connection in a separate thread
    while True:
        try:
            # Receive data from the client
            data = clientsocket.recv(1024)

            if not data:
                # Client disconnected
                break

            # Process the received data
            message = data.decode('utf-8')
            response = "Client {} said: {}".format(clientaddr, message)

            # Send the response back to the client
            clientsocket.send(response.encode('utf-8'))

            # Send the message to all other clients
            for c in clients:
                if c != clientsocket:
                    c.send(response.encode('utf-8'))
        except socket.error as e:
            # Client socket error occurred, assume client has disconnected
            print("> Client disconnected with error")
            break

    # Remove the client from the list of connected clients
    clients.remove(clientsocket)

    # Close the client socket
    clientsocket.close()


def server_console():
    # This function listens for input from the server console
    while True:
        message = str(input("> "))
        for c in clients:
            c.send(message.encode('utf-8'))


def startServer():
    # Create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service.
    port = 9999

    # Bind the socket to a specific address and port
    serversocket.bind((host, port))

    # Listen for incoming connections
    serversocket.listen(5)

    # Start the server console thread
    t = threading.Thread(target=server_console)
    t.start()

    while True:
        # Wait for a connection
        clientsocket, clientaddr = serversocket.accept()

        print(f"Got a connection from {str(clientaddr)}")

        # Add the client to the list of connected clients
        clients.append(clientsocket)

        # Start a new thread to handle the client connection
        t = threading.Thread(target=handle_client, args=(clientsocket, clientaddr))
        t.start()


def run_server():
    server_thread = threading.Thread(target=startServer())
    server_thread.start()


def open_window():
    # Check if MIDI directory exists and is not empty
    midi_dir = "resources/midi/"
    if not os.path.exists(midi_dir):
        messagebox.showerror("Error", f"MIDI directory '{midi_dir}' not found.")
        exit()
    midi_files = os.listdir(midi_dir)
    if not midi_files:
        messagebox.showerror("Error", f"No MIDI files found in directory '{midi_dir}'.")
        exit()

    def on_button_click(name):
        def playMusic():
            global to_play
            play(name)
            # Send the name of the MIDI file to the server
            for p in to_play:
                message = str(p)
                for c in clients:
                    c.send(message.encode('utf-8'))

        threading.Thread(target=playMusic).start()

    # Create a tkinter window
    window = tk.Tk()
    window.title("Piano Server")
    window.resizable(width=False, height=False)

    # Create a frame in the center
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add title label to the frame
    title = tk.Label(frame, text="Piano Server", font=("Arial", 24))
    title.grid(row=0, column=0, pady=20, sticky="n", columnspan=len(midi_files))

    # Calculate number of columns needed
    num_files = len(midi_files)
    max_rows = 10  # maximum number of rows per column
    max_cols = 5  # maximum number of columns
    num_cols = min(max(1, num_files // max_rows), max_cols)
    num_rows = (num_files + num_cols - 1) // num_cols

    # Add MIDI buttons to the frame
    for i in range(num_files):
        btn = tk.Button(frame, text=midi_files[i].rstrip(".mid"), padx=10,
                        command=lambda name=midi_files[i]: on_button_click(name),
                        width=15, wraplength=100, height=2)
        btn.grid(row=(i // num_cols) + 1, column=i % num_cols, pady=5)

    # Run the main loop
    window.mainloop()


if __name__ == '__main__':
    server = threading.Thread(target=run_server)
    window = threading.Thread(target=open_window)

    server.start()
    window.start()
