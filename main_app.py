import numpy as np
from flask import Flask, jsonify, request, redirect
from utils.python_database_connector import DatabaseConnector
from utils.python_firebase_connection import FirebaseConnection
from utils.classifier_svm import Classifier
from utils.spotify_client import SpotifyClient 

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>MOODLER API</h1>"

@app.route('/hrv_modify_playlist', methods=['POST'])
def testesssssss():
    headers = request.headers
    print("token -> {}".format(headers.get("Authorization").split(" ")[1]))
    sp = SpotifyClient(headers.get("Authorization").split(" ")[1])
    sp.authorize_spotify_client()
    return "d"

from controllers.user_controller import *
# from playlist_controller import *
# from reaction_controller import *
# from track_controller import *
# from recommendation_controller import *



# if __name__ == "__main__":
    # Classifier()
    # app.run(host='0.0.0.0',debug=True,port=4000)


    
    