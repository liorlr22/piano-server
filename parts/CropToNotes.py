from music21 import *
from music21.pitch import Pitch

# Parse MIDI file and create an object
file = converter.parse('../resources/midi/rush E.mid')

# Initialize an empty dictionary to store notes and their properties
note_arrays = {}

# Iterate through each part in the MIDI file
for part in file.parts:
    # Iterate through each element in the part
    for element in part.flat.notesAndRests:

        # If the element is a note (as opposed to a rest)
        if isinstance(element, note.Note):
            # Get the pitch of the note as a Pitch object
            pitch = Pitch(element.pitch.midi)
            # Get the duration of the note in quarter length
            duration = element.duration.quarterLength

            # If the pitch is not already in the note_arrays dictionary, add it
            if pitch not in note_arrays:
                note_arrays[pitch] = {}
            # If the part ID is not already in the dictionary for this pitch, add it
            if part.id not in note_arrays[pitch]:
                note_arrays[pitch][part.id] = {'pitches': [], 'durations': []}

            # Add the pitch and duration of the note to the appropriate arrays in the note_arrays dictionary
            note_arrays[pitch][part.id]['pitches'].append(pitch)
            note_arrays[pitch][part.id]['durations'].append(duration)

        # If the element is a chord
        elif isinstance(element, chord.Chord):
            # Iterate through each note in the chord
            for note_element in element.notes:
                # Get the pitch of the note as a Pitch object
                pitch = Pitch(note_element.pitch.midi)
                # Get the duration of the chord in quarter length (since all notes in a chord have the same duration)
                duration = element.duration.quarterLength

                # If the pitch is not already in the note_arrays dictionary, add it
                if pitch not in note_arrays:
                    note_arrays[pitch] = {}
                # If the part ID is not already in the dictionary for this pitch, add it
                if part.id not in note_arrays[pitch]:
                    note_arrays[pitch][part.id] = {'pitches': [], 'durations': []}

                # Add the pitch and duration of the note to the appropriate arrays in the note_arrays dictionary
                note_arrays[pitch][part.id]['pitches'].append(pitch)
                note_arrays[pitch][part.id]['durations'].append(duration)

# Iterate through each pitch in the note_arrays dictionary
for pitch, channel_arrays in note_arrays.items():
    # Get the name of the pitch as a string (e.g. "C#4")
    note_name = pitch.nameWithOctave
    # Iterate through each channel in the dictionary for this pitch
    for channel, arrays in channel_arrays.items():
        # Print the pitches and durations for this pitch and channel
        print(f"Note {note_name} in channel {channel}: {arrays['pitches']}")
        print(f"Duration {note_name} in channel {channel}: {arrays['durations']}")
