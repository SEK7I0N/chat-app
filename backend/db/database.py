""" Module to create a database and tables """

import logging
import sqlite3

# CONTANTS
DATABASE_NAME = 'chat_app'
USERS = [
    {'ID': 1, 'NAME': 'John', 'AGE': 20, 'ADDRESS': 'USA', 'EMAIL': 'something@something','CREATED_TIMESTAMP': '2020-01-01 00:00:00', 'PHONE_NUMBER': '1234567890'},
    {'ID': 2, 'NAME': 'Jane', 'AGE': 21, 'ADDRESS': 'UK', 'EMAIL': 'something@something','CREATED_TIMESTAMP': '2020-01-01 00:00:00', 'PHONE_NUMBER': '1234567890'},
    {'ID': 3, 'NAME': 'Jack', 'AGE': 22, 'ADDRESS': 'USA', 'EMAIL': 'something@something','CREATED_TIMESTAMP': '2020-01-01 00:00:00', 'PHONE_NUMBER': '1234567890'},
    {'ID': 4, 'NAME': 'Jill', 'AGE': 23, 'ADDRESS': 'UK', 'EMAIL': 'something@something','CREATED_TIMESTAMP': '2020-01-01 00:00:00', 'PHONE_NUMBER': '1234567890'},
    {'ID': 5, 'NAME': 'John', 'AGE': 20, 'ADDRESS': 'USA', 'EMAIL': 'something@something','CREATED_TIMESTAMP': '2020-01-01 00:00:00', 'PHONE_NUMBER': '1234567890'}
]

def connect_database(database_name):
    """Connects to the database"""
    return sqlite3.connect(f'{database_name}.db')


def create_database(database_name):
    """Creates a database"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    print(f'Database {database_name} created')
    logging.info('Database %s created', DATABASE_NAME)
    database.close()


def create_user_table(database_name):
    """Creates a USERS table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(500),
            EMAIL          CHAR(500) NOT NULL,
            CREATED_TIMESTAMP           DATETIME NOT NULL,
            PHONE_NUMBER DECIMAL(10,0) NOT NULL);''')
    print('Table USERS created')
    logging.info('Table USERS created')
    cursor.close()
    database.close()


def create_role_table(database_name):
    """Creates a ROLES table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ROLES
            (ID INT PRIMARY KEY     NOT NULL,
            ROLE           TEXT    NOT NULL);''')
    print('Table ROLES created')
    logging.info('Table ROLES created')
    cursor.close()
    database.close()


def create_user_role_table(database_name):
    """Creates a USER_ROLES table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS USER_ROLES
            (ID INT PRIMARY KEY     NOT NULL,
            USER_ID           INT    NOT NULL ,
            ROLE_ID           INT    NOT NULL,
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
            FOREIGN KEY (ROLE_ID) REFERENCES ROLES(ID));''')
    print('Table USER_ROLES created')
    logging.info('Table USER_ROLES created')
    cursor.close()
    database.close()


def create_login_table(database_name):
    """Creates a LOGIN table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS LOGIN
            (ID INT PRIMARY KEY     NOT NULL,
            USER_ID           INT    NOT NULL,
            USERNAME       CHAR(500),
            PASSWORD       CHAR(1500),
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID));''')
    print('Table LOGIN created')
    logging.info('Table LOGIN created')
    cursor.close()
    database.close()


def create_chat_room_table(database_name):
    """Creates a CHAT_ROOMS table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS CHAT_ROOMS
            (ID INT PRIMARY KEY     NOT NULL,
            ROOM_NAME           CHAR(500) NOT NULL,
            CREATED_TIMESTAMP           DATETIME NOT NULL);''')
    print('Table CHAT_ROOMS created')
    logging.info('Table CHAT_ROOMS created')
    cursor.close()
    database.close()


def create_message_table(database_name):
    """Creates a MESSAGES table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGES
            (ID INT PRIMARY KEY     NOT NULL,
            CHAT_ROOM_ID           INT    NOT NULL ,
            MESSAGE           CHAR(2500),
            SENDER_ID           INT    NOT NULL,
            MESSAGE_TIMESTAMP           DATETIME NOT NULL,
            FOREIGN KEY (CHAT_ROOM_ID) REFERENCES CHAT_ROOMS(ID),
            FOREIGN KEY (SENDER_ID) REFERENCES USERS(ID));''')
    print('Table MESSAGES created')
    logging.info('Table MESSAGES created')
    cursor.close()
    database.close()


def populate_users(database_name):
    """Populates the USERS table"""
    database = sqlite3.connect(f'backend/{database_name}.db')
    cursor = database.cursor()
    for user in USERS:
        cursor.execute('''INSERT INTO USERS (ID, NAME, AGE, ADDRESS, EMAIL, CREATED_TIMESTAMP, PHONE_NUMBER)
            VALUES (?, ?, ?, ?, ?, ?, ?)''', (user['ID'], user['NAME'], user['AGE'], user['ADDRESS'], user['EMAIL'], user['CREATED_TIMESTAMP'], user['PHONE_NUMBER']))
    print('Table USERS populated')
    logging.info('Table USERS populated')
    cursor.close()
    database.commit()
    database.close()


def main():
    """Main function"""
    create_database(DATABASE_NAME)
    create_user_table(DATABASE_NAME)
    create_role_table(DATABASE_NAME)
    create_user_role_table(DATABASE_NAME)
    create_login_table(DATABASE_NAME)
    create_chat_room_table(DATABASE_NAME)
    create_message_table(DATABASE_NAME)
    populate_users(DATABASE_NAME)

if __name__ == '__main__':
    main()
