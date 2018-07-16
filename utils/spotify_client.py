import spotipy as sp
import spotipy.util as util
import spotipy.oauth2 as oauth

class SpotifyClient(object):

    def __init__(self):
        self.token = None
        self.spotify = None

    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(SpotifyClient, cls).__new__(cls)
       return cls.instance

    def add_tracks_to_playlist(self,playlist_id,user_id,tracks_ids):
        self.spotify.user_playlist_add_tracks(user_id,playlist_id,tracks_ids)

    def search_for_top_tracks(self, artist_id):
        return self.spotify.artist_top_tracks(artist_id)
    
    def remove_track_from_playlist(self,user_id, playlist_id, track_ids):
        self.spotify.user_playlist_remove_all_occurrences_of_tracks(user_id,playlist_id,track_ids)
    
    def set_token(self, token):
        self.token = token
        self.spotify = sp.Spotify(auth=self.token)

    
