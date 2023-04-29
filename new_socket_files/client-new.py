import os
import socket
import music21


def receive_files(client_socket, directory):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        filename = data.decode().strip()
        filepath = os.path.join(directory, filename)
        print(f'Receiving file {filename}')
        with open(filepath, 'wb') as f:
            while True:
                filedata = client_socket.recv(1024)
                if not filedata:
                    break
                f.write(filedata)


def main():
    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    # Receive files from server
    directory = 'receive/'
    receive_files(client_socket, directory)


if __name__ == '__main__':
    main()
