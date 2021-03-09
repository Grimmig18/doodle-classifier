import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

import json
import numpy as np
from src.dict_obj import DictObject as DO


class DataLoader:
    
    # Indexes of default tree image words
    HELICOPTER = 0
    OCTOPUS = 1
    PIZZA = 2

    # Dict structure keywords
    WORD = 'word'
    DRAWING = 'drawing'


    def __init__(self, files=['helicopter.ndjson', 'octopus.ndjson', 'pizza.ndjson'], path='../data/processed/', default_width=256, default_height=256):
        self.files = files
        self.path = path

        self.default_width = default_width
        self.default_height = default_height


    def load_data_from_file(self, file_index, lines=0):
        """
        Loads the JSON from one of the files from self.files by index.
        Returns data as dict object
        """
        with open(self.path + self.files[file_index], 'r') as f:
            return [eval(x) for i, x in enumerate(f) if i in lines]



    def matrix_from_image(self, points):
        """
        Returns a default_width * default_height matrix filled with 0s.
        The (x, y) tupels in the points array define black pixels.
        """

        mat = np.full((self.default_width, self.default_height), 0)
        for point in points:
            mat[point[0], point[1]] = 1

        return mat

    def one_dimensional_array_from_matrix(self, mat):
        """
        Transforms a n-dimensional matrix into an one dimensional array.
        """
        return np.reshape(mat, np.multiply(*mat.shape))

    
