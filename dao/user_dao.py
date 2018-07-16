from datetime import date, datetime, timedelta
from utils.python_database_connector import DatabaseConnector
from dtos.user_dto import User

class UserDao:

    def __init__(self):
        self.db = DatabaseConnector()
    
    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(UserDao, cls).__new__(cls)
       return cls.instance

    def get_all_users(self): 
        self.db.executeQuery("SELECT * FROM user")
        return list(map(lambda user: self.map_user(user),self.db.getQueryResult()))
    
    def get_user_by_id(self,user_id):
        query = "SELECT * FROM user WHERE user.user_id='%s'" % user_id
        self.db.executeQuery(query)
        return list(map(lambda user: self.map_user(user),self.db.getQueryResult()))

    def insert_user(self,json_params):
        params = (json_params['id'], json_params['user_id'], json_params['date'])
        query = "INSERT INTO user (id, user_id, date) VALUES ('%s','%s','%s')" % params
        return self.db.executeQuery(query,isInsert=True)
    
    def delete_user(self,id):
        query = "DELETE FROM user WHERE user.id ='%s'" % id
        return self.db.executeQuery(query,isInsert=True)
    
    def map_user(self,user_input):
        user = User(
            user_input['id'],
            user_input['user_id'],
            user_input['date'],
        )
        return user.__dict__

        
        