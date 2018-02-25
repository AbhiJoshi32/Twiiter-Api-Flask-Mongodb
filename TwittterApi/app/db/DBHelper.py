from pymongo import MongoClient
from TwittterApi.config import *
import TwittterApi.config

class DBHelper:
    def __init__(self,db_name):
        self.mongo_client = MongoClient(DB_HOST, DB_PORT, connect=False)
        self.db_name = db_name
        self.db = self.mongo_client[db_name]
        
    def insertDoc(self,doc,collection):
        return self.db[collection].insert_one(doc)

    def findDocs(self,query,collection):
        return self.db[collection].find(query)

    def findOneDoc(self,query,collection):
        return self.db[collection].find_one(query)