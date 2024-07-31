import json
from pymongo import MongoClient
import requests
from bson.objectid import ObjectId
import logging
import random
import math

TOURNEMENT_SIZE = [8, 16, 32, 64]
REQUIRED_TOURNEMENT_FIELDS = ['_id', 'participants']
STAGES = ['group_stage', 'round_of_16', 'quarterfinals', 'semifinals', 'finals']

# MongoDB client setup
try:
    client = MongoClient('mongodb://mongo:27017/')
    db = client.library
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {str(e)}")
    raise

def validate_tournement_data(data):
    if all(field in data for field in REQUIRED_TOURNEMENT_FIELDS):
        if len(data['participants']) not in TOURNEMENT_SIZE:
            return False, 'error: Invalid number of participants. Must be 8, 16, 32, or 64'
        
        return True, None
    
    return False, 'error: Missing required fields'

def build_tournement(data):
    matches = create_matches(data)

    tournement_data = {
        "_id": data['_id'],
        "participants": data['participants'],
    }

    db_tournement_data = tournement_data.copy()
    db.tournements.insert_one(db_tournement_data)
    db.matches.insert_one(matches)

    return tournement_data

def create_matches(data):
    random_participants = data['participants']
    length = len(random_participants)
    matches = {}
    matches['_id'] = data['_id']
    size = math.log2(length)

    random.shuffle(random_participants)
    start = 0 if size >= 5 else 1    

    for stage in STAGES[start:]:
        if stage == STAGES[start]:
            if stage == 'group_stage':
                matches[stage] = {}
                for i in range(0, length, 4):
                    matches[stage][f"group_{chr(65 + i // 4)}"] = random_participants[i:i+4]
            else:
                matches[stage] = {
                    f"match_{i//2}": {
                        "participants": random_participants[i:i+2],
                        "winner": None
                    } for i in range(0, length, 2)
                }
        else:
            matches[stage] = {
                f"match_{i//2}": {
                    "participants": [],
                    "winner": None
                } for i in range(0, length, 2)
            }
        
        length //= 2

    return matches
   
def get_tournement_by_id(tournement_id):
    tournement = db.tournements.find_one({"_id": int(tournement_id)})

    if tournement:
        return tournement

def get_matches_by_id(tournement_id):
    matches = db.matches.find_one({"_id": int(tournement_id)})

    if matches:
        return matches