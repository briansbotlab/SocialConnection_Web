from .. import pyrebase_settings

def getGroupChatSeenListDatabyId(id):
    db = pyrebase_settings.firebase.database()
    d = db.child("GroupChatSeenList").child(id).get()
    tData = d.val()
    return Data

def save_data(roomid,chatid,userid,seen):
    db = pyrebase_settings.firebase.database()

    data = {
    "id": userid,
    "seen":seen
    }

    db.child("GroupChatSeenList").child(roomid).child(chatid).child(userid).set(data)

def isUserSeenChat(roomid,chatid,userid):
    db = pyrebase_settings.firebase.database()
    data = db.child("GroupChatSeenList").child(roomid).child(chatid).get()
    try:
        for user in data.each():
            if user.key() == userid:
                return True
    except:
        return False
    return False
