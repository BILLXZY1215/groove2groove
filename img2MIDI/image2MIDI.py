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
for note_name in ['C5', 'E5', 'G5']:
    # Retrieve the MIDI note number for this note name
    note_number = pretty_midi.note_name_to_number(note_name)
    # Create a Note instance, starting at 0s and ending at .5s
    print(note_number)
    note = pretty_midi.Note(
        velocity=100, pitch=note_number, start=0, end=2)
    # Add it to our cello instrument
    cello.notes.append(note)
# Add the cello instrument to the PrettyMIDI object
cello_c_chord.instruments.append(cello)
# Write out the MIDI data
cello_c_chord.write('cello-C-chord.mid')
