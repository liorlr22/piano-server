try:
    import mido
    from parts.DeleteFolderContents import delete
    from parts.GetTempo import temp
    from pathlib import Path
    from shutil import rmtree
except ModuleNotFoundError as e:
    import subprocess
    print(f"Error: {e}")
    command = 'pip install -r requirements.txt'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    raise

FOLDER = Path('opt-cropped/')

def create_midi_part(track, ref_midi):
    mid_new = mido.MidiFile()
    for midi_property in ["type", "charset", "clip", "debug", "ticks_per_beat"]:
        setattr(mid_new, midi_property, getattr(ref_midi, midi_property))

    mid_new.tracks.append(track)
    return mid_new

def track_split(track: mido.MidiTrack, segment_length, add_end_of_track=True):
    current_time = 0
    current_segment = mido.MidiTrack()

    # Iterate over each message in the track
    for msg in track:

        # Check if we have reached the end of the current segment
        if current_time >= segment_length:
            # Add the end of track message to the current segment
            if add_end_of_track:
                current_segment.append(mido.MetaMessage('end_of_track'))
            yield current_segment

            # Reset the current segment and update the counters
            current_time = 0
            current_segment = mido.MidiTrack()

        # Add the current message to the current segment
        current_segment.append(msg)
        current_time += msg.time

    # Add the end of track message to the last segment
    if add_end_of_track:
        current_segment.append(mido.MetaMessage('end_of_track'))

    yield current_segment

def crop(path):
    rmtree(FOLDER, ignore_errors=True)
    FOLDER.mkdir(exist_ok=True, parents=True)
    # load the MIDI file
    mid = mido.MidiFile(path)

    # Calculate the length of each segment based on 1 second
    ticks_per_beat = mid.ticks_per_beat
    segment_length = ticks_per_second = mido.second2tick(1, ticks_per_beat, mido.bpm2tempo(temp(path)))

    # Iterate over each track in the MIDI file
    for track_idx, track in enumerate(mid.tracks):
        for segment_idx, segment in enumerate(track_split(track, segment_length)):
            create_midi_part(segment, mid).save(FOLDER / f'track_{track_idx}_segment_{segment_idx}.mid')

if __name__ == '__main__':
    crop("../resources/midi/rush E.mid")
