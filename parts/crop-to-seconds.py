import mido

# load the MIDI file
mid = mido.MidiFile('../resources/midi/rush E.mid')

# Define the length of each segment (in ticks)
segment_length = mid.ticks_per_beat * 4  # 4 beats per segment

# Iterate over each track in the MIDI file
for track_idx, track in enumerate(mid.tracks):
    current_time = 0
    segment_idx = 0
    current_segment = mido.MidiTrack()

    # Iterate over each message in the track
    for msg in track:
        current_time += msg.time

        # Check if we have reached the end of the current segment
        if current_time >= segment_length:
            # Add the end of track message to the current segment
            current_segment.append(mido.MetaMessage('end_of_track'))

            # Save the current segment as a new MIDI file
            mid_new = mido.MidiFile()
            mid_new.tracks.append(current_segment)
            mid_new.save(f'opt-cropped/track_{track_idx}_segment_{segment_idx}.mid')

            # Reset the current segment and update the counters
            current_time = 0
            segment_idx += 1
            current_segment = mido.MidiTrack()

        # Add the current message to the current segment
        current_segment.append(msg)

    # Add the end of track message to the last segment
    current_segment.append(mido.MetaMessage('end_of_track'))

    # Save the last segment as a new MIDI file
    mid_new = mido.MidiFile()
    mid_new.tracks.append(current_segment)
    mid_new.save(f'opt-cropped/track_{track_idx}_segment_{segment_idx}.mid')