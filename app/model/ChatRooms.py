from .. import pyrebase_settings

def getChatRoomDatabyId(id):
    db = pyrebase_settings.firebase.database()
    chatlist = db.child("ChatRooms").child(id).get()
    chatlistData = chatlist.val()
    return chatlistData

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
#def stream_handler(users):
    # TODO:
