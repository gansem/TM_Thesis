from itertools import combinations

from numpy import mat
from tqdm import tqdm
import pandas as pd
import json


def translate_keys(osm_keys):
    return [translations[key] for key in osm_keys]


def check_keys(osm_keys):
    vyg_keys = translate_keys(osm_keys)
    osm_tags = [item[key].replace('+', '\+') for key in osm_keys]

    df_nona = df[df[vyg_keys[0]].notna()]
    matches = df_nona[df_nona[vyg_keys[0]].str.contains(osm_tags[0])].index.values
    matches = df[df.index.isin(matches)]
    if any(matches[vyg_keys[1]].str.contains(osm_tags[1]).dropna()):
        return True, matches[matches[vyg_keys[1]].str.contains(osm_tags[1])]
    return False, None


def match():
    match_tags = ['lat', 
                    'lon', 
                    'addr:housenumber', 
                    'addr:postcode', 
                    'addr:street', 
                    'name', 
                    'email', 
                    'phone']


    if sum([key in item.keys() for key in match_tags]) >= 2:
        for combination in combinations(match_tags, 2):
            if all([key in item for key in combination]):
                return check_keys(combination)
    return False, None


def create_output_file(path):
    with open('data/wikivoyage-listings-en-latest.csv', 'r') as fid:
        header_list = fid.readline().strip().split(",")

    with open(path, 'w') as fid:
        fid.write(",".join(header_list))

create_output_file('data/voyage_matches.csv')

translations = {'name':'title',
                'email': 'email',
                'phone':'phone',
                'addr:housenumber':'address',
                'addr:street':'address',
                'addr:postcode': 'address',
                'lat': 'latitude', 
                'lon': 'longitude'
                }

matches = 0

df = pd.read_csv('data/wikivoyage-listings-en-latest.csv')
df = df[df['type'].isin(['eat', 'drink']) & df['description'].notna()].reset_index(drop=True)

with open('data/restaurants.json', 'r', encoding='utf-8') as f:
    for line in tqdm(f):
        item = json.loads(line)
        match_bool, matching_item = match()
        if match_bool == True:
            matches += 1
            matching_item.to_csv('data/voyage_matches.csv', mode='a', header=False)
            with open('data/OSM_matches.json', 'a', encoding='utf-8') as f:
                f.write(str(item) + '\n')

print(matches)
