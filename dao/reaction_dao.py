import sys
sys.path.append('../utils')
sys.path.append('../dtos')
from datetime import date, datetime, timedelta
from python_database_connector import DatabaseConnector
from reaction_dto import Reaction

class ReactionDao:

    def __init__(self):
        self.db = DatabaseConnector()
    
    def get_all_reaction(self):
        query = "SELECT * FROM reaction"
        self.db.executeQuery(query)
        return list(map(lambda reaction: self.map_reaction(reaction), self.db.getQueryResult()))
    
    def get_reaction_by_id(self,id):
        query = "SELECT * FROM reaction WHERE reaction.id='%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda reaction: self.map_reaction(reaction), self.db.getQueryResult()))
    
    def insert_reaction(self,json_params):
        params = (json_params['id'],json_params['user_id'],json_params['track_id'],json_params['hrv'],json_params['date'],json_params['gps'])
        query = "INSERT INTO reaction (id,user_id,track_id,hrv,date,gps) \
        VALUES ('%s','%s','%s','%s','%s','%s')" % params
        self.db.executeQuery(query,isInsert=True)
        return "saved"

    def delete_reaction(self,id):
        query = "DELETE FROM reaction WHERE reaction.id='%s'" % id
        self.db.executeQuery(query,isInsert=True)
        return "deleted"

    def map_reaction(self,reaction_input):
        reaction = Reaction(
            reaction_input['id'],
            reaction_input['user_id'],
            reaction_input['track_id'],
            reaction_input['hrv'],
            reaction_input['date'],
            reaction_input['gps']
        )
        return reaction.__dict__
