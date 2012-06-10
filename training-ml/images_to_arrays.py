#!/usr/bin/env python

import Image
import numpy as np
import os

def to_float_array(a):
    a *= 2
    a /= 256.
    a -= 1
    return a

files = os.listdir("training/")
files.sort()

os.chdir("training")

# 20x20 images
X = np.zeros((len(files), 400))
i = 0

to_float_array_vect = np.vectorize(to_float_array)

for file in files:
    img = Image.open(file)
    X[i] = to_float_array_vect(np.array(img).flatten())
    i += 1

np.savetxt("training_X.txt", X)