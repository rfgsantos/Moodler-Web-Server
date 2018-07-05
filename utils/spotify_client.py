import spotipy as sp
import spotipy.util as util
import spotipy.oauth2 as oauth

class SpotifyClient(object):

    client_id = "18ee01c0d6fc47c99f5f30ad7e5279ff"
    client_secret = "977f060a4d944a378d78582f51467a77"
    client_redirect_uri = "http://localhost:4000/redirect"
    client_scope = "playlist-modify-public"

    def __init__(self):
        self.auth = oauth.SpotifyOAuth(SpotifyClient.client_id, SpotifyClient.client_secret, SpotifyClient.client_redirect_uri, scope=SpotifyClient.client_scope)
        self.url_redirect = self.auth.get_authorize_url()
        self.token = None
        self.spotify = None
        self.refresh_token = None

    #singleton
    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(SpotifyClient, cls).__new__(cls)
       return cls.instance

    def authorize_spotify_client(self,code):
        response = self.auth.get_access_token(code)
        self.token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.spotify = sp.Spotify(auth=self.token)
        print(self.spotify.user_playlist_create('rsantos92','HRV TESTE3')) 

    
