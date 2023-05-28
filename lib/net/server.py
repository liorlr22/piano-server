import socket
import threading
from typing import List, Optional
from pickle import dumps as pickle_dumps
import struct


class PianoServer:
    """
    A class that represents a piano server.

    Attributes:
        host (str): The host address to bind the server socket to.
        port (int): The port number to bind the server socket to.
        listen (int): The maximum number of queued connections (listen backlog).
        buffer_size (int): The maximum number of bytes to receive at once.
        sock (socket): The server socket.
        clients (list): A list of client sockets connected to the server.
    """

    def __init__(self, host: str, port: int, listen: int = 10, buffer_size: int = 2048) -> None:
        """
        Initializes a new instance of the PianoServer class.

        Args:
            host (str): The host address to bind the server socket to.
            port (int): The port number to bind the server socket to.
            listen (int): The maximum number of queued connections (listen backlog).
            buffer_size (int): The maximum number of bytes to receive at once.
        """
        self.host = host
        self.port = port
        self.listen = listen
        self.buffer_size = buffer_size
        assert 0 <= self.port < 65535, "Port number must be between 0 and 65535"
        if self.port == 0:
            print("Warning: Port number is 0, a random open port will be chosen")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: List[socket.socket] = []

    def start_server(self) -> None:
        """
        Starts the piano server and listens for incoming client connections.
        Creates a new thread for each connected client to handle communication.
        """
        # Bind the server socket to the host and port.
        self.sock.bind((self.host, self.port))

        self.sock.listen(self.listen)
        host, port = self.sock.getsockname()
        print(f"Server listening on {host}:{port}")

        while True:
            # Accept a new client connection.
            client, addr = self.sock.accept()
            # Create a new thread to handle communication with the client.

            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def stop_server(self) -> None:
        """
        Stops the piano server by closing the server socket and all client sockets.
        """
        if self.clients:
            # Close all client sockets.
            for client in self.clients:
                client.close()
            self.clients.clear()

        # Close the server socket.
        self.sock.close()

    def create_thread(self) -> threading.Thread:
        """
        Starts the piano server in a new thread and listens for incoming client connections.
        """
        return threading.Thread(target=self.start_server, args=())

    @property
    def connected_clients(self) -> int:
        return len(self.clients)

    def handle_client(self, client: socket.socket) -> None:
        """
        Handles communication with a connected client.
        Adds the client to the list of connected clients.

        Args:
            client (socket): The client socket to handle communication with.
        """
        self.clients.append(client)
        print(f"Client connected at {client}")

        while True:
            # pass
            # Receive data from the client.
            try:
                data: bytes = client.recv(self.buffer_size)
                if data:
                    pass
            except Exception as e:
                # If no data is received, the client has disconnected.
                self.clients.remove(client)

    def send(self, data: bytes, receiver: socket.socket, filename: str):
        """
        Sends the provided data to the specified receiver socket along with the filename.

        Args:
            data (bytes): The data to be sent.
            receiver (socket.socket): The socket to which the data should be sent.
            filename (str): The name of the file being sent.

        Returns:
            None
        """

        receiver.send(filename.encode())
        serialized = pickle_dumps(data)
        message = struct.pack('>Q', len(serialized)) + serialized
        receiver.send(message)

    def broadcast(self, data: bytes, sender: Optional[socket.socket] = None) -> None:
        """
        Broadcasts a message to all connected clients except for the sender.

        Args:
            data (bytes): The message to broadcast.
            sender (socket): The client socket that sent the message.
        """
        for client in self.clients:
            if sender and client == sender:
                continue
            serialized = pickle_dumps(data)
            message = struct.pack('>Q', len(serialized)) + serialized
            client.sendall(message)
