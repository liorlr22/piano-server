from music21 import midi, stream


def play_midi_files(paths):
    # Load each MIDI file as a stream
    streams = [midi.translate.midiFilePathToStream(path) for path in paths]

    # Combine the streams into a single stream
    combined_stream = stream.Score()
    for s in streams:
        combined_stream.append(s)

    # Create a MIDI output object for real-time playback
    output = midi.realtime.StreamPlayer(combined_stream)

    # Play the stream in real-time
    output.play()


if __name__ == '__main__':
    play_midi_files(["opt-cropped/track_0_segment_3.mid", "opt-cropped/track_1_segment_3.mid"])

