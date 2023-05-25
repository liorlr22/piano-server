import random

import mido
import music21
from pathlib import Path
from pickle import loads as pickle_loads
from pickle import dumps as pickle_dumps


def save_identical_notes(musicxml_path, value: str, output_path):
    # Load the MusicXML file
    score = music21.converter.parse(musicxml_path)

    # Create a new stream for the resulting notes
    result_stream = music21.stream.Stream()

    # Iterate over the notes in the score
    for note in score.flat.getElementsByClass('Note'):
        for lyric in note.lyrics:
            if lyric.identifier == value:
                # Add the note to the result stream
                result_stream.append(note)
            else:
                # Add a rest to the result stream
                result_stream.append(music21.note.Rest(quarterLength=note.quarterLength))
    # Save the resulting stream as a MIDI file
    result_stream.write('midi', fp=output_path)


class MidiStreamer:
    def __init__(self, midi_file: str) -> None:
        self.__midi_file = midi_file
        self.name = f"{Path(self.__midi_file).name.rstrip('.mid')}"
        self.__xml_file = f"{self.name}.xml"

    def generate_players_midi(self, players_num: int) -> list[mido.MidiFile]:
        # Read midi notes
        midi = mido.MidiFile(self.__midi_file)

        # Create an empty track for each player
        players_midi: list[mido.MidiFile] = []
        for _ in range(players_num):
            player_midi = mido.MidiFile()

            for attr in ["charset", "clip", "debug", "filename", "ticks_per_beat", "type"]:
                setattr(player_midi, attr, getattr(midi, attr))

            players_midi.append(player_midi)

        # Iterate over the tracks
        for track_index in range(len(midi.tracks)):
            # Create a new track for each player
            for player in range(len(players_midi)):
                player_track = mido.MidiTrack()
                player_track.name = midi.tracks[track_index].name

                players_midi[player].tracks.append(player_track)

            # Split Messages to each player
            for msg in midi.tracks[track_index]:
                if msg.type == "note_on":
                    selected_player: int = random.randrange(players_num)
                    for player in range(len(players_midi)):
                        if player == selected_player:
                            # Selected player plays the note (note_on message)
                            players_midi[player].tracks[track_index].append(msg)
                        else:
                            # Other players don't play the note (note_off message)
                            off_message = msg.copy(velocity=0)
                            players_midi[player].tracks[track_index].append(off_message)

                else:
                    for player_track in players_midi:
                        player_track.tracks[track_index].append(msg)
        return players_midi


if __name__ == '__main__':
    midi_file = "../../resources/midi/Gravity Falls.mid"
    streamer = MidiStreamer(midi_file)
    midis = streamer.generate_players_midi(1)
    for i, midi in enumerate(midis):
        midi.save(f"{streamer.name}-{i}.mid")
        print(f"Saved {streamer.name}-{i}.mid")
