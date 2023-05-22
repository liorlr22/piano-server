import random
import music21
from music21 import converter, stream
import mido


def save_identical_notes(musicxml_path, value, output_path):
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
        self.__xml_file = "example.xml"

    def midi_to_musicxml(self, user_input) -> None:
        # Parse the MIDI file
        midi_data = converter.parse(self.__midi_file)

        # Add user input as an attribute to each note in the MIDI data
        for i, element in enumerate(midi_data.recurse().notes):
            # Check if all numbers have been used as lyrics
            if i % len(user_input) == 0:
                # Shuffle the user input list randomly
                random.shuffle(user_input)

            # Add the next element from the shuffled user input list as a lyric to the current note
            element.addLyric(str(user_input[i % len(user_input)]))

        # Write the MIDI data to MusicXML
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
    midi_file = "../../resources/midi/yonatan.mid"
    streamer = MidiStreamer(midi_file)
    # streamer.midi_to_musicxml([1])
    streamer.musicxml_to_midi("output.mid")
    save_identical_notes("example.xml", "1", "output.mid")
    # TODO: rewrite midi to xml code
