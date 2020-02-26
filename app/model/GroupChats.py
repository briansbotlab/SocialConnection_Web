from .. import pyrebase_settings
from datetime import datetime

def getGroupChatDatabyId(id):
    db = pyrebase_settings.firebase.database()
    chat = db.child("GroupChats").child(id).get()
    chatData = chat.val()
    return chatData

def save_chat(id, message, roomid, sender, sendername, senttime, type):
    db = pyrebase_settings.firebase.database()

    data = {
    "id": id,
    "message": message,
    "receiver": roomid,
    "roomid": roomid,
    "seennum":0,
    "sender": sender,
    "sendername":sendername,
    "senttime": senttime,
    "type": type
    }

    db.child("GroupChats").child(id).set(data)

def updataSeenNum(id,num):
    db = pyrebase_settings.firebase.database()
    data = {
    "seennum": num
    }
    db.child("GroupChats").child(id).update(data)

def getAllChatsbyRoomid(roomid):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("GroupChats").get()
    for chat in all_chats.each():
        if chat.val()['roomid'] == roomid:
            formatedTime = datetime.fromtimestamp(chat.val()['senttime']/1000)
            formatedTime = formatedTime.strftime("%H:%M:%S")
            chat.val()['senttime'] = formatedTime
            Data[chat.key()] = chat.val()
    return Data


def getLastMessage(roomid):
    Data = {}
    db = pyrebase_settings.firebase.database()
    all_chats = db.child("GroupChats").get()
    for chat in all_chats.each():
        if chat.val()['roomid'] == roomid:
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

#def stream_handler(message):
    ## TODO:
