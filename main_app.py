import numpy as np
from flask import Flask, jsonify, request, redirect
from utils.python_database_connector import DatabaseConnector
from utils.python_firebase_connection import FirebaseConnection
from utils.classifier_svm import Classifier
from utils.spotify_client import SpotifyClient 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<h1>MOODLER API</h1>"

@app.route('/train_classifier', methods=['GET'])
def train_classifier():
    cf = Classifier()
    cf.train_after_playlist()
    return "you trained the classifier" 

@app.route('/hrv_modify_playlist', methods=['POST'])
def hrv_modify_playlist():
    response_to_android = ""
    headers = request.headers
    json = request.json
    sp = SpotifyClient()
    sp.set_token(headers.get("Authorization").split(" ")[1])

    classifier = Classifier()
    classificacao = classifier.get_classification(json.get('hrv'))

    if(classificacao):
        artist = json.get("artistURI")
        tracks = []
        for track in sp.search_for_top_tracks(artist)['tracks'][:3]:
            tracks.append(track['id'])

        sp.add_tracks_to_playlist(json.get('playlistId'),json.get('userId'),tracks)

        response_to_android = "Added tracks - Classified as LIKE"
    else:
        sp.remove_track_from_playlist(json.get('userId'),json.get('playlistId'),[json.get('trackId')])
        response_to_android = "Removed tracks - Classified as DISLIKE"
    
    return response_to_android

from controllers.user_controller import *
# from playlist_controller import *
# from reaction_controller import *
# from track_controller import *
# from recommendation_controller import *



if __name__ == "__main__":
    # Classifier()
    app.run(host='0.0.0.0',debug=True,port=4000)


    
    