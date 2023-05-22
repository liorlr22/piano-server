import socket
import threading
from typing import Union


class PianoClient:
    def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
        """
        Initializes a new instance of the PianoClient class.

        Args:
            host (str): The host address of the piano server.
            port (int): The port number of the piano server.
            buffer_size (int): The maximum number of bytes to receive at once.
            id (int): The ID of the piano client.
        """
        self.buffer_size = buffer_size
        self.host: str = host
        self.port: int = port
        self.id: Union[int, None] = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Connects the piano client to the piano server.
        Sends the client's username to the server and starts a new thread to receive messages from the server.
        """
        self.sock.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        # Send the client's username to the server.
        # self.sock.sendall(self.username.encode())

        # Start a new thread to listen for incoming messages from the server.
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, message: str) -> None:
        """
        Sends a message to the piano server.

        Args:
            message (str): The message to send.
        """
        # Send the message to the server.
        self.sock.sendall(message.encode())

    def receive_messages(self) -> None:
        """
        Receives messages from the piano server and prints them to the console.
        """
        while True:
            data = self.sock.recv(self.buffer_size)
            if not data:
                break
            message = data.decode()
            # Print the received message to the console.
            # TODO: Play message (in idea it should be a midi file with the right notes)
            print(message)

    def disconnect(self) -> None:
        """
        Disconnects the piano client from the piano server.
        """
        # Close the socket.
        self.sock.close()
