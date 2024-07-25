from userSocket import socketio
from flask import request
from blocklist import all_login_users
from model import ConversationModel


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('add_current_user')
def handle_add_current_user(currentUser):
    all_login_users[request.sid] = currentUser['userId']
    myMessages = ConversationModel.query.filter(ConversationModel.receiverId == currentUser['userId'])
    socketio.emit('all_my_msg', {'messages': myMessages}, to=request.sid)


def handle_add_message(userId):
    if userId in all_login_users.values():
        requestID = [key for key, value in all_login_users.items() if value == userId][0]
        myMessages = ConversationModel.query.filter(ConversationModel.receiverId == userId)
        socketio.emit('all_my_msg', {'messages': myMessages}, to=requestID)


@socketio.on('disconnect')
def handle_remove_current_user():
    loggedOutUser = request.sid
    if loggedOutUser in all_login_users:
        all_login_users.pop(loggedOutUser)


@socketio.on('logout')
def handle_logout():
    loggedOutUser = request.sid
    if loggedOutUser in all_login_users:
        all_login_users.pop(loggedOutUser)
