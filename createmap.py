import folium
import json
import pandas as pd
from tqdm import tqdm
from folium import IFrame
import pickle as pkl

df = pd.read_csv('locs.tsv', sep='\t')

location_lut = pkl.load(open('locations_lut (copy).pkl', 'rb')) # json.load(open('locations_lut_somehowfixed.json'))


# Step 1: Create a dictionary where each location maps to a list of URLs
location_images = {}

for index, row in tqdm(df.iterrows(), total=len(df)):
    loc_list = str(row['locs']).split(';')
    for loc in loc_list:
        if loc not in location_images:
            location_images[loc] = []
        location_images[loc].append(row['url'])

# Step 2: Transform location names to latlong using location_lut
location_coords = {loc: location_lut[loc]['latlong'] for loc in location_images if loc in location_lut}

# Step 3: Create Folium map
map_center = [41.3879, 2.16992]  # Centered around Barcelona for this example
m = folium.Map(location=map_center, zoom_start=8)



for loc, coords in tqdm(location_coords.items(), total=len(location_coords)):
    # Create a scrollable list of image URLs for the popup
    html = "<div style='width:200px; height:150px; overflow-y:auto;'><ul>"
    for url in location_images[loc]:
        html += f'<li><img src="{url}" width="150"></li>'
    html += "</ul></div>"
    
    iframe = IFrame(html, width=250, height=200)
    popup = folium.Popup(iframe, max_width=250)
    
    folium.Marker(
        location=coords,
        popup=popup,
        tooltip=loc
    ).add_to(m)

# Save the map to an HTML file
m.save("map.html")
