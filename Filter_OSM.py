import pandas as pd
import osmium
import json
import time

class HotelHandler(osmium.SimpleHandler):
    def __init__(self):
        super(HotelHandler, self).__init__()
        self.restaurants = []

    def node(self, o):
        if o.tags.get('amenity') in classes:
            item = {str(tag).split('=')[0]:str(tag).split('=')[1] for tag in o.tags}
            self.restaurants.append(item)

classes = ['restaurant', 'bar', 'pub', 'fast_food', 'ice_cream', 'biergarten', 'cafe', 'food_court']

start = time.time()
h = HotelHandler()
h.apply_file("data/limburg-latest.osm.pbf")
with open('data/restaurants.json', 'a', encoding='utf-8') as outfile:
    outfile.write('\n'.join(map(json.dumps, h.restaurants)) + '\n')
end = time.time()

print(end - start)
print(len(h.restaurants))