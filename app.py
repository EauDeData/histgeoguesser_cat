from flask import Flask, render_template, jsonify, request
import pandas as pd
import random
from geopy.distance import geodesic
import json
from tqdm import tqdm
import time
import random
import pickle as pkl
flask_app = Flask(__name__)

df = pd.read_csv('locs.tsv', sep='\t')
location_lut = pkl.load(open('locations_lut.pkl', 'rb')) # json.load(open('locations_lut_somehowfixed.json'))
debug = False

# Create a dictionary where each location maps to a list of URLs
location_images = {}
descriptions = {}
for index, row in  tqdm(df.iterrows(), total=len(df), desc='loading data for app...'):
    loc_list = str(row['locs']).split(';')
    if not row['url'] in descriptions:
        descriptions[row['url']] = row['descs']
    for loc in loc_list:
        if loc not in location_images:
            location_images[loc] = []
        location_images[loc].append(row['url'])
    if debug and len(location_images) > 10: break

# Filter locations that exist in location_lut
location_coords = {loc: location_lut[loc]['latlong'] for loc in location_images if loc in location_lut}


@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/get_random_image')
def get_random_image():
    loc = random.choice(list(location_coords.keys()))
    img_url = random.choice(location_images[loc])
    latlong = location_coords[loc]
    desc = descriptions[img_url]
    return jsonify({'url': img_url, 'latlong': latlong, 'location': loc})

@flask_app.route('/submit_guess', methods=['POST'])
def submit_guess():
    data = request.get_json()
    guessed_coords = (data['lat'], data['lng'])
    actual_coords = tuple(data['actual_latlong'])
    distance = geodesic(guessed_coords, actual_coords).kilometers
    fname = f"{time.time()}_{random.randint(0, 100)}_dist_{distance}_km"
    with open(f'players/{fname}', 'w') as handler:
        handler.write(f"{data['url']}\n{distance}")

    return jsonify({'distance': distance, 'actual_latlong': actual_coords, 'location': data['location'],
                    'description': descriptions[data['url']]})



if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=False)
