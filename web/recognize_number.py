#!/usr/bin/env python2

import numpy as np
import Image

class Recognizer:
    def __init__(self):
        self.Theta1 = np.genfromtxt("perceptron/Theta1.txt")
        self.Theta2 = np.genfromtxt("perceptron/Theta2.txt")
    
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))     
    
    def to_float_array(self, a):
        a *= 2
        a /= 256.
        a -= 1
        return a
    
    def predict_number(self):
        img = Image.open("number.png")
        img_array = np.array(img).flatten()
        to_float_array_vect = np.vectorize(self.to_float_array)
        img_float = to_float_array_vect(img_array)
    
        pred = self.predict(img_float[np.newaxis])
        return pred.item()
    
    def predict(self, X):
        m = X.shape[0]
        num_labels = self.Theta2.shape[0]
            
        h1 = self.sigmoid(np.dot(np.concatenate((np.ones((m, 1)), X), 1),    self.Theta1.T))
        h2 = self.sigmoid(np.dot(np.concatenate((np.ones((m, 1)), h1), 1), self.Theta2.T))

        p = h2.argmax(axis=1)[np.newaxis].T
    
        return p

