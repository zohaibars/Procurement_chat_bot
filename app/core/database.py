from pymongo import MongoClient
from config.settings import settings

class Database:
    client = None
    db = None
    collection = None

    @classmethod
    def connect(cls):
        if not cls.client:
            cls.client = MongoClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DB]
            cls.collection = cls.db[settings.MONGODB_COLLECTION]
        return cls.collection

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            cls.collection = None