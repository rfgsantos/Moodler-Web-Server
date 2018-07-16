from datetime import date, datetime, timedelta
from utils.python_database_connector import DatabaseConnector
from injector import inject as Inject
from dtos.playlist_dto import Playlist

class PlaylistDao:

    def __init__(self):
        self.db = DatabaseConnector()
    
    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(PlaylistDao, cls).__new__(cls)
       return cls.instance
    
    def get_all_playlist(self):
        query = "SELECT * FROM playlist"
        self.db.executeQuery(query)
        return list(map(lambda playlist: self.map_playlist(playlist),self.db.getQueryResult()))
    
    def get_playlist_by_id(self,id):
        query = "SELECT * FROM playlist WHERE playlist.playlist_id = '%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda playlist: self.map_playlist(playlist),self.db.getQueryResult()))

    def insert_playlist(self,json_params):
        params = (json_params['id'],json_params['user_id'],json_params['playlist_id'])
        query = "INSERT INTO playlist (id,user_id,playlist_id) VALUES ('%s','%s','%s')" % params
        return self.db.executeQuery(query, isInsert=True)

    def delete_playlist(self,id):
        query = "DELETE FROM playlist WHERE playlist.id='%s'" % id
        return self.db.executeQuery(query,isInsert=True)

    
    def map_playlist(self,playlist_input):
        playlist = Playlist(
            playlist_input['id'],
            playlist_input['user_id'],
            playlist_input['playlist_id']
        )
        return playlist.__dict__