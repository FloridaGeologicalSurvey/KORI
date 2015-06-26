'''
Created on Jun 26, 2015
@author: Seth Bassett

Module containing functions for breaking apart geoJSON generated
by QGIS and adding github compliant symbology

'''
import json

def symbologize(path, symbolDictionary):
    with open(path) as f:
        data = json.load(f)
    
    for row in data['features'][:]:
        for item in symbolDictionary.iteritems():
            if item[1]:
                row['properties'][item[0]] = item[1]
    
    return data
      
        
def get_symbol_dictionary():
    '''Returns a blank symbol dictionary
    Refer to https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0'''
    symbolDictionary = {"description": None,
                        'marker-size':None,
                        'marker-symbol':None,
                        'marker-color': None,
                        'stroke':None,
                        'stroke-opacity':None,
                        'stroke-width':None,
                        'fill':None,
                        'fill-opacity':None}
    return symbolDictionary

def write_json(jsonObj, path):
    with open(path, 'w') as outfile:
        json.dump(jsonObj, outfile, indent=1)
        
if __name__ == '__main__':
    inFile = r'C:\GISData\WKP Data\Spatial Data\JSON\json\caljamison_karst_points.geojson'
    outFile = 'c:/rdata/caljamison_karst_features_module.geojson'
    
    sdict = get_symbol_dictionary()
    sdict['marker-size'] = 'small'
    sdict['marker-symbol'] = 'triangle'
    sdict['marker-color'] = '#CC0099'
    write_json(symbologize(inFile, sdict), outFile)