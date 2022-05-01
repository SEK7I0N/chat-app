"""Main Module"""

import sqlite3
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import AuthHandler
from controller.group_controller import (add_user_to_a_group, check_group,
                                         check_user_group, delete_a_group,
                                         get_users_for_group, setup_group)
from controller.message_controller import (get_all_message_for_group,
                                           write_message)
from controller.user_controller import check_user, setup_user, validate_login
from model.group import GroupSchema
from model.messages import MessageSchema
from model.users import LoginSchema, UserSchema

# from utils.system_path import setup_path

# setup_path()
app = FastAPI()

orgins =['*']

app.add_middleware(middleware_class=CORSMiddleware,
                allow_origins=orgins,
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*'])

auth_handler = AuthHandler()

@app.post('/create_or_edit_user',tags=['User'])
async def register_user(user_details: UserSchema):
    """Register a new user"""
    if check_user(user_details):
        raise HTTPException(status_code=400, detail="Username/Email already exists")
    try:
        user_details.password = auth_handler.get_password_hash(user_details.password)
        user_details.created_at = datetime.now(timezone.utc)
        setup_user(user_details)
        return {"details": "User created"}
    except sqlite3.IntegrityError as sql_exception:
        raise HTTPException(
            status_code=400,
            detail=f"Exception occurred user not created : {sql_exception}"
            ) from sql_exception

@app.put('/create_or_edit_user',dependencies=[Depends(auth_handler.auth_wrapper)],tags=['User'])
async def edit_user(user_details: UserSchema):
    """Edit an existing user"""
    if not check_user(user_details):
        raise HTTPException(status_code=400, detail="User doesn't exist")
    user_details.password = auth_handler.get_password_hash(user_details.password)
    user_details.created_at = datetime.now(timezone.utc)
    setup_user(user_details,update=True)
    return {"details": "User updated"}

@app.post('/login', tags=['User'])
async def login(login_details: LoginSchema):
    """Login a user"""
    hashed_password = validate_login(login_details=login_details)
    if (hashed_password is None) or (not auth_handler.verify_password(
        password=login_details.password,hashed_password=hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(login_details.username)
    return { 'access token': token }


@app.post('/logout', tags=['User'])
async def logout(login_details: LoginSchema):
    """Logout a user"""
    hashed_password = validate_login(login_details=login_details)
    if (hashed_password is None) or (not auth_handler.verify_password(
        password=login_details.password,hashed_password=hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(username=login_details.username,exp=timedelta(microseconds=1))
    return { 'access token': token }

@app.post('/post_message',dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Messages'])
async def post_message(message_details: MessageSchema):
    """Protected endpoint"""
    message_details.created_at = datetime.now(timezone.utc)
    write_message(message_details=message_details)
    return { 'details': 'Message posted'  }


@app.get('/view_all_message',dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Messages'])
async def view_all_message(group: str):
    """Protected endpoint"""
    messages = get_all_message_for_group(group=group)
    return { 'details': messages  }

@app.post('/create_or_edit_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
async def create_group(group_details: GroupSchema):
    """Create a group"""
    group_details.created_at = datetime.now(timezone.utc)
    if check_group(group_details):
        raise HTTPException(status_code=400, detail="group already exists")
    status = setup_group(group_details=group_details)
    return {
        "name":group_details.name,
        "group":group_details.user,
        "created_at":group_details.created_at,
        "status": "group created" if status else "group not updated"
    }

@app.put('/create_or_edit_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
async def edit_group(group_details: GroupSchema):
    """Create a group"""
    group_details.created_at = datetime.now(timezone.utc)
    if not check_group(group_details):
        raise HTTPException(status_code=400, detail="group doesn't exists")
    status = setup_group(group_details=group_details,update=True)
    return {
        "name":group_details.name,
        "group":group_details.user,
        "created_at":group_details.created_at,
        "status": f"{group_details.name} group updated" if status else f"{group_details.name} group not updated"
    }



@app.post('/add_user_to_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
async def add_user_to_group(group_details: GroupSchema):
    """Create a group"""
    if not check_user_group(group_details):
        raise HTTPException(status_code=400, detail=f"user: {group_details.user} already part of group: {group_details.name}")
    status = setup_group(group_details=group_details,update=True)
    group_details.created_at = datetime.now(timezone.utc)
    add_user_to_a_group(group_details=group_details)
    return {
        "name":group_details.name,
        "group":group_details.user,
        "created_at":group_details.created_at,
        "status": f"user: {group_details.user} added in group: {group_details.name}" if status else f"user: {group_details.user} already part of group: {group_details.name}"
    }

@app.delete('/delete_a_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
async def delete_group(group_details:GroupSchema):
    """delete a group"""
    delete_a_group(group_details=group_details)
    return {'details': 'group deleted'}

@app.get('/view_users_in_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
async def get_user_group_details(group_details:GroupSchema):
    """get user group details"""
    users = get_users_for_group(group_details=group_details)
    return {'details': users}

@app.websocket("/post_message")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint"""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
