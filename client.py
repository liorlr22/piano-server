
try:
    import time
    import pickle
    import socket
    import struct
    import threading
    import music21 as m21
    import music21.note
    from music21.midi import realtime
except ModuleNotFoundError as e:
    print(e)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Reserve a port for your service.
port = 9999

# Connect to the server
client_socket.connect((host, port))
print("Connected To Server")

n_c = []
serialized = []


# Function to receive messages from the server
def receive():
    global n_c, serialized
    message_header = client_socket.recv(8)
    message_length = struct.unpack('>Q', message_header)[0]
    #
    serialized = b''
    while len(serialized) < message_length:
        remaining = message_length - len(serialized)
        data = client_socket.recv(min(remaining, 2048))
        if not data:
            break
        serialized += data

    midi_file = m21.stream.Stream()

    toPlay = pickle.loads(serialized)
    for element in toPlay:
        element.show('midi')
        time.sleep(element.duration.quarterLength)
    midi_out = m21.midi.realtime.StreamPlayer(midi_file)
    midi_out.play()


# Start a new thread to receive messages from the server
t = threading.Thread(target=receive)
t.start()
