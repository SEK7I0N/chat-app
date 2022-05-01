"""Main Module"""

import sqlite3
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import AuthHandler
from controller.group_controller import (add_user_to_a_group, check_group,
                                         setup_group)
from controller.message_controller import write_message
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
def register_user(user_details: UserSchema):
    """Register a new user"""
    if check_user(user_details):
        raise HTTPException(status_code=400, detail="Username/Email already exists")
    try:
        user_details.password = auth_handler.get_password_hash(user_details.password)
        user_details.created_at = datetime.now(timezone.utc)
        setup_user(user_details)
        return {"message": "User created"}
    except sqlite3.IntegrityError as sql_exception:
        raise HTTPException(
            status_code=400, 
            detail=f"Exception occurred user not created : {sql_exception}"
            ) from sql_exception

@app.put('/create_or_edit_user',dependencies=[Depends(auth_handler.auth_wrapper)],tags=['User'])
def edit_user(user_details: UserSchema):
    """Edit an existing user"""
    if not check_user(user_details):
        raise HTTPException(status_code=400, detail="User doesn't exist")
    print(user_details)
    user_details.password = auth_handler.get_password_hash(user_details.password)
    user_details.created_at = datetime.now(timezone.utc)
    return setup_user(user_details , update=True)

@app.post('/login', tags=['Users'])
def login(login_details: LoginSchema):
    """Login a user"""
    hashed_password = validate_login(login_details=login_details)
    if (hashed_password is None) or (not auth_handler.verify_password(password=login_details.password,hashed_password=hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    print(f'this is hashed pass {login_details.password} ')
    token = auth_handler.encode_token(login_details.username)
    return { 'token': token }

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    """Protected endpoint"""
    return { 'name': username }


@app.get('/unprotected')
def unprotected():
    """Unprotected endpoint"""
    return {'message': 'Hello World'}




@app.post('/post_message',dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Messages'])
def post_message(message_details: MessageSchema):
    """Protected endpoint"""
    message_details.created_at = datetime.now(timezone.utc)
    write_message(message_details=message_details)
    return { 'message': message_details  }


@app.post('/create_or_edit_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
def create_group(group_details: GroupSchema):
    """Create a group"""
    group_details.created_at = datetime.now(timezone.utc)
    if check_group(group_details):
        raise HTTPException(status_code=400, detail="group already exists")
    setup_group(group_details=group_details)
    return { 'group_details': group_details }

@app.put('/create_or_edit_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
def edit_group(group_details: GroupSchema):
    """Create a group"""
    group_details.created_at = datetime.now(timezone.utc)
    if not check_group(group_details):
        raise HTTPException(status_code=400, detail="group already exists")
    setup_group(group_details=group_details,update=True)
    return { 'group_details': group_details }



@app.post('/add_user_to_group', dependencies=[Depends(auth_handler.auth_wrapper)], tags=['Group'])
def add_user_to_group(group_details: GroupSchema):
    """Create a group"""
    group_details.created_at = datetime.now(timezone.utc)
    add_user_to_a_group(group_details=group_details)
    return { 'group_details': group_details }


@app.websocket("/post_message")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint"""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)
