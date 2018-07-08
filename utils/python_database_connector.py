import mysql.connector as con
from mysql.connector import errorcode
import utils.database_properties as properties
from injector import Module, Key, Injector, inject, singleton, provider

class DatabaseConnector(object):

    def __new__(cls):
       if not hasattr(cls, 'instance'):
           cls.instance = super(DatabaseConnector, cls).__new__(cls)
       return cls.instance

    def __init__(self):
        self.params = properties.python_db_params_heroku
        self.cnx = None
        self.cursor = None
        self.connect()

    def executeQuery(self, prepared_statement, isInsert=False):
        self.cursor.execute(prepared_statement)
        if isInsert:
            self.cnx.commit()

    def connect(self):
        try:
            self.cnx = con.connect(**self.params)
            self.cursor = self.cnx.cursor(dictionary=True)
        except con.Error as err:
            raise Exception(err)

    def disconnect(self):
        self.cnx.close()
        self.cursor.close()

    def getQueryResult(self,limit=None):
        if limit is not None:
            return self.cursor.fetchmany(limit)
        return self.cursor.fetchall()
