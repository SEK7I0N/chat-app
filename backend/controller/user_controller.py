"""User Controller"""
import logging
import sqlite3

from db.database import connect_database
from model.users import LoginSchema, UserSchema


def check_user(user_details : UserSchema):
    """Check if the user exists"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        user_login = fetch_user_id_from_login(cursor=cursor,username=user_details.username)
        user_email = fetch_user_id(cursor=cursor, user_email=user_details.email)
        if user_login is None and user_email is None:
            return False
        return True
    finally:
        cursor.close()
        conn.close()


def setup_user(user_details : UserSchema, update:bool = False):
    """Create a new user"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        if not update:
            create_user(cursor=cursor, user_details=user_details)
            user_id = fetch_user_id(cursor=cursor, user_email=user_details.email)
            create_login(cursor=cursor, user_id=user_id, user_details=user_details)
            role_id = fetch_role_id(cursor=cursor, role=user_details.role)
            create_user_role_link(cursor=cursor, user_id=user_id, role_id=role_id)
        else:
            user_id = fetch_user_id(cursor=cursor, user_email=user_details.email)
            update_user_details(cursor=cursor, user_id=user_id, user_details=user_details)
            update_login_details(cursor=cursor, user_details=user_details)
            role_id = fetch_role_id(cursor=cursor, role=user_details.role)
            update_user_role_link(cursor=cursor, user_id=user_id, role_id=role_id)
        conn.commit()
        logging.info('User %s created/updated', user_details.username)
    finally:
        cursor.close()
        conn.close()



def validate_login(login_details: LoginSchema):
    """validate users login details"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        return fetch_login_pass(cursor=cursor,login_details=login_details)
    finally:
        cursor.close()
        conn.close()


def get_user_details(login_details: LoginSchema):
    """validate users login details"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        return fetch_login_pass(cursor=cursor,login_details=login_details)
    finally:
        cursor.close()
        conn.close()


def fetch_role_id(cursor:sqlite3.Cursor, role:str):
    """fetch role id"""
    cursor.execute(
        f"SELECT ID FROM roles WHERE role = '{role}'"
    )
    return cursor.fetchone()[0]

def fetch_user_id(cursor:sqlite3.Cursor, user_email:str):
    """fetch user id"""
    cursor.execute(
        f"Select ID from users where email = '{user_email}'"
    )
    user_id = cursor.fetchone()
    if user_id is None:
        return None
    return user_id[0]

def fetch_user_id_from_login(cursor:sqlite3.Cursor, username:str|None):
    """fetch user id"""
    cursor.execute(
        f"SELECT user_id from LOGIN where username = '{username}'"
    )
    user_id = cursor.fetchone()
    if user_id is None:
        return None
    return user_id[0]

def fetch_login_pass(cursor:sqlite3.Cursor, login_details:LoginSchema):
    """Fetch Login Details"""
    cursor.execute(
        f"SELECT password FROM login WHERE username = '{login_details.username}'"
    )
    login_id = cursor.fetchone()
    if login_id is None:
        return None
    return login_id[0]

def fetch_user_details(cursor:sqlite3.Cursor, login_details:LoginSchema):
    """Fetch Login Details"""
    cursor.execute(
        f"SELECT * FROM USER WHERE username = '{login_details.username}'"
    )
    user_details = cursor.fetchone()
    if user_details is None:
        return None
    return user_details[0]

def create_user(cursor:sqlite3.Cursor, user_details : UserSchema):
    """Insert user details in database"""
    cursor.execute(
        f"""INSERT INTO users (name, age, address, email, phone_number, created_timestamp)
        VALUES
        ('{user_details.name}', '{user_details.age}', '{user_details.address}',
        '{user_details.email}', '{user_details.phone}', '{user_details.created_at}')"""
    )
    return cursor.fetchall()

def create_login(cursor:sqlite3.Cursor, user_id : int, user_details : UserSchema):
    """Insert login details in database"""
    cursor.execute(
        f"""INSERT into LOGIN (user_id, username, password)
        values
        ({user_id}, "{user_details.username}", "{user_details.password}")"""
        )
    return cursor.fetchall()

def create_user_role_link(cursor:sqlite3.Cursor, user_id, role_id):
    """Insert role details"""
    cursor.execute(
        f"Insert into user_roles (user_id, role_id) values ({user_id}, '{role_id}')"
    )
    return cursor.fetchall()

def update_user_details(cursor:sqlite3.Cursor, user_id: int, user_details : UserSchema):
    """Insert user details in database"""
    cursor.execute(
        f"""UPDATE users
        SET
        name = '{user_details.name}', age = '{user_details.age}',
        address ='{user_details.address}', email = '{user_details.email}',
        phone_number='{user_details.phone}'
        WHERE ID = '{user_id}'"""
    )
    return cursor.fetchall()


def update_login_details(cursor:sqlite3.Cursor,  user_details : UserSchema):
    """update login details in database"""
    cursor.execute(
        f"""UPDATE login
        SET  password = '{user_details.password}'
        WHERE username = '{user_details.username}'"""
        )
    return cursor.fetchall()

def update_user_role_link(cursor:sqlite3.Cursor, user_id, role_id):
    """update user_role details"""
    cursor.execute(
        f"""UPDATE user_roles
        SET role_id={role_id}
        WHERE user_id = {user_id}"""
    )
    return cursor.fetchall()
