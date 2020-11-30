from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)
db = client.get_database('Student')

records = db.Lecture1
status_records = db.Status

def update(names, status):
    if (names!=None):
        for name in names:
            attendance_update = {
                'attendance': 'present'
            }
            if (name.find('_') == -1):
                pass
            else:
                idx = name.index('_')
                roll = name[idx+1 :]
                records.update({'roll': roll}, {'$set': attendance_update})
    status_records.update({}, {'$set': {'status': status}})
    print(status)