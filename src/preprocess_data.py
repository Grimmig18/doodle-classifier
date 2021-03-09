import json
import ndjson

# Create dict for processed data
rec = []

# Read raw data
with open('./data/raw/octopus.ndjson', 'r', encoding='utf-8') as raws:
    reader = ndjson.reader(raws)
    total_images = 0

    for raw in raws:
        raw_json = json.loads(raw)
        
        if raw_json['recognized'] == True:
            # Extrect only the information we care about
            new_r = {
                'word': raw_json['word'],
                'drawing': raw_json['drawing']
            }
            rec.append(new_r)




with open('./data/processed/octopus.ndjson', 'w', encoding='utf-8') as f:
    for r in rec:
        f.write(str(r)+ '\n')
    

