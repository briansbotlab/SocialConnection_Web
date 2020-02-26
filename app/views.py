from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from sc import settings
from . import pyrebase_settings
from . import sessionCtl
from .model import Users, Chatlist, Chats, ChatRooms, GroupChats, GroupChatSeenList
import time
import json
import os
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if sessionCtl.isSessionExist(request,'uid'):
        return redirect('/main/Chats')
    else:
        return render(request, 'home.html')

def register(request):
    if request.method == "POST":

        auth = pyrebase_settings.firebase.auth()
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if(len(password) < 6):
            message = "Password must at least 6 characters."
            return render(request,"register.html",{"msg":message})

        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            Users.save_user(username, email, user['localId'])
            userData = Users.getUserDatabyId(user['localId'])
            sessionCtl.setLoginSession(request,username,user['localId'],email,userData['imageURL'])
            return redirect('/main/Chats')
        except:
            message = "Unable to Register."
            return render(request,"register.html",{"msg":message})
    else:

        return render(request, 'register.html')


def login(request):
    if request.method == "POST":

        auth = pyrebase_settings.firebase.auth()
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            userData = Users.getUserDatabyId(user['localId'])
            sessionCtl.setLoginSession(request,userData['username'],user['localId'],email,userData['imageURL'])
            return redirect('/main/Chats')
        except:
            message = "Unable to Login."
            return render(request,"login.html",{"msg":message})
    else:
        return render(request, 'login.html')

def resetpassword(request):
    if request.method == "POST":

        auth = pyrebase_settings.firebase.auth()
        email = request.POST['email']

        try:
            auth.send_password_reset_email(email)
            message = "Reset Email has been sent, please confirm your Emailbox."
            return render(request,"resetpassword.html",{"msg":message})
        except:
            message = "Error, please check your input."
            return render(request,"resetpassword.html",{"msg":message})
    else:
        return render(request, 'resetpassword.html')

def chats(request):
    allUsers = Users.getUsers()
    allChatrooms = ChatRooms.getChatRooms()

    currentUserId = sessionCtl.getCurrentUserId(request)
    current_chatlist = Chatlist.getChatlistDatabyId(currentUserId)

    userData = {}
    chatroomData = {}

    if current_chatlist == None:
        return render(request, 'fragment/chats.html')
    else:
        for user in allUsers:
            if user in current_chatlist:
                data = allUsers[user]
                data['userid'] = user
                lastMessage = Chats.getLastMessage(currentUserId,user)
                if lastMessage:
                    data.update(lastMessage)
                userData[user] = data

        for chatroom in allChatrooms:
            if chatroom in current_chatlist:
                data = allChatrooms[chatroom]
                chatroomData[chatroom] = data

        return render(request, 'fragment/chats.html',{"users":userData,"rooms":chatroomData})

def chats_user_room(request,id):
    if Users.isUserExist(id):
        return redirect("/main/Users/"+id)
    elif ChatRooms.isRoomExist(id):
        return room_message(request,id)
    else:
        return redirect("/main/Chats/")



def chatrooms(request):
    allChatrooms = ChatRooms.getChatRooms()

    return render(request, 'fragment/chatrooms.html',{"rooms":allChatrooms})

