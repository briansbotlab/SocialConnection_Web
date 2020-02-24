from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from SocialConnection import settings
from . import pyrebase_settings
from . import sessionCtl
from .model import Users, Chatlist, Chats, ChatRooms, GroupChats
import time
import json
import os


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
            sessionCtl.setLoginSession(request,username,user['localId'],email)
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
            sessionCtl.setLoginSession(request,userData['username'],user['localId'],email)
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
                lastMessage = Chats.getLastMessage(currentUserId,user)
                if lastMessage:
                    data.update(lastMessage)
                userData[user] = data

        for chatroom in allChatrooms:
            if chatroom in current_chatlist:
                data = allChatrooms[chatroom]
                lastMessage = GroupChats.getLastMessage(chatroom)
                if lastMessage:
                    data.update(lastMessage)
                chatroomData[chatroom] = data

        return render(request, 'fragment/chats.html',{"users":userData,"rooms":chatroomData})

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
    return redirect('/main/ChatRooms')



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
        sessionCtl.updateUsername(request,username)

        if(file):
            file_extension = ['png' , 'jpg', 'jpeg']
            if file.name.split(".")[-1].lower() in file_extension:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                uploaded_file_url = fs.url(filename)
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")

                imageURL = Users.uploadImage(uploaded_file_url)
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
    return render(request, 'home.html')

def message(request,userid):
    if Users.isUserExist(userid):
        user = Users.getUserDatabyId(userid)
        currentUserId = sessionCtl.getCurrentUserId(request)
        sessionCtl.setReceiverSession(request,userid)
        all_msg = Chats.getAllChatsbySenserAndReceiver(userid,currentUserId)
        last_msg = Chats.getLastMessage(currentUserId,userid)
        if(last_msg['sender'] == userid):
            Chats.seenMessage(last_msg['id'])
        return render(request, 'message.html',{"user":user,"msgs":all_msg,"last_msg":last_msg})
    else:
        return redirect('/main/Users')

def message_interval(request,userid):
    if Users.isUserExist(userid):
        if request.method == 'GET':
            currentUserId = sessionCtl.getCurrentUserId(request)
            last_msg = Chats.getLastMessage(currentUserId,userid)
            if(last_msg['sender'] == userid):
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
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")

                imageURL = Chats.uploadImage(uploaded_file_url)
                id = Chats.generate_id()
                receiver, sender = sessionCtl.getCurrentReceiverandSender(request)
                senttime = int(time.time() * 1000)
                Chats.save_chat(id, False, imageURL, receiver, sender, senttime, "image")
                os.remove(uploaded_file_url)
    return redirect('/main/Users/'+userid)


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
    return redirect('/main/Users/'+userid)
