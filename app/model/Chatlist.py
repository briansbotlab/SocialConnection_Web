from .. import pyrebase_settings

def getChatlistDatabyId(id):
    db = pyrebase_settings.firebase.database()
    chatlist = db.child("Chatlist").child(id).get()
    chatlistData = chatlist.val()
    return chatlistData

def save_chatlist(id, receiver_id):
    db = pyrebase_settings.firebase.database()

    data_1 = {
    "id": receiver_id,
    "notify": True,
    }

    data_2 = {
    "id": id,
    "notify": True,
    }

    db.child("Chatlist").child(id).child(receiver_id).set(data_1)
    db.child("Chatlist").child(receiver_id).child(id).set(data_2)

def getChatlistbyId(id):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_data = db.child("Chatlist").child(id).get()
    for data in all_data.each():
        Data[data.key()] = data.val()
    return Data

#def stream_handler(users):
    # TODO:
