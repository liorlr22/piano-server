import os
import socket
from parts import GetLength
import tkinter as tk
from tkinter import messagebox


def send_files(client_socket, directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'rb') as f:
            client_socket.sendall(filename.encode() + b'\n')
            while True:
                filedata = f.read(1024)
                if not filedata:
                    break
                client_socket.sendall(filedata)


def open_window():
    # Check if MIDI directory exists and is not empty
    midi_dir = "../resources/midi/"
    if not os.path.exists(midi_dir):
        messagebox.showerror("Error", f"MI  DI directory '{midi_dir}' not found.")
        exit()
    midi_files = os.listdir(midi_dir)
    if not midi_files:
        messagebox.showerror("Error", f"No MIDI files found in directory '{midi_dir}'.")
        exit()

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


def on_button_click(name):
    pass


def main():
    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(1)
    print('Server started, waiting for connections...')

    while True:
        # Accept incoming client connection
        client_socket, client_address = server_socket.accept()
        print(f'Client connected from {client_address}')

        # Send files to client
        directory = '../parts/opt-merged'
        send_files(client_socket, directory)

        # Close client connection
        client_socket.close()
        print(f'Connection to {client_address} closed')
