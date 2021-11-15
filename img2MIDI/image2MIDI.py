import cv2
from PIL import Image
import numpy as np
import pretty_midi
import sys

# Python program to find 3 elements such
# that max(abs(A[i]-B[j]), abs(B[j]- C[k]),
# abs(C[k]-A[i])) is minimized.
import sys


def findCloset(A, B, C):
    A = A.tolist()
    B = B.tolist()
    C = C.tolist()
    p = len(A)
    q = len(B)
    r = len(C)
    # Initialize min diff
    diff = sys.maxsize
    res_i = 0
    res_j = 0
    res_k = 0
    # Traverse Array
    i = 0
    j = 0
    k = 0
    while(i < p and j < q and k < r):
        # Find minimum and maximum of
        # current three elements
        minimum = min(A[i], min(B[j], C[k]))
        maximum = max(A[i], max(B[j], C[k]))
        # Update result if current diff is
        # less than the min diff so far
        if maximum-minimum < diff:
            res_i = i
            res_j = j
            res_k = k
            diff = maximum - minimum
        # We can 't get less than 0 as
        # values are absolute
        if diff == 0:
            break
        # Increment index of array with
        # smallest value
        if A[i] == minimum:
            i = i+1
        elif B[j] == minimum:
            j = j+1
        else:
            k = k+1
        # Print result
    print(A[res_i], ' ', B[res_j], ' ', C[res_k])
    return [A[res_i],  B[res_j], C[res_k]]


def image2MIDI(image_path, instrument, interval):
    interval = float(interval)
    c_chord = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a specified instrument
    # TODO: Implement Instrument Name Category
    program = pretty_midi.instrument_name_to_program(instrument)
    instr = pretty_midi.Instrument(program=program)

    img = np.array(Image.open(image_path))  # RGB Matrix
    img = cv2.resize(img, (106, 100))
    img = np.dot(img, [0.33, 0.33, 0.33])

    i = 0
    for piano_row in img.T:
        unique_array = np.unique(piano_row, return_counts=True)
        value_unique_array = unique_array[0]
        count_unique_array = unique_array[1]
        temp = np.sort(count_unique_array)
        # Get the three most frequent and pixel-max pixel value
        max_freq_pixel = max(value_unique_array[np.where(
            count_unique_array == temp[-1])])
        snd_freq_pixel = max(value_unique_array[np.where(
            count_unique_array == temp[-2])])
        trd_freq_pixel = max(value_unique_array[np.where(
            count_unique_array == temp[-3])])
        print('pixel: ', max_freq_pixel, snd_freq_pixel, trd_freq_pixel)
        max_freq_index = np.where(
            piano_row == max_freq_pixel)
        snd_freq_index = np.where(
            piano_row == snd_freq_pixel)
        trd_freq_index = np.where(
            piano_row == trd_freq_pixel)
        print('index: ', max_freq_index,
              snd_freq_index, trd_freq_index)
        most_freq_closet_index = findCloset(
            max_freq_index[0], snd_freq_index[0], trd_freq_index[0])
        # TODO: chord mapping
    # Iterate over note names, which will be converted to note number later
    # Example: C Major
    # C D E F G A B C
    # 1 2 3 4 5 6 7 1
    # 72 74 76 77 79 81 83 85
    # C = ['C5', 'E5', 'G5']  # 1 3 5
    # Dm = ['D5', 'F5', 'A5']  # 2 4 6
    # D = ['D5', 'F5#', 'A5']  # 2 4 6
    # Em = ['E5', 'G5', 'B5']  # 3 5 7
    # F = ['F5', 'A5', 'C5']  # 4 6 1
    # G = ['G5', 'B5', 'D5']  # 5 7 2
    # Am = ['A5', 'C5', 'E5']  # 6 1 3
    # Bm = ['B5', 'D5', 'F5']  # 7 2 4
    # TODO: Implement chord database
    # chord_progress = [C, Am, F, G]  # Sample: 1645
        for note_name in most_freq_closet_index:
            note_number = note_name + 21
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
interval = sys.argv[3]

image2MIDI(image_path, instrument, interval)
