"""User Controller"""
import sqlite3
from datetime import datetime, timezone

from db.database import connect_database
from model.messages import MessageSchema

from controller.group_controller import fetch_group_id
from controller.user_controller import fetch_user_id_from_login


def write_message(message_details: MessageSchema):
    """Write message"""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        message_details.sender_id = fetch_user_id_from_login(
            cursor=cursor,username=message_details.sender)
        message_details.group_id = fetch_group_id(cursor=cursor, group_name=message_details.group)
        insert_messages(cursor=cursor, message_details=message_details)
        conn.commit()
    finally:
        cursor.close()
        conn.close()



def insert_messages(cursor: sqlite3.Cursor,message_details: MessageSchema):
    """Insert messages"""
    cursor.execute(
        f"""INSERT INTO messages (group_id, message, sender_ID, message_timestamp)
        VALUES
        ({message_details.group_id},'{message_details.content}',
        {message_details.sender_id},'{datetime.now(timezone.utc)}');"""
    )
    return cursor.fetchall()
