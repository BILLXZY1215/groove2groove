import cv2
from PIL import Image
import numpy as np
import pretty_midi
import sys
import webcolors
import math
from collections import Counter

colormap = {
    # (R, G, B)
    # Resource:
    # https://www.color-name.com/
    # https://www.w3.org/wiki/CSS/Properties/color/keywords
    'C': (255, 0, 0),  # red
    'F': (130, 0, 0),  # dark red
    'G': (255, 165, 0),  # orange
    'D': (255, 255, 0),  # yellow
    'A': (0, 255, 0),  # green
    'E': (135, 206, 235),  # sky blue
    'B': (0, 0, 255),  # blue
    'F#': (24, 62, 250),  # bright blue
    'C#': (238, 130, 238),  # violet
    'G#': (200, 162, 200),  # lilac
    'D#': (210, 169, 161),  # flesh
    'A#': (255, 228, 225),  # mistyrose
}

C_Major = {
    'C': 72,  # C5
    'C#': 73,
    'D': 74,
    'D#': 75,
    'E': 76,
    'F': 77,
    'F#': 78,
    'G': 79,
    'G#': 80,
    'A': 81,
    'A#': 82,
    'B': 83,
}


def three_distance(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)


def findClosest(rgb):
    # rgb: (R, G, B)
    min_distance = sys.maxsize
    res = ''
    for note in colormap:
        delta_R = rgb[0] - colormap[note][0]
        delta_G = rgb[1] - colormap[note][1]
        delta_B = rgb[2] - colormap[note][2]
        dist = three_distance(delta_R, delta_G, delta_B)
        if (dist < min_distance):
            min_distance = dist
            res = note
    return res


def noteName2Value(note_name):
    return C_Major[note_name]


def imageColor2MIDI(image_path, interval):
    interval = float(interval)
    img = Image.open(image_path)  # RGB Matrix
    img = img.resize((64, 64))  # resize to a portable size
    if img.mode == 'RGB':
        img = list(img.convert('RGB').getdata())
        pixels = [(item, img.count(item)) for item in set(img)]
        # sort by frequency
        pixels = sorted(pixels, key=lambda x: x[1], reverse=True)
        notes = []
        for color, _ in pixels:
            rgb = (color[0], color[1], color[2])
            notes.append(noteName2Value(findClosest(rgb)))
        print(notes)
    else:
        print('Unimplemented image type')


image_path = sys.argv[1]
interval = sys.argv[2]

imageColor2MIDI(image_path, interval)
