from lib.net import PianoServer
import mido
from pickle import dumps, loads


# GUI select midi
# Select port
# Select host
# Add Index splitting logics

def main() -> None:

    # START GUI

    server = PianoServer(
        host="0.0.0.0",
        listen=5,
        port=5000,
        buffer_size=2048
    )

    server_thread = server.start_server_thread()


    midi = mido.MidiFile(r"C:\Temp\piano-server\resources\midi\the small Jehonathan.mid")
    # Count seconds from start of midi
    # Send note on/off messages at the right time only!
    streamer = MidiStreamer(midi)
    for msg in streamer:
        server.broadcast(dumps(msg))
    # for track in midi.tracks:
    #     for msg in track:
    #         while server.connected_clients == 0:
    #             pass
    #         server.broadcast(dumps(msg))

    server_thread.join()


if __name__ == '__main__':
    main()
