import random
from music21 import converter
import mido


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

    def musicxml_to_midi(self, output_file_path) -> None:
        musicxml_data = converter.parse(self.__xml_file)

        # Retrieve the lyrics from the MusicXML data
        lyrics = []
        for element in musicxml_data.recurse().notes:
            lyric = element.lyric
            if isinstance(lyric, str):
                lyrics.append(lyric)
            elif hasattr(lyric, 'text'):
                lyrics.append(lyric.text)

        # Write the MusicXML data to MIDI
        musicxml_data.write('midi', output_file_path)


def get_range(number) -> list:
    """
    This function takes a number as input and returns a list of numbers from 1 to that number.

    Args:
      number: The number to generate a list of numbers from.

    Returns:
      A list of numbers from 1 to the input number.
    """

    list_of_numbers = ['*']
    for i in range(1, number + 1):
        list_of_numbers.append(i)

    return list_of_numbers


if __name__ == '__main__':
    midi_file = "../../resources/midi/Little Jonny.mid"
    streamer = MidiStreamer(midi_file)
    streamer.midi_to_musicxml(get_range(2))
    streamer.musicxml_to_midi("example.midi")
