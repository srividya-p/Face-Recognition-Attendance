from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

client = MongoClient(MONGODB_URL)
db = client.get_database('Student')

records = db.Lecture1

def update(names):
    for name in names:
        attendance_update = {
            'attendance': 'present'
        }
        idx = name.index('_')
        roll = name[idx+1 :]
        records.update({'roll': roll}, {'$set': attendance_update})
    print('Attendance Records Updated!')