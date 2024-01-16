from flask import request
from flask_socketio import emit

from .extensions import socketio

users = {}
user_count = 0  # Counter for assigning user IDs

@socketio.on("connect")
def handle_connect():
    global user_count
    user_count += 1
    users[request.sid] = {"user_id": user_count}

    # Automatically send a welcome message to the new user
    emit("chat", {"message": f"Welcome! You are user {user_count}", "username": "CONNECTED"}, room=request.sid)

@socketio.on("new_message")
def handle_new_message(message):
    username = "User" + str(users[request.sid]["user_id"])
    emit("chat", {"message": message, "username": username}, broadcast=True)

def get_username(sid):
    # Implement logic to retrieve or generate a unique username for the given sid
    return f"\nUser{users[sid]['user_id']}"

@socketio.on("file_shared")
def handle_file_shared(data):
    username = get_username(request.sid)
    emit("file_shared", {"username": username, "fileName": data["fileName"], "fileContent": data["fileContent"]}, broadcast=True)

