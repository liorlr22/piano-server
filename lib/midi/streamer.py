import random
import music21
from music21 import converter, stream
from pathlib import Path


def save_identical_notes(musicxml_path, value: str, output_path):
    # Load the MusicXML file
    score = music21.converter.parse(musicxml_path)

    # Create a new stream for the resulting notes
    result_stream = music21.stream.Stream()

    # Iterate over the notes in the score
    for note in score.flat.getElementsByClass('Note'):
        for lyric in note.lyrics:
            if lyric.text == value:
                # Add the note to the result stream
                result_stream.append(note)
    # Save the resulting stream as a MIDI file
    result_stream.write('midi', fp=output_path)


class MidiStreamer:
    def __init__(self, midi_file: str) -> None:
        self.__midi_file = midi_file
        self.name = f"{Path(self.__midi_file).name.rstrip('.mid')}"
        self.__xml_file = f"{self.name}.xml"

    def midi_to_musicxml(self, lyrics) -> None:
        midi_data = converter.parse(self.__midi_file)

        notes = midi_data.recurse().notes
        for note in notes:
            if lyrics:
                random_lyric = random.choice(lyrics)
                lyric = music21.note.Lyric(random_lyric)
                note.lyrics.append(lyric)
        midi_data.write('musicxml', self.__xml_file)

    def musicxml_to_midi(self, output_file_path: str) -> None:
        musicxml_data = converter.parse(self.__xml_file)
        musicxml_data.write('midi', output_file_path)


def get_range(number: int) -> list:
    """
    This function takes a number as input and returns a list of numbers from 1 to that number.

    Args:
      number: The number to generate a list of numbers from.

    Returns:
      A list of numbers from 1 to the input number.
    """

    assert number >= 0, "number must be higher or equal to 0"
    list_of_numbers = []
    for i in range(1, number + 1):
        list_of_numbers.append(i)

    return list_of_numbers


if __name__ == '__main__':
    midi_file = "../../resources/midi/rush E.mid"
    streamer = MidiStreamer(midi_file)
    streamer.midi_to_musicxml(get_range(1))
    save_identical_notes(f"{streamer.name}.xml", "1", f"{streamer.name}.mid")

# TODO: the problem with my code is that somewhere between the conversion from musicXML to midi there are new notes
#  that are added to the midi. without lyrics the program works great (from midi to xml and back)
