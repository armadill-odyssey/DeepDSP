from DSP import Signal
import numpy as np
import os
from config import ROOT_DIR


"""Load all the .wav files in a given directory, return list of type Signal"""
def loadAudio(dir):
    tracks = []

    for fn in os.listdir(ROOT_DIR + '/resources/audio/' + dir):
        # Double check we are loading a wav file
        if not fn.lower().endswith(('.wav')):
            continue

        filepath = os.path.join(ROOT_DIR, 'resources/audio/', dir, fn)
        tracks.append(Signal(filepath))

    return tracks