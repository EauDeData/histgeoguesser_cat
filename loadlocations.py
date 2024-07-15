import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm
import json
from multiprocessing import Pool
import pickle as pkl
locations = pd.read_csv('locs.tsv', sep='\t')
geolocator = Nominatim(user_agent="xacmap")

df_cleaned = locations.dropna(subset=['locs'])

locations_lut = {}

for location in tqdm(df_cleaned['locs']):
    # json.dump(locations_lut, open('locations_lut.json', 'w'))
    for subloc in location.split(';'):
        if not subloc in locations_lut:
            try:
                # print(locations_lut)
                parsed_loaction = geolocator.geocode(subloc, language='cat')
            except: continue

            if not parsed_loaction is None:
                locations_lut[subloc] = {"latlong": (parsed_loaction.latitude, parsed_loaction.longitude), "address": parsed_loaction.address}
    pkl.dump(locations_lut, open('locations_lut.pkl', 'wb'))
pkl.dump(locations_lut, open('locations_lut.pkl', 'wb'))
