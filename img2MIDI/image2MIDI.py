import cv2
from PIL import Image
import numpy as np
import pretty_midi
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
    # print(A[res_i], ' ', B[res_j], ' ', C[res_k])
    return [A[res_i],  B[res_j], C[res_k]]


def threeChordMapping(note_list):
    if len(note_list) != 3:
        return
    # Find two nearest element index (only support three elements)
    # Default: 0 1 2 / 1 2 0
    one = 0
    two = 1
    three = 2
    diff = abs(note_list[1] - note_list[0])
    if(abs(note_list[2] - note_list[0]) < diff):
        # 0 2 1 / 2 0 1
        two = 2
        three = 1
        diff = abs(note_list[2] - note_list[0])
    if(abs(note_list[2] - note_list[1]) < diff):
        # 1 2 0 / 2 1 0
        one = 1
        two = 2
        three = 0
        diff = abs(note_list[2] - note_list[1])

    # print('origin: ', note_list)
    # print('two nearest: ', note_list[one], note_list[two])
    while(diff > 12):  # If the minimal diff is still > 12, set note to same range
        if(note_list[one] > note_list[two]):
            note_list[two] = note_list[two] + 12
        else:
            note_list[one] = note_list[one] + 12
        diff = abs(note_list[one] - note_list[two])

    # Now, find the farest to the farest element
    n = one
    if(abs(note_list[two] - note_list[three]) > abs(note_list[one] - note_list[three])):
        n = two
    diff = abs(note_list[three] - note_list[n])
    while(diff > 12):
        if(note_list[three] > note_list[n]):
            note_list[three] = note_list[three] - 12
        else:
            note_list[three] = note_list[three] + 12
        diff = abs(note_list[three] - note_list[n])
    # Now, three notes should be in the same range
    # Set: (0, +3, +6), (0, +3, +7), (0, +3, +9), (0, +4, +7), (0, +4, +9), (0, +5, +9)
    chord_set = [[3, 6], [3, 7], [3, 9], [4, 7], [4, 9], [5, 9]]
    new_note_list = [note_list[one], note_list[two], note_list[three]]
    new_note_list.sort()
    # print(new_note_list)
    # Default
    snd_expect_value = new_note_list[0] + 3
    trd_expect_value = new_note_list[0] + 6
    diff = (new_note_list[1] - snd_expect_value)**2
    +(new_note_list[2] - trd_expect_value)**2
    res = [3, 6]
    # Euclidean Distance: Find the most likely chord
    for chord_offset in chord_set:
        snd_expect_value = new_note_list[0] + chord_offset[0]
        trd_expect_value = new_note_list[0] + chord_offset[1]
        temp = (new_note_list[1] - snd_expect_value)**2
        +(new_note_list[2] - trd_expect_value)**2
        if temp < diff:
            res = chord_offset
    new_note_list[1] = new_note_list[0] + res[0]
    new_note_list[2] = new_note_list[0] + res[1]
    print(new_note_list)
    return new_note_list


def image2MIDI(image_path, instrument, interval):
    interval = float(interval)
    c_chord = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a specified instrument
    # TODO: Implement Instrument Name Category
    program = pretty_midi.instrument_name_to_program(instrument)
    instr = pretty_midi.Instrument(program=program)

    img = np.array(Image.open(image_path))  # RGB Matrix
    img = cv2.resize(img, (88, 100))
    img = np.dot(img, [0.33, 0.33, 0.33])  # TODO: improvement on colors

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
        # print('pixel: ', max_freq_pixel, snd_freq_pixel, trd_freq_pixel)
        max_freq_index = np.where(
            piano_row == max_freq_pixel)
        snd_freq_index = np.where(
            piano_row == snd_freq_pixel)
        trd_freq_index = np.where(
            piano_row == trd_freq_pixel)
        # print('index: ', max_freq_index, snd_freq_index, trd_freq_index)
        most_freq_closet_index = findCloset(
            max_freq_index[0], snd_freq_index[0], trd_freq_index[0])
        three_chord_index = threeChordMapping(most_freq_closet_index)
        # TODO: chord mapping
    # Iterate over note names, which will be converted to note number later
    # Example: C Major
    # C D E F G A B C
    # 1 2 3 4 5 6 7 1
    # 72 74 76 77 79 81 83 85
    # C = ['C5', 'E5', 'G5']  # 1 3 5 (72 76 79) (0, +3, +6)
    # Dm = ['D5', 'F5', 'A5']  # 2 4 6 (74 77 81) (0, +3, +7)
    # D = ['D5', 'F5#', 'A5']  # 2 4 6 (74 78 81) (0, +4, +7)
    # Em = ['E5', 'G5', 'B5']  # 3 5 7 (76 79 83) (0, +3, +7)
    # F = ['F5', 'A5', 'C5']  # 4 6 1 (77 81 72) (0, +5, +9)
    # G = ['G5', 'B5', 'D5']  # 5 7 2 (79, 83, 74) (0, +5, +9)
    # Am = ['A5', 'C5', 'E5']  # 6 1 3 (81 72 76) (0, +4, +9)
    # Bm = ['B5', 'D5', 'F5']  # 7 2 4 (83 74 77) (0, +3, +9)
    # Set: (0, +3, +6), (0, +3, +7), (0, +3, +9), (0, +4, +7), (0, +4, +9), (0, +5, +9)
    # TODO: Implement chord database
    # chord_progress = [C, Am, F, G]  # Sample: 1645
        for note_name in three_chord_index:
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
