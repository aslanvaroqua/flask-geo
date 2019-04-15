from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import jsonify
import uuid
from flask import json
import boto3
import os
import landsatxplore.api as lx
from landsatxplore.earthexplorer import EarthExplorer

username = os.environ.get("LANDSATXPLORE_USERNAME", "skylinegis")
password = os.environ.get("LANDSATXPLORE_PASSWORD", "pepsiav123pepsiav123")

app = FlaskAPI(__name__)

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

@app.route("/", methods=['POST'])
def home():
    """
    Gets latitude and longitude from POST request
    """
    req_data = request.get_json()
    lat = req_data['lat']
    lon = req_data['lon']

    refId = uuid.uuid4()

    username = os.environ.get("LANDSATXPLORE_USERNAME", "skylinegis")
    password = os.environ.get("LANDSATXPLORE_PASSWORD", "pepsiav123pepsiav123")

    print(username)

    # Initialize a new API instance and get an access key
    api = lx.API(username, password)
    # ee = EarthExplorer(username, password)

    # search by location

    # Request
    scenes = api.search(
        dataset='LANDSAT_8_C1',
        latitude=lat,
        longitude=lon,
        start_date='2019-01-01',
        end_date='2019-04-07',
        max_cloud_cover=40)

    print('{} scenes found.'.format(len(scenes)))
    results = []


    for scene in scenes:
        print(scene['acquisitionDate'])
        sceneResponse = add2queue(str(refId),scene)
        results.append(sceneResponse)
    #     ee.download(scene_id=scene['entityId'], output_dir="/home/u/" + str(refId) + "/")
    #
    # ee.logout()



    api.logout()


    # data = jsonify(results)

    return {"refId": str(refId), "crresults":results}


def add2queue(refId, scene):

    sqs = boto3.client('sqs', 'us-west-2')
    print("sqs")
    print(sqs)

    queue_url = 'https://sqs.us-west-2.amazonaws.com/155558474149/lsat-tasks'
    message_body = ""

# Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageBody='{"refId": refId, "eeId" : refId}')

    print(response['MessageId'])
    print(response['MessageId'])
    return response['MessageId']




if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)