def search_rooms(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', None)
        if keyword != None:
            room_list = ChatRooms.searchRooms(keyword.lower())
            if room_list:
                qs_json = json.dumps(room_list)
            else:
                qs_json = json.dumps({})
            return HttpResponse(qs_json, content_type='application/json')

def create_rooms(request):
    if request.method == 'POST':
        roomname = request.POST['roomname']
        roompass = request.POST['roompass']
        currentUserId = sessionCtl.getCurrentUserId(request)
        id = ChatRooms.generate_id()
        if(roompass == ""):
            ChatRooms.save_chatroom(id, roomname, currentUserId, roompass, "not_secret", "offline")
            Chatlist.save_chatlist(id, currentUserId)
        else:
            ChatRooms.save_chatroom(id, roomname, currentUserId, roompass, "secret", "offline")
            Chatlist.save_chatlist(id, currentUserId)
    return redirect('/main/ChatRooms/')



def users(request):
    allUsers = Users.getUsers()
    currentUserId = sessionCtl.getCurrentUserId(request)
    for user in allUsers.copy():
        if user == currentUserId:
            allUsers.pop(user)

    return render(request, 'fragment/users.html',{"users":allUsers})

def search_users(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', None)
        currentUserId = sessionCtl.getCurrentUserId(request)
        if keyword != None:
            user_list = Users.searchUsers(keyword.lower())
            if user_list:
                for user in user_list.copy():
                    if user == currentUserId:
                        user_list.pop(user)
                qs_json = json.dumps(user_list)
            else:
                qs_json = json.dumps({})
            return HttpResponse(qs_json, content_type='application/json')



def profile(request):
    currentUserId = sessionCtl.getCurrentUserId(request)
    user = Users.getUserDatabyId(currentUserId)
    return render(request, 'fragment/profile.html',{"user":user})

def edit_profile(request):
    if request.method == "POST":
        username = request.POST['username']
        file = request.FILES.get('upload', False)
        currentUserId = sessionCtl.getCurrentUserId(request)
        if(file):
            file_extension = ['png' , 'jpg', 'jpeg']
            if file.name.split(".")[-1].lower() in file_extension:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                #uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url

                imageURL = Users.uploadImage(uploaded_file_url)
                sessionCtl.updateUsernameAndUserImg(request,username,imageURL)
                Users.update_user(currentUserId,username,imageURL)
                os.remove(uploaded_file_url)
                return redirect('/main/Profile')
        elif(not file):
            Users.update_user(currentUserId,username,"default")
            return redirect('/main/Profile')

    else:
        return redirect('/main/Profile')



def logout(request):
    sessionCtl.delLoginSession(request)
    return redirect('/')

def message(request,userid):
    if Users.isUserExist(userid):
        user = Users.getUserDatabyId(userid)
        currentUserId = sessionCtl.getCurrentUserId(request)
        sessionCtl.setReceiverSession(request,userid)
        Chatlist.save_chatlist(userid, currentUserId)
        all_msg = Chats.getAllChatsbySenserAndReceiver(userid,currentUserId)
        last_msg = Chats.getLastMessage(currentUserId,userid)
        if(not last_msg):
            last_msg = {}
        elif(last_msg['sender'] == userid):
            Chats.seenMessage(last_msg['id'])
        return render(request, 'message.html',{"user":user,"msgs":all_msg,"last_msg":last_msg})
    else:
        return redirect('/main/Users')

def message_interval(request,userid):
    if Users.isUserExist(userid):
        if request.method == 'GET':
            currentUserId = sessionCtl.getCurrentUserId(request)
            last_msg = Chats.getLastMessage(currentUserId,userid)
            if(not last_msg):
                last_msg = {}
            elif(last_msg['sender'] == userid):
                Chats.seenMessage(last_msg['id'])
            all_msg = Chats.getAllChatsbySenserAndReceiver(userid,currentUserId)
            if all_msg:
                qs_json = json.dumps(all_msg)
            else:
                qs_json = json.dumps({})
            return HttpResponse(qs_json, content_type='application/json')

def image_message(request,userid):
    if request.method == "POST":
        file = request.FILES.get('upload', False)
        if(file):
            file_extension = ['png' , 'jpg', 'jpeg']
            if file.name.split(".")[-1].lower() in file_extension:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                #uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url

                imageURL = Chats.uploadImage(uploaded_file_url)
                id = Chats.generate_id()
                receiver, sender = sessionCtl.getCurrentReceiverandSender(request)
                senttime = int(time.time() * 1000)
                Chats.save_chat(id, False, imageURL, receiver, sender, senttime, "image")
                os.remove(uploaded_file_url)
    return redirect('/main/Users/'+userid)

@csrf_exempt
def text_message(request,userid):
    if Users.isUserExist(userid):
        if request.method == "POST":
            message = request.POST['message']
            if message !="":
                id = Chats.generate_id()
                receiver, sender = sessionCtl.getCurrentReceiverandSender(request)
                senttime = int(time.time() * 1000)
                Chats.save_chat(id, False, message, receiver, sender, senttime, "text")
                #return HttpResponse({}, content_type='application/json')
        currentUserId = sessionCtl.getCurrentUserId(request)
        last_msg = Chats.getLastMessage(currentUserId,userid)
        if(not last_msg):
            last_msg = {}
        elif(last_msg['sender'] == userid):
            Chats.seenMessage(last_msg['id'])
        all_msg = Chats.getAllChatsbySenserAndReceiver(userid,currentUserId)
        if all_msg:
            qs_json = json.dumps(all_msg)
        else:
            qs_json = json.dumps({})
        return HttpResponse(qs_json, content_type='application/json')

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def room_message(request,roomid):
    if ChatRooms.isRoomExist(roomid) and request.method == "POST":
        room = ChatRooms.getChatRoomDatabyId(roomid)

        if request.POST["roompass"] == room['password']:
            currentUserId = sessionCtl.getCurrentUserId(request)
            sessionCtl.setReceiverSession(request,roomid)
            Chatlist.save_chatlist(roomid, currentUserId)
            all_msg = {}
            thisuser = {}
            thischat = {}
            groupchat = GroupChats.getAllChatsbyRoomid(roomid)
            users = Users.getUsers()
            for chat in groupchat:
                for user in users:
                    if user == groupchat[chat]['sender']:
                        thisuser = users[user]
                        thisuser['userid'] = user
                        thischat = groupchat[chat]
                        thischat['chatid'] = chat
                        all_msg[chat] = Merge(thisuser,thischat)

            last_msg = GroupChats.getLastMessage(roomid)
            if(not last_msg):
                last_msg = {}
            elif(last_msg['roomid'] == roomid):
                if not GroupChatSeenList.isUserSeenChat(roomid,last_msg['id'],currentUserId):
                    GroupChatSeenList.save_data(roomid,last_msg['id'],currentUserId,True)
                    GroupChats.updataSeenNum(last_msg['id'],last_msg['seennum']+1)

            num = Chatlist.getConnections(roomid)
            return render(request, 'room_message.html',{"room":room,"num":num,"msgs":all_msg,"last_msg":last_msg})

    return redirect('/main/ChatRooms/')

def room_message_interval(request,roomid):
    if ChatRooms.isRoomExist(roomid):
        if request.method == 'GET':
            room = ChatRooms.getChatRoomDatabyId(roomid)
            currentUserId = sessionCtl.getCurrentUserId(request)
            all_msg = {}
            thisuser = {}
            thischat = {}
            groupchat = GroupChats.getAllChatsbyRoomid(roomid)
            users = Users.getUsers()
            for chat in groupchat:
                for user in users:
                    if user == groupchat[chat]['sender']:
                        thisuser = users[user]
                        thisuser['userid'] = user
                        thischat = groupchat[chat]
                        thischat['chatid'] = chat
                        all_msg[chat] = Merge(thisuser,thischat)

            last_msg = GroupChats.getLastMessage(roomid)
            if(not last_msg):
                last_msg = {}
            elif(last_msg['roomid'] == roomid):
                if not GroupChatSeenList.isUserSeenChat(roomid,last_msg['id'],currentUserId):
                    GroupChatSeenList.save_data(roomid,last_msg['id'],currentUserId,True)
                    GroupChats.updataSeenNum(last_msg['id'],last_msg['seennum']+1)

            qs_json = json.dumps(all_msg)

            return HttpResponse(qs_json, content_type='application/json')

@csrf_exempt
def room_text_message(request,roomid):
    if ChatRooms.isRoomExist(roomid):
        if request.method == "POST":
            message = request.POST['message']
            if message !="":
                id = GroupChats.generate_id()
                receiver, sender = sessionCtl.getCurrentReceiverandSender(request)
                senttime = int(time.time() * 1000)
                sendername =sessionCtl.getCurrentUserName(request)
                GroupChats.save_chat(id, message, receiver, sender, sendername, senttime, "text")

        currentUserId = sessionCtl.getCurrentUserId(request)
        all_msg = {}
        thisuser = {}
        thischat = {}
        groupchat = GroupChats.getAllChatsbyRoomid(roomid)
        users = Users.getUsers()
        for chat in groupchat:
            for user in users:
                if user == groupchat[chat]['sender']:
                    thisuser = users[user]
                    thisuser['userid'] = user
                    thischat = groupchat[chat]
                    thischat['chatid'] = chat
                    all_msg[chat] = Merge(thisuser,thischat)

        last_msg = GroupChats.getLastMessage(roomid)
        if(not last_msg):
            last_msg = {}
        elif(last_msg['roomid'] == roomid):
            if not GroupChatSeenList.isUserSeenChat(roomid,last_msg['id'],currentUserId):
                GroupChatSeenList.save_data(roomid,last_msg['id'],currentUserId,True)
                GroupChats.updataSeenNum(last_msg['id'],last_msg['seennum']+1)


        qs_json = json.dumps(all_msg)
        return HttpResponse(qs_json, content_type='application/json')

def room_image_message(request,roomid):
    if request.method == "POST":
        file = request.FILES.get('upload', False)
        if(file):
            file_extension = ['png' , 'jpg', 'jpeg']
            if file.name.split(".")[-1].lower() in file_extension:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                #uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url

                imageURL = Chats.uploadImage(uploaded_file_url)
                id = GroupChats.generate_id()
                receiver, sender = sessionCtl.getCurrentReceiverandSender(request)
                senttime = int(time.time() * 1000)
                sendername =sessionCtl.getCurrentUserName(request)
                GroupChats.save_chat(id, imageURL, receiver, sender, sendername, senttime, "image")
                os.remove(uploaded_file_url)
    return redirect('/main/ChatRooms/'+roomid)

def room_setting(request,roomid):
    if ChatRooms.isRoomExist(roomid):
        room = ChatRooms.getChatRoomDatabyId(roomid)
        chatlist = Chatlist.getChatlistbyId(roomid)
        currentUserId = sessionCtl.getCurrentUserId(request)
        users = Users.getUsers()
        for user in users.copy():
            if user == currentUserId:
                users.pop(user)
        room_user = {}
        thisuser = {}
        thischat = {}
        for chat in chatlist:
            for user in users:
                if user == chatlist[chat]['id']:
                    thisuser = users[user]
                    thischat = chatlist[chat]
                    room_user[chat] = Merge(thisuser,thischat)
        return render(request, 'roomsetting.html',{"room":room,"users":room_user})
    return redirect('/main/ChatRooms/'+roomid)

def room_setting_image(request,roomid):
    if ChatRooms.isRoomExist(roomid):
        file = request.FILES.get('upload', False)
        if(file):
            file_extension = ['png' , 'jpg', 'jpeg']
            if file.name.split(".")[-1].lower() in file_extension:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                #uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url
                imageURL = ChatRooms.uploadImage(uploaded_file_url)

                ChatRooms.update_RoomImg(roomid,imageURL)
                os.remove(uploaded_file_url)

    return redirect('/main/ChatRooms/'+roomid+'/setting/')

def room_setting_edit(request,roomid):
    if ChatRooms.isRoomExist(roomid):
        if request.method == "POST":
            roomname = request.POST['roomname']
            roompass = request.POST['roompass']
            if(roompass == ""):
                ChatRooms.update_Room(roomid, roomname, roompass, "not_secret")
            else:
                ChatRooms.update_Room(roomid, roomname, roompass, "secret")

    return redirect('/main/ChatRooms/'+roomid+'/setting/')

def room_setting_chat(request,roomid,userid):
    if Users.isUserExist(userid):
        return redirect("/main/Users/"+userid)
    return redirect('/main/ChatRooms/'+roomid+'/setting/')
