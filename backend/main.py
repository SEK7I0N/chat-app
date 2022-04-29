"""Main Module"""

from fastapi import Depends, FastAPI, HTTPException

from auth.auth import AuthHandler
from controller.user_controller import check_user, setup_user
from model.users import LoginDetails, UserDetails
from utils.system_path import setup_path

setup_path()
app = FastAPI()

auth_handler = AuthHandler()

users = []


@app.post('/register')
def register(user_details: UserDetails):
    """Register a new user"""
    if check_user(user_details):
        raise HTTPException(status_code=400, detail="User already exists")
    user_details.password = auth_handler.get_password_hash(user_details.password)
    return setup_user(user_details)
    

@app.post('/login')
def login(login_details: LoginDetails):
    """Login a user"""
    user = next((x for x in users if x['username'] == login_details.username), None)
    if (user is None) or (not auth_handler.verify_password(login_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    """Protected endpoint"""
    return { 'name': username }


@app.get('/unprotected')
def unprotected():
    """Unprotected endpoint"""
    return {'message': 'Hello World'}
