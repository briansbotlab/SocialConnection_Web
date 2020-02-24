from .. import pyrebase_settings

def getUserDatabyId(userid):
    db = pyrebase_settings.firebase.database()
    user = db.child("Users").child(userid).get()
    userData = user.val()
    return userData

def update_user(id,username,imageURL):
    db = pyrebase_settings.firebase.database()
    data = {
    "username": username,
    "search": username.lower(),
    "imageURL": imageURL
    }
    db.child("Users").child(id).update(data)

def save_user(username, email, id):
    db = pyrebase_settings.firebase.database()

    data = {
    "username": username,
    "email": email,
    "id": id,
    "imageURL": "default",
    "status": "offline",
    "search": username.lower()
    }

    db.child("Users").child(id).set(data)

def getUsers():
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_users = db.child("Users").get()
    for user in all_users.each():
        Data[user.key()] = user.val()
    return Data

def isUserExist(id):
    db = pyrebase_settings.firebase.database()
    all_users = db.child("Users").get()
    for user in all_users.each():
        if user.key() == id:
            return True
    return False

def searchUsers(s):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_users = db.child("Users").get()
    for user in all_users.each():
        if s in user.val()['search']:
            Data[user.key()] = user.val()
    if bool(Data):
        return Data
    else:
        return False

import time
def uploadImage(img):
    storage = pyrebase_settings.firebase.storage()
    stamp = str(int(time.time() * 1000))
    cloud_name = stamp + '.' + img.split(".")[-1]

    storage.child("uploads/"+cloud_name).put(img)
    return storage.child("uploads/"+cloud_name).get_url(None)


def stream_handler(users):
    return users
