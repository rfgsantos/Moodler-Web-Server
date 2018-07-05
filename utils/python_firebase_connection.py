
from firebase import firebase
from injector import Module, Key, Injector, inject, singleton, provider
import asyncio

@singleton
class FirebaseConnection(object):

    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(FirebaseConnection, cls).__new__(cls)
       return cls.instance

    def __init__(self):
        self.database = 'https://hrpy-d7cae.firebaseio.com/'
        self.firebase = firebase.FirebaseApplication(self.database)

    def get_all_data(self):
        result = self.firebase.get('/evaluation', None)
        return list(dict(result).values()) 