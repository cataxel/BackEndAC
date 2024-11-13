import os
from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, db_name):
        self.uri = os.getenv("MONGODB_URI", "mongodb+srv://beto:FEyR64Tyj1VFXo5I@sessions.byekg.mongodb.net/?retryWrites=true&w=majority&appName=Sessions")
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        if not self.client:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]

    def get_collection(self, collection_name):
        if self.db is not None:
            return self.db[collection_name]
        else:
            raise ConnectionError("Database connection is not established.")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
