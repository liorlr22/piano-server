import pickle
import socket
import struct
import threading
import time
import music21 as m21
from music21.midi import realtime

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
    #
    # n_c = pickle.loads(serialized)
    # for n in n_c:
    #     play(str(n))

    midi_file = m21.stream.Stream()

    toPlay = pickle.loads(serialized)
    for i in toPlay:
        midi_file.append(i)

    midi_out = m21.midi.realtime.StreamPlayer(midi_file)
    midi_out.play()
    time.sleep(midi_file.duration.quarterLength)  # Wait for the song to finish playing


def play(n):
    try:
        n = eval(n)
    except:
        n = n
    stream = music21.stream.Stream()
    if type(n) == float:
        note = music21.note.Rest()
        note.duration = music21.duration.Duration(n)
        stream.append(note)
    else:
        try:
            note = music21.note.Note(n[0])
            note.duration = music21.duration.Duration(n[1])
            stream.append(note)
        except:
            chord = music21.chord.Chord(n[0])
            chord.duration = music21.duration.Duration(n[1])
            stream.append(chord)

    realtime.StreamPlayer(stream).play()


# Start a new thread to receive messages from the server
t = threading.Thread(target=receive)
t.start()
