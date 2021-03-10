from qd import QuickDrawing
import json
import numpy as np
import png

def count_items(a):
    unique, counts = np.unique(a, return_counts=True)
    print(dict(zip(unique, counts)))

img = {}
counter = 1
with open('./data/raw/pizza.ndjson', 'r') as f:
    for l in f:
        js = json.loads(l)
        js['image'] = js['drawing']
        img = QuickDrawing('example', js)
        
        if counter == 6:
            break
        
        counter = counter + 1

# img.image.show('test')

img_data = list(img.image.getdata())
count_items(img_data)
img_data_2 = list(img.get_image().getdata())
img.image.show()
# print(len(img_data))


for i in range(len(img_data)):
    if img_data[i] != img_data_2[i]:
        print(img_data, img_data_2)

dim = int(np.sqrt(len(img_data)))
mat = np.reshape([1 if i == (255,255,255) else 0 for i in img_data], (dim, dim))
# print(mat)

mat = [[int(c) for c in row] for row in mat]

w = png.Writer(len(mat[0]), len(mat), greyscale=True, bitdepth=1)
f = open('pizza_test.png', 'wb')
w.write(f, mat)
f.close()

# img.image_data