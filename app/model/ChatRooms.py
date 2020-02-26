from .. import pyrebase_settings

def getChatRoomDatabyId(id):
    db = pyrebase_settings.firebase.database()
    roomlist = db.child("ChatRooms").child(id).get()
    roomlistData = roomlist.val()
    return roomlistData

def save_chatroom(id, chatRoomName, manager, password, secret_status, status):
    db = pyrebase_settings.firebase.database()

    data = {
    "id": id,
    "chatRoomName": chatRoomName,
    "imageURL": "default",
    "manager": manager,
    "password": password,
    "search": chatRoomName.lower(),
    "secret_status": secret_status,
    "status": "offline"
    }

    db.child("ChatRooms").child(id).set(data)


def getChatRooms():
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chatrooms = db.child("ChatRooms").get()
    for chatroom in all_chatrooms.each():
        Data[chatroom.key()] = chatroom.val()
    return Data

def generate_id():
    db = pyrebase_settings.firebase.database()
    id = db.generate_key()
    return id

def searchRooms(s):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chatrooms = db.child("ChatRooms").get()
    for chatroom in all_chatrooms.each():
        if s in chatroom.val()['search']:
            Data[chatroom.key()] = chatroom.val()
    if bool(Data):
        return Data
    else:
        return False

def isRoomExist(id):
    db = pyrebase_settings.firebase.database()
    all_chatrooms = db.child("ChatRooms").get()
    for chatroom in all_chatrooms.each():
        if chatroom.key() == id:
            return True
    return False


def update_Room(id,chatRoomName,password,secret_status):
    db = pyrebase_settings.firebase.database()

    data = {
    "chatRoomName": chatRoomName,
    "password": password,
    "search": chatRoomName.lower(),
    "secret_status": secret_status,
    }
    db.child("ChatRooms").child(id).update(data)

import time
def uploadImage(img):
    storage = pyrebase_settings.firebase.storage()
    stamp = str(int(time.time() * 1000))
    cloud_name = stamp + '.' + img.split(".")[-1]

    storage.child("uploads/"+cloud_name).put(img)
    return storage.child("uploads/"+cloud_name).get_url(None)

def update_RoomImg(id,imageURL):
    db = pyrebase_settings.firebase.database()

    data = {
    "imageURL": imageURL
    }
    db.child("ChatRooms").child(id).update(data)

#def stream_handler(users):
    # TODO:
