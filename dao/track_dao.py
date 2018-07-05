import sys
sys.path.append('../utils')
sys.path.append('../dtos')
from datetime import date, datetime, timedelta

from python_database_connector import DatabaseConnector
from injector import inject as Inject
from track_dto import Track

class TrackDao:

    def __init__(self):
        self.db = DatabaseConnector()
    
    def get_all_track(self):
        query = "SELECT * FROM track"
        self.db.executeQuery(query)
        return list(map(lambda track: self.map_track(track),self.db.getQueryResult()))
    
    def get_track_by_id(self,id):
        query = "SELECT * FROM track WHERE track.id='%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda track: self.map_track(track),self.db.getQueryResult()))
    
    def insert_track(self,json_params):
        params = (json_params['id'],json_params['durantio_sec'],json_params['danceability'],json_params['energy'],json_params['loudness'],
        json_params['track_key'],json_params['valance'],json_params['tempo'],json_params['time_signature'])
        query = "INSERT INTO track (id,duration_sec,danceability,energy,loudness,track_key,valance,tempo,time_signature) \
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % params
        self.db.executeQuery(query,isInsert=True)
        return "saved"

    def delete_track(self,id):
        query = "DELETE FROM track WHERE track.id='%s'" % id
        self.db.executeQuery(query,isInsert=True)
        return "deleted"
    
    def map_track(self,track_input):   
        track = Track(
            track_input['id'],
            track_input['duration_sec'],
            track_input['danceability'],
            track_input['energy'],
            track_input['loudness'],
            track_input['track_key'],
            track_input['valance'],
            track_input['tempo'],
            track_input['time_signature']
        )
        return track.__dict__