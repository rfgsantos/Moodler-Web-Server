import numpy as np
from flask import Flask, jsonify, request, redirect
from utils.python_database_connector import DatabaseConnector
from utils.python_firebase_connection import FirebaseConnection
from utils.classifier_svm import Classifier
from utils.spotify_client import SpotifyClient 

app = Flask(__name__)

@app.route('/teste')
def teste():
    spotify_client = SpotifyClient()
    return redirect(spotify_client.url_redirect)

@app.route('/redirect', methods=['GET'])
def uri_get_red():
    code = request.args.get('code')
    spotify_client = SpotifyClient()
    spotify_client.authorize_spotify_client(code)
    return "redirected"

@app.route('/test2', methods=['GET'])
def uri_get_red():
    return "TESTE 2"

from controllers.user_controller import *
# from playlist_controller import *
# from reaction_controller import *
# from track_controller import *
# from recommendation_controller import *



# if __name__ == "__main__":
#     app.run(host='0.0.0.0',debug=True,port=4000)


    
    