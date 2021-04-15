# Setup
import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append('e:\\Projekte\\2021\\ML\\doodle-classifier')
sys.path.append(root_dir)
# print(os.getcwd())

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

from src.data_loader import DataLoader as DL
from src.coach import train_in_batches


dl = DL()
clf_batches = MLPClassifier(hidden_layer_sizes=(128,))
for i in range(3):
    data, labels = dl.get_next_training_set(100)
    clf_batches.partial_fit(data, labels, np.unique(labels))


# import os
# import sys
# root_dir = os.path.join(os.getcwd(), '..')
# sys.path.append(root_dir)
# import numpy as np
# import png

# from PIL import Image, ImageDraw

# img = [[[203,193,177,143,104,66,34,17,12,14,30,53,75,100,125,152,177,204,228,245,255,258,259,258,251,239,228,211,199,190,180,171,163,163],[51,45,45,52,74,106,148,192,233,264,288,305,313,315,315,303,278,244,207,174,143,117,92,75,61,48,40,35,33,33,33,34,42,42],[0,27,45,58,78,94,111,127,143,161,177,194,210,228,244,261,277,294,310,328,344,361,380,397,413,429,449,463,481,496,512,529,546,566]],[[139,137,137,134,126,116,109,109,111,118,121,123,124,123],[56,61,73,97,133,179,226,266,292,312,325,334,340,338],[965,994,1011,1027,1043,1061,1081,1098,1115,1130,1148,1166,1194,1232]],[[21,23,31,45,67,95,128,161,191,220,252,273,294,306,306],[199,206,210,212,212,204,190,179,173,167,157,151,146,144,144],[1399,1443,1462,1477,1494,1510,1527,1543,1561,1580,1599,1614,1628,1642,1663]],[[216,205,188,158,125,96,75,63,58,56,55,55,55,56],[60,71,93,128,175,222,266,299,320,337,348,357,364,363],[2049,2093,2110,2126,2143,2162,2177,2195,2220,2230,2247,2261,2277,2362]],[[53,60,69,85,108,134,162,188,207,223,234,243,243],[136,143,151,163,179,195,212,227,238,250,259,268,268],[2535,2561,2577,2594,2611,2630,2644,2660,2676,2699,2715,2731,2749]]]

# max = 0
# for stroke in img:
#     print(stroke)
#     for i in range(len(stroke[0])):
#         print(stroke[0][i], stroke[1][i])
#         if stroke[0][i] > max:
#             max = stroke[0][i]
#         if stroke[1][i] > max:
#             max = stroke[1][i]

# print(max)

# mat = np.full((max, max), 1)

# for stroke in img:
#     for i in range(len(stroke[0])):
#         mat[stroke[0][i] - 1, stroke[1][i] - 1] = 0

# mat = [[int(c) for c in row] for row in mat]
# w = png.Writer(len(mat[0]), len(mat), greyscale=True, bitdepth=1)
# f = open("tst" + '.png', 'wb')
# w.write(f, mat)
# f.close()



# image = Image.new("RGB", (max, max), color=(255,255,255))
# image_draw = ImageDraw.Draw(image)

# for stroke in img:
#     stroke_tup = [(stroke[0][i], stroke[1][i]) for i in range(len(stroke[0]))]
#     image_draw.line(stroke_tup, fill=(0,0,0), width=2)

# img_data = np.reshape(list(image.getdata()), (max, max, 3))


# mat = np.full((max, max), 1)

# for i, row in enumerate(img_data):
#     for j, val in enumerate(row):
#         if not np.array([v == 255 for v in val]).all():
#             mat[i,j] = 0

# mat = [[int(c) for c in row] for row in mat]
# w = png.Writer(len(mat[0]), len(mat), greyscale=True, bitdepth=1)
# f = open("lmao" + '.png', 'wb')
# w.write(f, mat)
# f.close()


# with open('./data/processed/pizza.ndjson', 'r') as f:
#     for i, line in enumerate(f):
#         print(i, ": ", line)
#         break