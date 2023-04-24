import os
import socket
from mido import MidiFile
import tkinter


def midi_length(path):
    mid = MidiFile(path)
    return mid.length


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


if __name__ == '__main__':
    print(midi_length("../parts/opt-cropped/track_0_segment_1.mid"))
