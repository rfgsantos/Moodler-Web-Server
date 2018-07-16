import numpy as np
from flask import Flask, jsonify, request, redirect
from utils.python_database_connector import DatabaseConnector
from utils.python_firebase_connection import FirebaseConnection
from utils.classifier_svm import Classifier
from utils.spotify_client import SpotifyClient
from utils.business import Business

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

    business =  Business()

    if(classificacao):
        artist = json.get("artistURI").split(":")[2]
        tracks = list(map(lambda track: track['id'], sp.search_for_top_tracks(artist)['tracks'][:3]))

        business.process_insertion_of_musics(json.get('playlistId'), json.get('userId'), tracks, json.get('hrv'), json.get('trackURI').split(":")[2], json.get('user_evaluation'))

        sp.add_tracks_to_playlist(json.get('playlistId'),json.get('userId'),tracks)
        response_to_android = "Added tracks - Classified as LIKE"
    else:
        sp.remove_track_from_playlist(json.get('userId'),json.get('playlistId'),[json.get('trackURI').split(":")[2]])
        business.remove_track_from_list(json.get('playlistId'),json.get('userId'),tracks,json.get('hrv'),json.get('trackURI').split(":")[2], json.get('user_evaluation'))
        response_to_android = "Removed tracks - Classified as DISLIKE"
    
    return response_to_android

from controllers.user_controller import *
from controllers.playlist_controller import *
from controllers.reaction_controller import *
from controllers.track_controller import *

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=4000)


    
    