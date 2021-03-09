import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

import json
import numpy as np
class DataLoader:
    
    # Indexes of default tree image words
    HELICOPTER = 0
    OCTOPUS = 1
    PIZZA = 2

    # Dict structure keywords
    WORD = 'word'
    DRAWING = 'drawing'


    def __init__(self, files=['helicopter.ndjson', 'octopus.ndjson', 'pizza.ndjson'], path='../data/processed/', width=256, height=256):
        self.files = files
        self.path = path

        self.width = width
        self.height = height


    def load_data_from_file(self, file_index, line=0):
        """
        Loads the JSON from one of the files from self.files by index.
        Returns data as dict object
        """
        with open(self.path + self.files[file_index], 'r') as f:
            counter = 0
            for l in f:
                if counter == line:
                    return eval(l)
                counter = counter + 1


    def drawing_array_to_tupels(self, drawing):
        tupels = []
        for i in range(len(drawing)):
            tupels.extend([(drawing[i][0][j], drawing[i][1][j]) for j in range(len(drawing[i][0]))])

        return tupels


    def matrix_from_image(self, points):
        """
        Returns a width * height matrix filled with 0s.
        The (x, y) tupels in the points array define black pixels.
        """

        mat = np.full((self.width, self.height), 0)
        for point in points:
            mat[point[0], point[1]] = 1

        return mat

    def one_dimensional_array_from_matrix(self, mat):
        """
        Transforms a n-dimensional matrix into an one dimensional array.
        """
        return np.reshape(mat, np.multiply(*mat.shape))

    
