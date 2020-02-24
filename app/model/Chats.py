from .. import pyrebase_settings
from datetime import datetime

def getChatDatabyId(id):
    db = pyrebase_settings.firebase.database()
    chat = db.child("Chats").child(id).get()
    chatData = chat.val()
    return chatData

def save_chat(id, isseen, message, receiver, sender, senttime, type):
    db = pyrebase_settings.firebase.database()

    data = {
    "id": id,
    "isseen": isseen,
    "message": message,
    "receiver": receiver,
    "sender": sender,
    "senttime": senttime,
    "type": type
    }

    db.child("Chats").child(id).set(data)

def getChatsbySenserAndReceiver(sender, receiver):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("Chats").get()
    for chat in all_chats.each():
        if chat.val()['sender'] == sender and chat.val()['receiver'] == receiver:
             Data[chat.key()] = chat.val()
    return Data

def getAllChatsbySenserAndReceiver(sender, receiver):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("Chats").get()
    for chat in all_chats.each():
        if (chat.val()['sender'] == sender and chat.val()['receiver'] == receiver) or (chat.val()['sender'] == receiver and chat.val()['receiver'] == sender):
            formatedTime = datetime.fromtimestamp(chat.val()['senttime']/1000)
            formatedTime = formatedTime.strftime("%H:%M:%S")
            chat.val()['senttime'] = formatedTime
            Data[chat.key()] = chat.val()

    return Data


def seenMessage(id):
    db = pyrebase_settings.firebase.database()
    data = {
    "isseen": True
    }
    db.child("Chats").child(id).update(data)


def getLastMessage(sender,receiver):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("Chats").get()
    for chat in all_chats.each():
        if (chat.val()['sender'] == sender and chat.val()['receiver'] == receiver) or (chat.val()['sender'] == receiver and chat.val()['receiver'] == sender):
            formatedTime = datetime.fromtimestamp(chat.val()['senttime']/1000)
            formatedTime = formatedTime.strftime("%H:%M:%S")
            chat.val()['senttime'] = formatedTime
            Data[chat.key()] = chat.val()

    if bool(Data):
        return Data.popitem()[-1]
    else:
        return False


def generate_id():
    db = pyrebase_settings.firebase.database()
    id = db.generate_key()
    return id

import time
def uploadImage(img):
    storage = pyrebase_settings.firebase.storage()
    stamp = str(int(time.time() * 1000))
    cloud_name = stamp + '.' + img.split(".")[-1]

    storage.child("uploads/"+cloud_name).put(img)
    return storage.child("uploads/"+cloud_name).get_url(None)
