from flask import jsonify

class User:

    def __init__(self,id,name,access_token,refresh_token,expires_at):
        self.id = id
        self.name = name
        self.access_token = access_token
        self.refesh_token = refresh_token
        self.expires_at = expires_at
        
    
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_access_token(self):
        return self.access_token
    
    def get_refresh_toekn(self):
        return self.refesh_token

    def get_expires_at(self):
        return self.expires_at
    