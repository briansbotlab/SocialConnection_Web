from .. import pyrebase_settings

def getGroupChatDatabyId(id):
    db = pyrebase_settings.firebase.database()
    chat = db.child("GroupChats").child(id).get()
    chatData = chat.val()
    return chatData

def save_chat(id, message, receiver, sender, sendername, senttime, type):
    db = pyrebase_settings.firebase.database()

    data = {
    "id": id,
    "message": message,
    "receiver": receiver,
    "roomid": roomid,
    "seennum":0,
    "sender": sender,
    "sendername":sendername,
    "senttime": senttime,
    "type": type
    }

    db.child("GroupChats").child(id).set(data)


def getLastMessage(roomid):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("GroupChats").get()
    for chat in all_chats.each():
        if chat.val()['roomid'] == roomid:
             Data[chat.key()] = chat.val()

    if bool(Data):
        return Data.popitem()[-1]
    else:
        return False

#def stream_handler(message):
    ## TODO:
