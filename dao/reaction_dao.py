from datetime import date, datetime, timedelta
from utils.python_database_connector import DatabaseConnector
from dtos.reaction_dto import Reaction

class ReactionDao:

    def __init__(self):
        self.db = DatabaseConnector()

    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(ReactionDao, cls).__new__(cls)
       return cls.instance
    
    def get_all_reaction(self):
        query = "SELECT * FROM reaction"
        self.db.executeQuery(query)
        return list(map(lambda reaction: self.map_reaction(reaction), self.db.getQueryResult()))
    
    def get_reaction_by_id(self,id):
        query = "SELECT * FROM reaction WHERE reaction.id='%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda reaction: self.map_reaction(reaction), self.db.getQueryResult()))
    
    def insert_reaction(self,json_params):
        params = (json_params['id'],json_params['user_id'],json_params['track_id'],json_params['hrv'],json_params['evaluation'], json_params['user_evaluation'])
        query = "INSERT INTO reaction (id,user_id,track_id,hrv,evaluation,user_evaluation) VALUES ('%s','%s','%s','%s','%s','%s')" % params
        return self.db.executeQuery(query,isInsert=True)

    def delete_reaction(self,id):
        query = "DELETE FROM reaction WHERE reaction.id='%s'" % id
        return self.db.executeQuery(query,isInsert=True)

    def map_reaction(self,reaction_input):
        reaction = Reaction(
            reaction_input['id'],
            reaction_input['user_id'],
            reaction_input['track_id'],
            reaction_input['hrv'],
            reaction_input['evaluation'],
            reaction_input['user_evaluation']
        )
        return reaction.__dict__
