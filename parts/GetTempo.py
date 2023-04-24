import mido


def temp(path):
    mid = mido.MidiFile(path)

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = mido.tempo2bpm(msg.tempo)
                print(f'Tempo: {tempo} BPM')
                return tempo
