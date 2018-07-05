import sys
sys.path.append('../utils')
sys.path.append('../dtos')
from datetime import date, datetime, timedelta

from python_database_connector import DatabaseConnector
from injector import inject as Inject
from recomendation_dto import Recomendation

class RecomendationDao:

    @Inject
    def __init__(self):
        self.db = DatabaseConnector()
    
    def get_all_recomendations(self):
        query = "SELECT * FROM recomendation"
        self.db.executeQuery(query)
        return list(map(lambda recomendation: self.map_recomendation(recomendation),self.db.getQueryResult()))
    
    def get_recomendation_by_id(self,id):
        query = "SELECT * FROM recomendation WHERE recomendation.id='%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda recomendation: self.map_recomendation(recomendation),self.db.getQueryResult()))
    
    def insert_recomendation(self,json_params):
        params = (json_params['id'],json_params['playlist_id'],json_params['track_id'])
        query = "INSERT INTO recomendation (id,playlist_id,track_id) VALUES ('%s','%s','%s')" % params
        self.db.executeQuery(query,isInsert=True)
        return "saved"
    
    def delete_recomendation(self,id):
        query = "DELETE FROM recomendation WHERE recomendation.id='%s'" % id
        self.db.executeQuery(query,isInsert=True)
        return "deleted"

    def map_recomendation(self,recomendation_input):
        recomendation = Recomendation(
            recomendation_input['id'],
            recomendation_input['playlist_id'],
            recomendation_input['track_id']
        )
        return recomendation.__dict__