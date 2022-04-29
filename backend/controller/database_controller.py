"""Database Controller"""
import logging
import sqlite3

from db.database import DATABASE_NAME, connect_database
from model.users import UserDetails


def check_if_user_exists(user_details : UserDetails):
    """Check if the user is exists"""
    print(DATABASE_NAME)
    conn = connect_database(DATABASE_NAME)
    cursor = conn.cursor()
    print(f"SELECT * FROM USERS WHERE NAME = '{user_details.username}'")
    cursor.execute(f"SELECT * FROM USERS WHERE NAME = '{user_details.username}'")
    user = cursor.fetchone()
    print(f"cursor = {cursor}")
    print(f"user = {user}")
    cursor.close()
    conn.close()
    if user is None:
        return False
    return True

def create_user(user_details : UserDetails):
    """Create a new user"""
    conn = connect_database(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (id,name, age, address, email, phone_number, created_timestamp) VALUES ({user_details.id},'{user_details.name}', '{user_details.age}', '{user_details.address}', '{user_details.email}', '{user_details.phone}', '{user_details.created_timestamp}')"
    )
    cursor.execute(
        f"Select ID from users where email = '{user_details.email}'"
    )
    user_id = cursor.fetchone()
    cursor.execute(
        f"Insert into login (id, user_id, username, password) values ({user_details.id},{user_id[0]}, '{user_details.username}', '{user_details.password}')"
        )
    conn.commit()
    cursor.close()
    conn.close()
    logging.info('User %s created', user_details.username)
    return True
