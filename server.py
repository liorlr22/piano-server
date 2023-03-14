import os
import pickle
import socket
import struct
import threading
import tkinter as tk
from tkinter import messagebox
import music21 as m21

# List to hold connected clients
clients = []
notes_to_parse = None
part_stream = None
to_play = []


def play(f):
    global to_play
    to_play = []
    midi_file = m21.converter.parse(f'resources/midi/{f}')
    # for element in midi_file.flat.notesAndRests:
    #     if isinstance(element, m21.note.Note):
    #         to_play.append(element)
    #     elif isinstance(element, m21.chord.Chord):
    #         to_play.append(element)
    #     elif isinstance(element, m21.note.Rest):
    #         to_play.append(element)

    # Iterate over each element (note, chord, rest) in the MIDI file
    for element in midi_file.flat:
        # If the element is a Note or Chord, append it to the list
        if isinstance(element, m21.note.Note) or isinstance(element, m21.chord.Chord):
            to_play.append(element)
        # If the element is a Rest, create a new Rest object with the same duration
        # and append it to the list
        elif isinstance(element, m21.note.Rest):
            rest_duration = element.duration.quarterLength
            rest = m21.note.Rest()
            rest.duration = m21.duration.Duration(rest_duration)
            to_play.append(rest)


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
            response = f"Client {clientaddr} said: {message}"

            # Send the response back to the client
            clientsocket.send(response.encode('utf-8'))

            # Send the message to all other clients
            for c in clients:
                if c != clientsocket:
                    c.send(response.encode('utf-8'))
        except socket.error as e:
            # Client socket error occurred, assume client has disconnected
            messagebox.showerror("Error", f"Client disconnected with error '{e}'.")
            break

    # Remove the client from the list of connected clients
    clients.remove(clientsocket)

    # Close the client socket
    clientsocket.close()


def server_console():
    # This function listens for input from the server console
    while True:
        message = input(" ")
        for c in clients:
            c.send(message.encode('utf-8'))


def start_server():
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

        print(f"Got a connection from {clientaddr}")

        # Add the client to the list of connected clients
        clients.append(clientsocket)

        # Start a new thread to handle the client connection
        t = threading.Thread(target=handle_client, args=(clientsocket, clientaddr))
        t.start()


def run_server():
    server_thread = threading.Thread(target=start_server)
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
            print(to_play)
            serialized = pickle.dumps(to_play)
            message = struct.pack('>Q', len(serialized)) + serialized
            for conn in clients:
                conn.sendall(message)

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

    # Add label for the number of connected clients
    num_clients_label = tk.Label(frame, text="Clients: 0", font=("Arial", 16))
    num_clients_label.grid(row=1, column=0, pady=10, sticky="w", columnspan=5)

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
    server = threading.Thread(target=start_server)
    window = threading.Thread(target=open_window)

    server.start()
    window.start()
