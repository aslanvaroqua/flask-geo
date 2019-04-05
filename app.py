from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

@app.route("/", methods=['POST'])
def home():
    """
    Gets latitude and longitude from POST request
    """
    req_data = request.get_json()
    latitude = req_data['latitude']
    longitude = req_data['longitude']
    print(latitude)
    print(longitude)
    return "Latitude: " + str(latitude) + " , Longitude: " + str(longitude)

if __name__ == "__main__":
    app.run(debug=True)

