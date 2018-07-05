import sys
sys.path.append('../utils')
sys.path.append('../dtos')
from datetime import date, datetime, timedelta

from python_database_connector import DatabaseConnector
from injector import inject as Inject
from playlist_dto import Playlist

class PlaylistDao:

    @Inject
    def __init__(self):
        self.db = DatabaseConnector()
    
    def get_all_playlist(self):
        query = "SELECT * FROM playlist"
        self.db.executeQuery(query)
        return list(map(lambda playlist: self.map_playlist(playlist),self.db.getQueryResult()))
    
    def get_playlist_by_id(self,id):
        query = "SELECT * FROM playlist WHERE playlist.id = '%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda playlist: self.map_playlist(playlist),self.db.getQueryResult()))

    def insert_playlist(self,json_params):
        params = (json_params['id'],json_params['user_id'],json_params['comment'])
        query = "INSERT INTO playlist (id,useri_id,comment) VALUES ('%s','%s','%s')" % params
        self.db.executeQuery(query, isInsert=True)
        return "saved"

    def delete_playlist(self,id):
        query = "DELETE FROM playlist WHERE playlist.id='%s'" % id
        self.db.executeQuery(query,isInsert=True)
        return "deleted"
    
    def map_playlist(self,playlist_input):
        playlist = Playlist(
            playlist_input['id'],
            playlist_input['user_id'],
            playlist_input['comment']
        )
        return playlist.__dict__