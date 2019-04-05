from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

import requests
import os
import json

def convertToARD(lat, lon):
    converturl = 'http://landsatlook.usgs.gov/arcgis/rest/services/LLook_Outlines/MapServer/6/query?where=1%3D1&outSr=4326&outFields=H,V&inSr=4326&geometry=%7B%22x%22%3A' + lat + '%2C%22y%22%3A' + lon + '%2C%22spatialReference%22%3A%7B%22wkid%22%3A4326%7D%7D&geometryType=esriGeometryPoint&spatialRel=esriSpatialRelIntersects&orderByFields=H%20ASC&f=json'
    r = requests.get(converturl)
    rresponse = r.json()
    features = rresponse['features']
    h = features[0]['attributes']['H']
    v = features[0]['attributes']['V']
    region='CU'
    horizontal=h
    vertical=v
    return {"region":region, "horizontal":horizontal, "vertical":vertical, "lat":lat, "lon":lon}



@app.route("/", methods=['POST'])
def home():
    """
    Gets latitude and longitude from POST request
    """
    req_data = request.get_json()
    latitude = req_data['latitude']
    longitude = req_data['longitude']
    username = req_data['username']
    password = req_data['password']
    payload = dict(username=username, password=password, catalogId='EE', authType='EROS')
    data = dict(jsonRequest=json.dumps(payload))
    r = requests.post('https://earthexplorer.usgs.gov/inventory/json/v/1.4.0/login', data=data)
    creds = r.json()
    apiKey = creds['data']
    return apiKey
    print(latitude)
    print(longitude)
        



    print("start")
    c = convertToARD("-111.35","40.7608",)
    search_results = get_scenes("CU", c['horizontal'], c['vertical'])

    print('Found {} scenes'.format(search_results['data']['totalHits']))
    print('Returned {} scenes'.format(search_results['data']['numberReturned']))
    print('First acquisition: ', search_results['data']['results'][0]['acquisitionDate'])
    print('First acquisition = ')

    print(search_results['data']['results'])

    print(search_results['data']['results'][0]['browseUrl'])

    print('Last acquisition: ', search_results['data']['results'][-1]['acquisitionDate'])

    print('Last acquisition JPG: ')
    print(search_results['data']['results'][-1]['browseUrl'])



    # grab a file for testing
    ids = [x['entityId'] for x in search_results['data']['results']]

    # Download all in serial (try first 5)
    success = []
    fail = []
    for entityId in ids[:5]:
        print(entityId)
        try:
            tarname, url = get_url(entityId, apiKey)
            download(tarname, url)
            success.append(entityId)
        except IndexError:
            print('no downloadable product for that id...')
            fail.append(entityId)

    return "Latitude: " + str(latitude) + " , Longitude: " + str(longitude)

if __name__ == "__main__":
    app.run(debug=True)

