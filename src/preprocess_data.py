import json
import ndjson
import numpy as np
from scipy.spatial.distance import pdist
import math
from quickdraw import QuickDrawing

f_name = "pizza.ndjson"



# Create dict for processed data
rec = []

# Get total number of lines
total = 0
with open('./data/raw/' + f_name, 'r', encoding='utf-8') as f:
    total = sum(1 for l in f)

sm = 1 / total * 100

# Read raw data
with open('./data/raw/' + f_name, 'r', encoding='utf-8') as raws:
    counter = 1 
    for raw in raws:
        raw_json = json.loads(raw)
        
        if raw_json['recognized'] == True:
            
            new_r = {
                'word': raw_json['word'],
                'drawing': []
            }

            raw_json['image'] = raw_json['drawing']
            img = QuickDrawing('example', raw_json)

            img_data = list(img.image.getdata())

            dim = int(np.sqrt(len(img_data)))
            mat = np.reshape([1 if i == (255,255,255) else 0 for i in img_data], (dim, dim))

            stroke = [[], []]

            # Convert to stroke
            for x in range(len(mat)):
                for y in range(len(mat[x])):
                    if mat[x][y] == 0:
                        stroke[0].append(x)
                        stroke[1].append(y)

            if len(stroke[0]) == 0:
                print("Hello")
                
                for t in img_data:
                    if t != (255,255,255):
                        print(t)

            new_r['drawing'] = stroke
            rec.append(new_r)

            percentage = (counter / total) * 100
            
            if percentage % 0.1 < sm:
                print(round(percentage, 2), '%')

                # Save batch
                with open('./data/processed/' + f_name, 'a+', encoding='utf-8') as f:
                    for r in rec:
                        f.write(str(r)+ '\n')

                # Reset record
                rec = []   

        counter = counter + 1

        # Save remaining
    with open('./data/processed/' + f_name, 'a+', encoding='utf-8') as f:
        for r in rec:
            f.write(str(r)+ '\n')
            



# def find_local_max_in_drawing(drawing): 
#     max = 0
#     for stroke in drawing:
#         for point in range(len(stroke[0])):
#             if stroke[0][point] > max:
#                 max = stroke[0][point]
#             if stroke[1][point] > max:
#                 max = stroke[1][point] 
#     return max

# ): 
#     max = 0
#     for stroke in drawing:
#         for point in range(len(stroke[0])):
#             if stroke[0][point] > max:
#                 max = stroke[0][point]
#             if stroke[1][point] > max:
#                 max = stroke[1][point] 
#     return max

# def fill_stroke(stroke):
#     new_x = []
#     new_y = []

#     for i in range(len(stroke[0]) - 1):
#         # X
#         cur_x = stroke[0][i]
#         nex_x = stroke[0][i+1]

#         cur_y = stroke[1][i]
#         nex_y = stroke[1][i+1]

#         diff_x = nex_x - cur_x
#         diff_y = nex_y - cur_y

#         # int(round(cdist([[cur_x], [cur_y]], [[nex_x], [nex_y]], metric='cityblock')))
#         distance = (pdist([[cur_x, cur_y], [nex_x, nex_y]], metric='euclidean')[0])
#         # print(distance)

#         y_step_size = 1 / 255
#         if diff_x != 0:
#             y_step_size = diff_y / distance

#         x_step_size = 1 / 255
#         if diff_y != 0:
#             x_step_size = diff_x / distance
        
#         # new_stroke.append((cur_x, cur_y))
#         new_x.append(cur_x)
#         new_y.append(cur_y)

#         # counter = 1
#         for j in range(1, int(round(distance))):
#             _x = int(round(cur_x + j*x_step_size))
#             _y = int(round(cur_y + j*y_step_size))
            
#             if _x > 255 or _x < 0 or _y > 255 or _y < 0:
#                 break

#             new_x.append(_x)
#             new_y.append(_y)

#         new_x.append(stroke[0][-1])
#         new_y.append(stroke[1][-1])

#     return [new_x, new_y]

    # counter = 1

    # for raw in raws:
    #     raw_json = json.loads(raw)
        
    #     if raw_json['recognized'] == True:
    #         # Extract only the information we care about
    #         new_r = {
    #             'word': raw_json['word'],
    #             'drawing': raw_json['drawing']
    #         }
            

    #         # Find highest Value
    #         new_d = []

    #         # Scale strokes
    #         for stroke in raw_json['drawing']:
    #             stroke[0] = [int(x) for x in np.rint(np.interp(stroke[0], (min(stroke[0]), max(stroke[0])), (0, 255))).tolist()]
    #             stroke[1] = [int(x) for x in np.rint(np.interp(stroke[1], (min(stroke[1]), max(stroke[1])), (0, 255))).tolist()]

    #             new_d.append(fill_stroke(stroke))
            
    #         new_r['drawing'] = new_d
    #         rec.append(new_r)
        
        
    #     percentage = (counter / total) * 100
    #     if percentage % 1 < sm:
    #         print(round(percentage, 2), '%')

    #         # Save batch
    #         with open('./data/processed/' + f_name, 'a+', encoding='utf-8') as f:
    #             for r in rec:
    #                 f.write(str(r)+ '\n')

    #         # Reset record
    #         rec = []
    #         break

        
    #     counter = counter + 1
    
    




    

