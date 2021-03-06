from __future__ import division, print_function, absolute_import

import numpy as np
from random import shuffle
from math import ceil
import pickle
import subprocess

from .helpers import loadAudio
from .conf import conf
from config import ROOT_DIR


library = dict()

# Shuffle to arrays in unison
def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def loadData():

    # reload audio object from file
    try:
        audio_file = open(ROOT_DIR + r'/resources/audio.pkl', 'rb')
        audio_matrix, classifications = pickle.load(audio_file)
        audio_file.close()
        return unison_shuffled_copies(audio_matrix, classifications)
    except:
        # If no pickle file
        pass

    if conf["downSample"]:
        subprocess.call(ROOT_DIR + "/bin/downsample.sh", shell=True)

    for c in conf["classes"]:
        print(c)
        library[c] = loadAudio(c)

    # All tracks in a matrix
    audio_matrix = np.zeros((0, conf["buff_size"], conf["num_buffs"], 4))

    # Each track classified
    classifications = np.zeros((0, len(library)))

    # kind : ie kick, snare, etc
    # samples_list : tracks
    for i, (kind, samples_list) in enumerate(library.items()):
        # if (conf["randomize"]):
            # Randomize list of audio
            # shuffle(samples_list)

        # Set binary classifications for this kind
        class_row = np.zeros((len(samples_list), len(library)))
        ones = np.ones((len(samples_list), 1))
        class_row[:, i:i + 1] = ones
        classifications = np.vstack((classifications, class_row))

        # append each track to the audio matrix
        for j, track in enumerate(samples_list):
            print("loading: ", kind, " track: ", j + 1, "/", len(samples_list))

            # dft = buf_size x num_buffs x channel x complex
            dft = track.signalDFT()
            dft = dft.reshape((1, dft.shape[0], dft.shape[1], 4))
            audio_matrix = np.vstack((audio_matrix, dft))

    file = open(ROOT_DIR + r'/resources/audio.pkl', 'wb')
    pickle.dump((audio_matrix, classifications), file)
    file.close()

    print("done loading")

    # Randomize Audio
    return unison_shuffled_copies(audio_matrix, classifications)
