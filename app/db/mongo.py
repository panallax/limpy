from pymongo import MongoClient
from pymongo.errors import ConnectionError
import os
from dotenv import load_dotenv

class MongoConnectionManager:
    def __init__(self, mongo_uri: str, db_name: str):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.database = None

    def connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.database = self.client[self.db_name]
            print("Connected to MongoDB")
        except ConnectionError as e:
            print(f"Connection error {e}")
            raise e

    def get_database(self):
        if not self.database:
            self.connect()
        return self.database
    
    def get_collection(self, collection_name: str):
        return self.database[collection_name]

    def close(self):
        if self.client:
            self.client.close()
            print("Connection to MongoDB closed")


load_dotenv()
mongo_manager = MongoConnectionManager(
    mongo_uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME")
)
