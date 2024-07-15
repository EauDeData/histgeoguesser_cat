import json
import os
import spacy
from tqdm import tqdm
import pandas as pd

base_dir = 'extraccions/'
json_files = [os.path.join(base_dir, json_file) for json_file in os.listdir(base_dir)]

# nlp = spacy.load("ca_core_news_trf")
data_to_map = []

for json_dirpath in tqdm(json_files, desc='extracting files...'):
    extracted_data = json.load(open(json_dirpath, encoding='latin-1'))['unitatsDocumentals']
    pd.DataFrame(data_to_map,columns = ('url', 'descs', 'locs')).to_csv('locs.tsv', sep='\t', index=False)
    for fons_data in tqdm(extracted_data, desc=f"Processing {json_dirpath}..."):
        descriptors_toponimics = fons_data['descToponimics']
        descripcions_fons = [fons_data['nomFons']]
        if 'descripcio' in descripcions_fons:
            descripcions_fons = descripcions_fons + fons_data['descripcio']
        
        for image_data in fons_data['imatges']:
            if 'estatFitxer' in image_data and image_data['estatFitxer'] != 'PUBLICAT':
                continue
            if 'descripcio' in image_data:
                descripcions_imatge = [image_data['descripcio']]
            else: descripcions_imatge = []
            total_descripcions = descripcions_fons + descripcions_imatge
            
            # detected_locs = []
            # for desc in total_descripcions:
            #     doc = nlp(desc)
            #     for ent in doc.ents:

            #         if ent.label_ == 'LOC':
            #             detected_locs.append(ent.text)
            data_to_map.append((image_data['url'],  ';'.join(total_descripcions), ';'.join(descriptors_toponimics)))
pd.DataFrame(data_to_map,columns = ('url', 'descs', 'locs')).to_csv('locs.tsv', sep='\t', index=False)

