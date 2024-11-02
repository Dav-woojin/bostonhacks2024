from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys, os
from dotenv import load_dotenv
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PW = os.getenv('MONGO_PW')

uri = "mongodb+srv://{}:{}@cluster0.30uxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(MONGO_USER, MONGO_PW)

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)