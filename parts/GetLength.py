from mido import MidiFile


def get_midi_length(path):
    mid = MidiFile(path)
    return mid.length
