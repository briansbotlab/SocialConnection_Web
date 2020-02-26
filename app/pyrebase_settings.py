from pyrebase import pyrebase

config = {
    "apiKey": "your apiKey",
    "authDomain": "your authDomain",
    "databaseURL": "your databaseURL",
    "projectId": "your projectId",
    "storageBucket": "your storageBucket",
    "messagingSenderId": "your messagingSenderId",
    "appId": "your appId"
  };

# initialize app with config
firebase = pyrebase.initialize_app(config)
