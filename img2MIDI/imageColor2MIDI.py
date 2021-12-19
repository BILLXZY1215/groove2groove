import cv2
from PIL import Image
import numpy as np
import pretty_midi
import sys
import webcolors

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


def imageColor2MIDI(image_path, interval):
    interval = float(interval)
    img = Image.open(image_path)  # RGB Matrix
    # img = img.resize((88, 100))
    if img.mode == 'RGB':
        pixels = list(img.convert('RGB').getdata())
        for r, g, b in pixels:  # just ignore the alpha channel
            rgb = (r, g, b)
            print(rgb)
    else:
        print('Unimplemented image type')


image_path = sys.argv[1]
interval = sys.argv[2]

imageColor2MIDI(image_path, interval)
