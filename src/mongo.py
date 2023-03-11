import os
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGODB_HOST'), int(os.environ.get('MONGODB_PORT')))
mongo = client[os.environ.get('MONGODB_DB')]
