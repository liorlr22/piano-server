from music21 import *

# Load the XML file
xml_file = 'Turkish March.xml'
score = converter.parse(xml_file)

# Extract the notes and other musical elements
notes_to_parse = None
part_stream = None

# Find the first part in the score
try:
    part_stream = score.parts.stream()[0]
except:
    part_stream = score

# Get all the notes and chords in the score
notes_to_parse = part_stream.flat.notesAndRests

# Iterate over notes and print pitch and duration
for element in notes_to_parse:
    if isinstance(element, note.Note):
        print(f"Pitch: {element.pitch.nameWithOctave}, Duration: {element.duration.quarterLength}")
    elif isinstance(element, chord.Chord):
        print(f"Pitch: {element.pitchedCommonName}, Duration: {element.duration.quarterLength}")

midi_player = midi.realtime.StreamPlayer(score)
midi_player.play()
