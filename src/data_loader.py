import os
import sys

from sklearn.utils.extmath import randomized_range_finder
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

import numpy as np
import random
import string
import png
from PIL import Image

from src.preprocess_data import total_lines
class DataLoader:

    max_possible_lines = 0 
    current_training_set = {}
    last_index = 0
    
    # Indexes of default tree image words
    HELICOPTER = 0
    OCTOPUS = 1
    PIZZA = 2

    classes = []

    word_index = {
        "helicopter": HELICOPTER,
        "octopus": OCTOPUS,
        "pizza": PIZZA
    }

    number_index = {
        0: "helicopter",
        1: "octopus",
        2: "pizza"
    }

    line_index = {}

    # Dict structure keywords
    WORD = 'word'
    DRAWING = 'drawing'

    # Model save path
    model_save_path = '../model/clf_batches.sav'


    def __init__(self, files=['helicopter.ndjson', 'octopus.ndjson', 'pizza.ndjson'], path='../data/processed/', width=256, height=256):
        self.files = files
        self.path = path

        self.width = width
        self.height = height

        # self.set_max_line_count()



    def set_max_line_count(self):
        max_l = np.inf
        for file in self.files:
            with open(self.path + file, 'r') as f:
                for i, _ in enumerate(f):
                    pass
                if max_l > i:
                    max_l = i

        print("Set max_possible_lines to {}".format(max_l))
        self.max_possible_lines = max_l

    def get_classes(self):
        self.classes = [k for k in self.number_index]
        return self.classes

    def get_class_names(self):
        return [self.number_index[k] for k in self.number_index]


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
        # print(mat.shape)
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

    def load_image(self, path, is_array=True, is_hand_drawn=False):
        img = Image.open(path)
        arr = np.array(img)

        new_arr = np.full(arr.shape[:-1 if is_array else None], 1)

        for l in range(arr.shape[0]):
            for t in range(len(arr[l])):
                if is_array:
                    if np.array([True if v == 255 else False for v in arr[l,t]]).all():
                        new_arr[l,t] = 0
                else:
                    if arr[l,t] == True or (is_hand_drawn and arr[l,t] == 255):
                        new_arr[l,t] = 0

        
        return new_arr, self.one_dimensional_array_from_matrix(new_arr)

    def load_hand_drawn(self, path):
        img = Image.open(path)
        arr = np.array(img)

        new_arr = np.full(arr.shape[:], 1)

        for l in range(arr.shape[0]):
            for t in range(len(arr[l])):
                if arr[l,t] == 255:
                    new_arr[l,t] = 0

        return new_arr, self.one_dimensional_array_from_matrix(new_arr)

        


        

    def load_data_batches(self, batch_size=1000, skip=0, return_1d=False):
        """
        Returns an array of data (image data as a 256x256 matrix) and an array of corresponding labels.
        Structure is similar to the iris dataset
        """
        data = []
        labels = []

        data.extend(self.load_batch(word=self.HELICOPTER, batch_size=batch_size, start=skip))
        labels.extend([self.HELICOPTER for _ in range(batch_size)])

        data.extend(self.load_batch(word=self.OCTOPUS, batch_size=batch_size, start=skip))
        labels.extend([self.OCTOPUS for _ in range(batch_size)])

        data.extend(self.load_batch(word=self.PIZZA, batch_size=batch_size, start=skip))
        labels.extend([self.PIZZA for _ in range(batch_size)])

        data_1d = np.array([self.one_dimensional_array_from_matrix(mat) for mat in data])

        if return_1d:
            data = data_1d

        return data, labels


    def load_batch(self, word, batch_size=1000, start=0):
        """
        Load data from file and convert to image matrix
        """

        data = []

        with open(self.path + self.files[word], 'r') as f:
            # skip files
            counter = 0
            for i, l in enumerate(f):
                counter = counter + 1
                if counter - 1 < start:
                    continue
                elif start + batch_size == counter - 1:
                    break

                d = eval(l)
                data.append(self.matrix_from_image(self.drawing_array_to_tupels(d[self.DRAWING])))

        return data


    def load_image_matrix(self, word, number):
        data = self.load_data_from_file(self.word_index[word], number)
        drawing_mat = self.matrix_from_image(self.drawing_array_to_tupels(data[self.DRAWING]))

        return drawing_mat, self.word_index[data[self.WORD]], data[self.DRAWING]

    
    
    def load_random_test_data(self, sample_size=500, return_1d=False):
        data = []
        labels = []

        for file in self.files:

            self.line_index, line_no = total_lines(self.line_index, file, path='../data/processed/')


            random_list = random.sample(range(0, line_no), sample_size)
            label = self.word_index[file.split(".")[0]]

            counter = 0
            with open('../data/processed/' + file, 'r') as f:

                for i, l in enumerate(f):
                    if i in random_list:
                        d = eval(l)
                        data.append(self.matrix_from_image(self.drawing_array_to_tupels(d[self.DRAWING])))
                        labels.append(label)

        data_1d = np.array([self.one_dimensional_array_from_matrix(mat) for mat in data])

        if return_1d:
            data = data_1d

        return data, labels

    def get_next_training_set(self, batch_size=1000):
        self.load_next(batch_size)
        return self.current_training_set['data'], self.current_training_set['labels']
         


    def load_next(self, increase, return_1d=True):
        self.current_training_set = {}
        col_data = []
        col_labels = []
        shape = ()
        counter = 0
        # Load next data batch
        for file in self.files:
            label = self.word_index[file.split(".")[0]]

            with open('../data/processed/' + file, 'r') as f:
                for i, l in enumerate(f):
                    if i < self.last_index:
                        continue
                    if i >= self.last_index + increase:
                        self.last_index = i
                        break

                    counter = counter + 1
                    
                    t = self.matrix_from_image(self.drawing_array_to_tupels(eval(l)[self.DRAWING]))
                    shape = t.shape
                    col_data = np.append(col_data, t)
                    col_labels.append(label)

                    # self.current_training_set = np.append(self.current_training_set, [t, label], axis=1)
                    # self.current_training_set[0] = np.append(self.current_training_set[0], self.matrix_from_image(self.drawing_array_to_tupels(t[self.DRAWING])))
                    # self.current_training_set[0].append()
                    # self.current_training_set[1] = np.append(self.current_training_set[1], label)

        # Reshape col_data list
        col_data = np.reshape(col_data, (counter, *shape))
        
        self.current_training_set['labels'] = col_labels

        if return_1d:
            data_1d = np.array([self.one_dimensional_array_from_matrix(mat) for mat in col_data])
            col_data = data_1d

        self.current_training_set['data'] = col_data

    

    def strokes_from_matrix(self, mat):

        # for l in range(arr.shape[0]):
        #     for t in range(len(arr[l])):
        #         if np.array([True if v == 255 else False for v in arr[l,t]]).all():
        #             new_arr[l,t] = 1
        print(mat)
        stroke = [[], []]
        for i, row in enumerate(mat):
            for j, elem in enumerate(row):
                if elem == 0:
                    stroke[0].append(i)
                    stroke[1].append(j)

        return stroke






            

    
