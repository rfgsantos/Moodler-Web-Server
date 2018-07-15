from datetime import date, datetime, timedelta
from utils.python_database_connector import DatabaseConnector
from dtos.user_dto import User

class UserDao:

    def __init__(self):
        self.db = DatabaseConnector()

    def get_all_users(self): 
        self.db.executeQuery("SELECT * FROM user")
        return list(map(lambda user: self.map_user(user),self.db.getQueryResult()))
    
    def get_user_by_id(self,id):
        query = "SELECT * FROM user WHERE user.id='%s'" % id
        self.db.executeQuery(query)
        return list(map(lambda user: self.map_user(user),self.db.getQueryResult()))

    def insert_user(self,json_params):
        params = (json_params['id'], json_params['user_id'], json_params['date'])
        query = "INSERT INTO user (id, user_id, date) VALUES ('%s','%s','%s')" % params
        self.db.executeQuery(query,isInsert=True)
        return "saved"
    
    def delete_user(self,id):
        query = "DELETE FROM user WHERE user.id ='%s'" % id
        self.db.executeQuery(query,isInsert=True)
        return "deleted"
    
    def map_user(self,user_input):
        user = User(
            user_input['id'],
            user_input['user_id'],
            user_input['date'],
        )
        return user.__dict__

        
        