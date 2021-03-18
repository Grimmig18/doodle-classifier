import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

from data_loader import DataLoader as DL
import numpy as np

dl = DL()
# data = dl.load_data_from_file(dl.PIZZA)
data, labels = dl.load_data_batches()
data_1d = np.array([dl.one_dimensional_array_from_matrix(mat) for mat in data])

print(len(data))
print(len(labels))
