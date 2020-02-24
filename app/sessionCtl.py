def setLoginSession(request,username,uid,email):
    request.session['uid'] = uid
    request.session['username'] = username
    request.session['email'] = email

def setReceiverSession(request,receiver):
    request.session['receiver'] = receiver

def delLoginSession(request):
    del request.session['uid']
    del request.session['username']
    del request.session['email']
    if isSessionExist(request,'receiver'):
        del request.session['receiver']

def getCurrentUserId(request):
    uid = request.session['uid']
    return uid

def updateUsername(request,username):
    request.session['username'] = username

def isSessionExist(request,sessionName):
    if sessionName in request.session:
        return True
    else:
        return False

def getCurrentReceiverandSender(request):
    receiver = request.session['receiver']
    sender = request.session['uid']
    return receiver, sender
