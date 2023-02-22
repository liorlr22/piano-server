import socket
import threading

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service.
port = 9999

# Connect to the server
client_socket.connect((host, port))
print("Connected To Server")


# Function to receive messages from the server
def receive():
    while True:
        # Receive the response from the server
        response = client_socket.recv(1024)

        # Print the response
        print(response.decode('utf-8'))


# Start a new thread to receive messages from the server
t = threading.Thread(target=receive)
t.start()
