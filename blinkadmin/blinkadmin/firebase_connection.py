import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    try:
        cred = credentials.Certificate("../blink-a34ae-firebase-adminsdk-5myau-fd79745951.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://blink-a34ae.firebaseio.com"})
    except Exception as e:
        print(e)

initialize_firebase()