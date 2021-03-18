import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

import json
import numpy as np
import random
import string
import png
class DataLoader:
    
    # Indexes of default tree image words
    HELICOPTER = 0
    OCTOPUS = 1
    PIZZA = 2

    word_index = {
        "helicopter": HELICOPTER,
        "octopus": OCTOPUS,
        "pizza": PIZZA
    }

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
        tupels.extend([(drawing[0][j], drawing[1][j]) for j in range(len(drawing[0]))])

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

    def save_image(self, image_data, name='random'):
        if name == 'random':
            name = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))

        data_tupels = self.drawing_array_to_tupels(image_data)
        image = np.full((self.width, self.height), 1)

        for t in data_tupels:
            image[t[0], t[1]] = 0
            
        image = [[int(c) for c in row] for row in image]

        w = png.Writer(len(image[0]), len(image), greyscale=True, bitdepth=1)
        f = open(name + '.png', 'wb')
        w.write(f, image)
        f.close()


    def load_data_batches(self, batch_size=1000):
        """
        Returns an array of data (image data as a 256x256 matrix) and an array of corresponding labels.
        Structure is similar to the iris dataset
        """
        data = []
        labels = []

        data.extend(self.load_batch(word=self.HELICOPTER, batch_size=batch_size))
        labels.extend([self.HELICOPTER for _ in range(batch_size)])

        data.extend(self.load_batch(word=self.OCTOPUS, batch_size=batch_size))
        labels.extend([self.OCTOPUS for _ in range(batch_size)])

        data.extend(self.load_batch(word=self.PIZZA, batch_size=batch_size))
        labels.extend([self.PIZZA for _ in range(batch_size)])

        return data, labels


    def load_batch(self, word, batch_size=1000, start=0):
        """
        Load data from file and convert to image matrix
        """

        data = []

        with open(self.path + self.files[word], 'r') as f:
            # skip files
            counter = 0
            for l in f:
                counter = counter + 1
                if counter - 1 < start:
                    continue
                elif start + batch_size == counter - 1:
                    break

                d = eval(l)
                data.append(self.matrix_from_image(self.drawing_array_to_tupels(d[self.DRAWING])))

        return data


    def load_image_matrix(self, word, number):
        data = self.load_data_from_file(word, number)
        drawing_mat = self.matrix_from_image(self.drawing_array_to_tupels(data[self.DRAWING]))

        return drawing_mat, self.word_index[data[self.WORD]]

    
