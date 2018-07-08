import spotipy as sp
import spotipy.util as util
import spotipy.oauth2 as oauth

class SpotifyClient(object):

    def __init__(self, token):
        self.token = token
        self.spotify = sp.Spotify(auth=self.token)

    #singleton
    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(SpotifyClient, cls).__new__(cls)
       return cls.instance

    def authorize_spotify_client(self):
        print(self.spotify.user_playlist_create('rsantos92','HRV TESTE3')) 
    
    def create_playlist(self, tracks):
        cenas

    
