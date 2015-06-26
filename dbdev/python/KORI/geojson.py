'''
Created on Jun 26, 2015

@author: Bassett_S
'''
import json

if __name__ == '__main__':
    with open(r'C:\GISData\WKP Data\Spatial Data\JSON\json\caljamison_karst_points.geojson') as f:
        data = json.load(f)
    for feature in data['features']:
        print feature['geometry']['type']
        print feature['geometry']['coordinates']
        