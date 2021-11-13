import cv2
from PIL import Image
import numpy as np
import pretty_midi
import sys


def image2MIDI(image_path, instrument):

    img = np.array(Image.open(image_path))  # RGB Matrix
    img = cv2.resize(img, (106, 100))
    img = np.dot(img, [0.33, 0.33, 0.33])
    # for piano_row in img.T:
    # TODO: index of chosen note

    # Create a PrettyMIDI object
    c_chord = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a specified instrument
    # TODO: Implement Instrument Name Category
    program = pretty_midi.instrument_name_to_program(instrument)
    instr = pretty_midi.Instrument(program=program)
    # Iterate over note names, which will be converted to note number later
    # Example: C Major
    # C D E F G A B C
    # 1 2 3 4 5 6 7 1
    C = ['C5', 'E5', 'G5']  # 1 3 5
    Dm = ['D5', 'F5', 'A5']  # 2 4 6
    Em = ['E5', 'G5', 'B5']  # 3 5 7
    F = ['F5', 'A5', 'C5']  # 4 6 1
    G = ['G5', 'B5', 'D5']  # 5 7 2
    Am = ['A5', 'C5', 'E5']  # 6 1 3
    Bm = ['B5', 'D5', 'F5']  # 7 2 4
    # TODO: Implement chord database
    chord_progress = [C, Am, F, G]  # Sample: 1645
    interval = 2
    i = 0
    for chord in chord_progress:
        for note_name in chord:
            note_number = pretty_midi.note_name_to_number(note_name)
            # print(note_number)
            note = pretty_midi.Note(
                velocity=100, pitch=note_number, start=0+interval*i, end=interval*(i+1))
            instr.notes.append(note)
        i = i + 1

    # Add the instr instrument to the PrettyMIDI object
    c_chord.instruments.append(instr)
    # Write out the MIDI data
    c_chord.write('{}-C-chord.mid'.format(instrument))


image_path = sys.argv[1]
instrument = sys.argv[2]

image2MIDI(image_path, instrument)
