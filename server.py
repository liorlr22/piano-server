import socket
import threading
import os
from music21 import *
import tkinter as tk
from tkinter import font as tkfont

# List to hold connected clients
clients = []


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: [controller.show_frame("PageOne"), run_server()])
        button1.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


def play():
    # Load the XML file
    midi_files = os.listdir("resources/midi/")
    xml_files = os.listdir("resources/xml/")
    file = 'resources/midi/Killer Queen.mid'
    score = converter.parse(file)

    # Extract the notes and other musical elements
    notes_to_parse = None
    part_stream = None

    # Find the first part in the score
    try:
        part_stream = score.parts.stream()[0]
    except:
        part_stream = score

    # Get all the notes and chords in the score
    notes_to_parse = part_stream.flat.notesAndRests
    # Iterate over notes and print pitch and duration
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            print(f"Pitch: {element.pitch.nameWithOctave}, Duration: {element.duration.quarterLength}")
        elif isinstance(element, chord.Chord):
            print(f"Pitch: {element.pitchedCommonName}, Duration: {element.duration.quarterLength}")

    midi_file = 'output.mid'
    midi_player = midi.realtime.StreamPlayer(score)
    midi_player.play()
    score.write('midi', fp=midi_file)


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
            response = "Client {} said: {}".format(clientaddr, message)

            # Send the response back to the client
            clientsocket.send(response.encode('utf-8'))

            # Send the message to all other clients
            for c in clients:
                if c != clientsocket:
                    c.send(response.encode('utf-8'))
        except socket.error as e:
            # Client socket error occurred, assume client has disconnected
            print("> Client disconnected with error")
            play()
            break

    # Remove the client from the list of connected clients
    clients.remove(clientsocket)

    # Close the client socket
    clientsocket.close()


def server_console():
    # This function listens for input from the server console
    while True:
        message = input("> enter message: ")
        response = f"> Server said: {message}"
        for c in clients:
            c.send(response.encode('utf-8'))


def startServer():
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

        print("Got a connection from %s" % str(clientaddr))

        # Add the client to the list of connected clients
        clients.append(clientsocket)

        # Start a new thread to handle the client connection
        t = threading.Thread(target=handle_client, args=(clientsocket, clientaddr))
        t.start()


def run_server():
    server_thread = threading.Thread(target=startServer())
    server_thread.start()


if __name__ == '__main__':
    window = SampleApp()

    # Run the Tkinter event loop
    window.mainloop()
