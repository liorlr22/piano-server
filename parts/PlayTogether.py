import mido
from mido import MidiFile
import threading
import pygame
from music21 import midi, stream, converter
from time import sleep
import miditime.miditime as miditime


def get_midi_length(path):
    mid = MidiFile(path)
    return mid.length


# Define a function to play a MIDI file in real-time from a specific time

def play_midi_from_time(midi_file, start_time, end_time=None):
    if end_time is None:
        end_time = get_midi_length(midi_file)

    mid = mido.MidiFile(midi_file)
    new_mid = mido.MidiFile()

    # Iterate through the MIDI tracks
    for track in mid.tracks:
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)

        # Iterate through the MIDI messages in the track
        time = 0
        for msg in track:
            time += msg.time

            # If the message is in the time range, add it to the new track
            if start_time * mid.ticks_per_beat <= time <= end_time * mid.ticks_per_beat:
                new_msg = msg.copy(time=time)
                new_track.append(new_msg)

                # If the end of the range has been reached, stop iterating
                if time >= end_time * mid.ticks_per_beat:
                    break

    # Save the new MIDI file
    new_mid.save('cut.mid')


def play_midi_files(path):
    # Load each MIDI file as a stream
    streams = [midi.translate.midiFilePathToStream(path)]

    # Combine the streams into a single stream
    combined_stream = stream.Score()
    for s in streams:
        combined_stream.append(s)

    # Create a MIDI output object for real-time playback
    output = midi.realtime.StreamPlayer(combined_stream)

    # Play the stream in real-time
    output.play()


if __name__ == '__main__':
    # files = ["opt-cropped/track_0_segment_3.mid", "opt-cropped/track_1_segment_3.mid"]
    # for t in files:
    #     th = threading.Thread(target=play_midi_files, args=[t])
    #     th.start()

    origin_file = "../resources/midi/rush E.mid"
    origin_file_length = get_midi_length(origin_file)

    file1 = "opt-cropped/track_0_segment_142.mid"
    file2 = "opt-cropped/track_1_segment_8.mid"

    segment_number = file1.split("_")[3].rstrip(".mid")
    sum_time_before = 0.0
    for i in range(int(segment_number)):
        f = f"opt-cropped/track_0_segment_{i}.mid"
        sum_time_before += get_midi_length(f)

    needed_time = origin_file_length - sum_time_before

    play_midi_from_time(file2, 0.8)
