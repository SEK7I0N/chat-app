"""User Controller"""
import sqlite3
from datetime import datetime, timezone

from db.database import connect_database
from model.group import GroupSchema

from controller.user_controller import fetch_user_id_from_login


def check_group(group_details : GroupSchema):
    """Check if the group exists"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        group = fetch_group_id(cursor=cursor,group_name=group_details.name)
        if group is None:
            return False
        return True
    finally:
        cursor.close()
        conn.close()


def check_user_group(group_details : GroupSchema):
    """Check if the user_group exists"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        group_id = fetch_group_id(cursor=cursor,group_name=group_details.name)
        user_id = fetch_user_id_from_login(cursor=cursor,username=group_details.user)
        user_group = fetch_user_group_details(cursor=cursor, user_id=user_id, group_id=group_id)
        if user_group is None:
            return False
        return True
    finally:
        cursor.close()
        conn.close()


def setup_group(group_details: GroupSchema, update:bool = False):
    """setup a new user or edit a current one"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        group_details.user_id = fetch_user_id_from_login(cursor=cursor,username=group_details.user)
        if not update:
            print('to be inserted')
            insert_group_details(cursor=cursor, group_details=group_details)
            group_details.group_id = fetch_group_id(cursor=cursor, group_name=group_details.name)
            insert_user_group_details(cursor=cursor, group_details=group_details)
        else:
            print('to be updated')
            group_details.group_id = fetch_group_id(cursor=cursor, group_name=group_details.name)
            update_group_details(cursor=cursor,group_details=group_details)
        print(f'group_details: {group_details}')
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_user_to_a_group(group_details: GroupSchema):
    """link user and group """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        group_details.user_id = fetch_user_id_from_login(cursor=cursor,username=group_details.user)
        group_details.group_id = fetch_group_id(cursor=cursor, group_name=group_details.name)
        insert_user_group_details(cursor=cursor, group_details=group_details)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def fetch_group_id(cursor:sqlite3.Cursor, group_name:str):
    """fetch group id"""
    cursor.execute(
        f"""SELECT ID FROM groups WHERE group_name = '{group_name}'"""
    )
    group_id = cursor.fetchone()
    print(f'group_id: {group_id}')
    if group_id is None:
        return None
    return group_id[0]

def fetch_user_group_details(cursor: sqlite3.Cursor, user_id:int, group_id:int):
    """fetch user group details"""
    cursor.execute(
        f"""SELECT * FROM user_groups WHERE user_id = {user_id} AND group_id = {group_id}"""
    )
    user_group = cursor.fetchone()
    if user_group is None:
        return None
    return user_group

def insert_group_details(cursor: sqlite3.Cursor, group_details: GroupSchema):
    """Insert messages"""
    cursor.execute(
        f"""INSERT INTO groups (group_name, created_at, created_by)
        VALUES
        ('{group_details.name}','{group_details.created_at}',{group_details.user_id})"""
    )
    return cursor.fetchall()


def insert_user_group_details(cursor: sqlite3.Cursor, group_details: GroupSchema):
    """Insert messages"""
    cursor.execute(
        f"""INSERT INTO user_groups (group_id, user_id, user_timestamp)
        VALUES
        ({group_details.group_id},{group_details.user_id},'{datetime.now(timezone.utc)}')"""
    )
    print(f'group_details: {group_details}')
    return cursor.fetchall()

def update_group_details(cursor: sqlite3.Cursor, group_details: GroupSchema):
    """Insert messages"""
    cursor.execute(
        f"""UPDATE groups
        SET group_name = '{group_details.name}'
        WHERE ID = {group_details.group_id}"""
    )
    return cursor.fetchall()
