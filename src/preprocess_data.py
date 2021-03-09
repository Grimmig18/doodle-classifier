import json
import ndjson
import numpy as np

f_name = "helicopter.ndjson"

def find_local_max_in_drawing(drawing): 
    max = 0
    for stroke in drawing:
        for point in range(len(stroke[0])):
            if stroke[0][point] > max:
                max = stroke[0][point]
            if stroke[1][point] > max:
                max = stroke[1][point] 
    return max

# Create dict for processed data
rec = []

# Read raw data
with open('./data/raw/' + f_name, 'r', encoding='utf-8') as raws:
    reader = ndjson.reader(raws)
    total_images = 0

    highest_x = 0
    highest_y = 0

    for raw in raws:
        raw_json = json.loads(raw)
        
        if raw_json['recognized'] == True:
            # Extract only the information we care about
            new_r = {
                'word': raw_json['word'],
                'drawing': raw_json['drawing']
            }
            

            # Find highest Value
            max = find_local_max_in_drawing(raw_json['drawing'])

            # Scale strokes
            for stroke in raw_json['drawing']:
                stroke[0] = [int(x) for x in np.rint(np.interp(stroke[0], (0, max), (0, 256))).tolist()]
                stroke[1] = [int(x) for x in np.rint(np.interp(stroke[1], (0, max), (0, 256))).tolist()]
            
            rec.append(new_r)


with open('./data/processed/' + f_name, 'w', encoding='utf-8') as f:
    for r in rec:
        f.write(str(r)+ '\n')
    

