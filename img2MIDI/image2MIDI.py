import cv2
from PIL import Image
import numpy as np
import pretty_midi

# img = cv2.imread('Amily.jpeg')
# cv2.imshow('output', img)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()

img = np.array(Image.open('Amily.jpeg'))  # RGB Matrix
img = cv2.resize(img, (106, 100))
img = np.dot(img, [0.33, 0.33, 0.33])
print(img.shape)
# Create a PrettyMIDI object
cello_c_chord = pretty_midi.PrettyMIDI()
# Create an Instrument instance for a cello instrument
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)
# Iterate over note names, which will be converted to note number later
# C D E F G A B C
# 1 2 3 4 5 6 7 1
for note_name in ['C5', 'E5', 'G5']:  # C (1,3,5)
    note_number = pretty_midi.note_name_to_number(note_name)
    print(note_number)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=0, end=2)
    cello.notes.append(note)

for note_name in ['A5', 'C5', 'E5']:  # Am (6,1,3)
    note_number = pretty_midi.note_name_to_number(note_name)
    print(note_number)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=2, end=4)
    cello.notes.append(note)

for note_name in ['F5', 'A5', 'C5']:  # F (4,6,1)
    note_number = pretty_midi.note_name_to_number(note_name)
    print(note_number)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=4, end=6)
    cello.notes.append(note)

for note_name in ['G5', 'B5', 'D5']:  # G (5,7,2)
    note_number = pretty_midi.note_name_to_number(note_name)
    print(note_number)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=6, end=8)
    cello.notes.append(note)

# Add the cello instrument to the PrettyMIDI object
cello_c_chord.instruments.append(cello)
# Write out the MIDI data
cello_c_chord.write('cello-C-chord.mid')
