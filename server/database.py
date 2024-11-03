from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys, os
from dotenv import load_dotenv
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PW = os.getenv('MONGO_PW')

uri = "mongodb+srv://{}:{}@cluster0.30uxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(MONGO_USER, MONGO_PW)
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client.get_database("mind_orbit_db")
    users = database.get_collection('users')
    tasks = database.get_collection('tasks')
    print("Successfully connected to database")
except Exception as e:
    print("Failed: ", e)

# Name
# Email
# Excercises
# Sleep
# Stress
# Hobbies

def create_user(name, email, survey_response):
    user = {        
        'name': name,
        'email': email,
        'exercise': survey_response['exercise'],
        'sleep': survey_response['sleep'],
        'stress': survey_response['stress'],
        'hobbies': survey_response['hobbies']
    }
    return users

def get_user_info(email):
    try:
        return users.find_one({'email': email})
    except Exception:
        return False 

def insert_user(user):
    try:
        users.insert(user)
        return True
    except Exception:
        return False

# goes in oauth
def logout():
    return None

# insert new into database
# find every user that prefers excerise
# 