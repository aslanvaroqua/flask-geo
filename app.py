from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import pymongo
import uuid

app = FlaskAPI(__name__)

@app.route("/", methods=['POST'])
def home():
    """
    Gets latitude and longitude from POST request
    """
    req_data = request.get_json()
    lat1 = req_data['lat1']
    lon1 = req_data['lon1']



    print(lat1)
    print(lon1)
    refId = uuid.uuid4()

    # start calculations

    return "Latitude: " + str(lat1) + " , Longitude: " + str(lon1) + "id = " + refId

if __name__ == "__main__":
    app.run(debug=True)

