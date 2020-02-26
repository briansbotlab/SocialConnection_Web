from .model import Users

def setLoginSession(request,username,uid,email,userImg):
    request.session['uid'] = uid
    request.session['username'] = username
    request.session['email'] = email
    request.session['userImg'] = userImg
    Users.user_login(uid)

def setReceiverSession(request,receiver):
    request.session['receiver'] = receiver

def delLoginSession(request):
    if isSessionExist(request,'uid'):
        Users.user_logout(request.session['uid'])
        del request.session['uid']
    if isSessionExist(request,'username'):
        del request.session['username']
    if isSessionExist(request,'email'):
        del request.session['email']
    if isSessionExist(request,'userImg'):
        del request.session['userImg']
    if isSessionExist(request,'receiver'):
        del request.session['receiver']


def getCurrentUserId(request):
    uid = request.session['uid']
    return uid

def getCurrentUserName(request):
    username = request.session['username']
    return username

def updateUsernameAndUserImg(request,username,userImg):
    request.session['username'] = username
    request.session['userImg'] = userImg

def isSessionExist(request,sessionName):
    if sessionName in request.session:
        return True
    else:
        return False

def getCurrentReceiverandSender(request):
    receiver = request.session['receiver']
    sender = request.session['uid']
    return receiver, sender
