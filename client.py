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
        play(response.decode())


def play(n):
    #continue here
    pass

    # create a music21 note object for the C# note
    note_obj = note.Note('C#')

    # get the pitch object for the note
    pitch_obj = note_obj.pitch

    # get the frequency of the pitch object
    frequency = pitch_obj.frequency

    # create a Tone object at the frequency of the C# note
    c_sharp = Tone(frequency)

    # generate a sine wave at the C# frequency for 1.5 seconds
    chord = c_sharp.to_audio_segment(duration=1500)

    # play the chord
    chord.play()


# Start a new thread to receive messages from the server
t = threading.Thread(target=receive)
t.start()
