import os
import re
import mido
from CropToSeconds import crop
from DeleteFolderContents import delete


FOLDER = "opt-merged/"


def merge(path):
    delete(FOLDER)
    crop(path)
    # load the MIDI file
    mid = mido.MidiFile(path)

    # set the directory where the segment files are located
    dir_path = 'opt-cropped/'

    # find all the segment files in the directory
    files = os.listdir(dir_path)
    segment_files = [f for f in files if 'segment' in f]

    # group the segment files by their index number
    segments_by_index = {}
    for file in segment_files:
        # extract the segment index using a regular expression
        match = re.search(r'segment_(\d+)\.mid', file)
        if match:
            index = int(match.group(1))
            if index in segments_by_index:
                segments_by_index[index].append(file)
            else:
                segments_by_index[index] = [file]

    # iterate over each segment index
    for index in segments_by_index.keys():
        # create a new MIDI file for the merged segments
        merged_mid = mido.MidiFile()
        # iterate over each track and add the corresponding segment to the merged MIDI file
        for track_idx in range(len(mid.tracks)):
            track_segment_file = f'track_{track_idx}_segment_{index}.mid'
            if track_segment_file in segments_by_index[index]:
                track_segment = mido.MidiFile(os.path.join(dir_path, track_segment_file))
                for track in track_segment.tracks:
                    merged_mid.tracks.append(track)
        # save the merged MIDI file
        merged_mid.save(f'{FOLDER}segment_{index}.mid')


merge("../resources/midi/rush E.mid")
