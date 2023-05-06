import mido
import typing


class MidiStreamer:
    def __init__(self, midi_file: mido.MidiFile):
        self.__midi_file = midi_file

    def get_midi_file(self) -> mido.MidiFile:
        return self.__midi_file

