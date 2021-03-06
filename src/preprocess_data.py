import os
import sys
root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

import json
import ndjson
import numpy as np
from scipy.spatial.distance import pdist
import math


from src.qd import QuickDrawing
import json
import numpy as np
from functools import reduce

import time
import sys

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],[(t*1000,),1000,60,60])
            
def print_progress(p, start_time):
    sys.stdout.write("\r" + str(p) + "% \t Time elapsed: " + secondsToStr(time.time() - start_time) + "s")
    sys.stdout.flush()

def total_lines(line_index, f_name, path='../data/raw/'):
    if f_name not in line_index:
        # print("Count line numbers in file: {}".format(f_name))
        total = 0
        with open(path + f_name, 'r', encoding='utf-8') as f:
            total = sum(1 for l in f)

        line_index[f_name] = total
        return line_index, total
    else:
        # print("Got line number from dict: {}".format(f_name))
        return line_index, line_index[f_name]


f_names = ["pizza.ndjson", "helicopter.ndjson", "octopus.ndjson"]

# def count_items(a):
#     unique, counts = np.unique(a, return_counts=True)
#     print(dict(zip(unique, counts)))

def compute_file(f_name):
    start_time = time.time()
    print("Computing file: ", f_name)
    # Get total number of lines
    total = total_lines(f_name)

    sm = 1 / total * 100

    # Read raw data
    # Create dict for processed data
    rec = []
    img = {}
    counter = 1
    with open('../data/raw/' + f_name, 'r') as f:
        for l in f:
            
            js = json.loads(l)

            if js['recognized'] == False:
                continue

            js['image'] = js['drawing']
            img = QuickDrawing('example', js)

            img_data = QuickDrawing.image_to_stroke_array(list(img.image.getdata()))

            new_r = {
                'word': js['word'],
                'drawing': img_data
            }

            rec.append(new_r)

            percentage = (counter / total) * 100

            if percentage % 0.01 < sm:
                print_progress(round(percentage, 2), start_time)

                # Save batch
                with open('../data/processed/' + f_name, 'a+', encoding='utf-8') as f:
                    for r in rec:
                        f.write(str(r)+ '\n')

                # Reset record
                rec = []   

            counter = counter + 1
        
        print("\n")

def preprocess():
    for fn in f_names:
        compute_file(fn)

    print("Done")


    

