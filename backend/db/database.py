""" Module to create a database and tables """

import logging
import sqlite3

# DATABASE_NAME = 'backend/chat_app'
DATABASE_NAME = 'chat_app'

def connect_database(database_name = DATABASE_NAME):
    """Connects to the database"""
    return sqlite3.connect(f'{database_name}.db',timeout=10)


def create_database(database_name):
    """Creates a database"""
    database = connect_database()
    print(f'Database {database_name} created')
    logging.info('Database %s created', DATABASE_NAME)
    database.close()


def create_user_table():
    """Creates a USERS table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS
            (ID INTEGER PRIMARY KEY,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(500),
            EMAIL          CHAR(500) NOT NULL UNIQUE,
            CREATED_TIMESTAMP           DATETIME NOT NULL,
            PHONE_NUMBER DECIMAL(10,0) NOT NULL);''')
    print('Table USERS created')
    logging.info('Table USERS created')
    cursor.close()
    database.close()


def create_role_table():
    """Creates a ROLES table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ROLES
            (ID INTEGER PRIMARY KEY,
            ROLE           TEXT    NOT NULL);''')
    print('Table ROLES created')
    logging.info('Table ROLES created')
    cursor.close()
    database.close()


def create_user_role_table():
    """Creates a USER_ROLES table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS USER_ROLES
            (
            USER_ID           INT    NOT NULL ,
            ROLE_ID           INT    NOT NULL,
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
            FOREIGN KEY (ROLE_ID) REFERENCES ROLES(ID),
            UNIQUE(USER_ID, ROLE_ID) ON CONFLICT REPLACE);''')
    print('Table USER_ROLES created')
    logging.info('Table USER_ROLES created')
    cursor.close()
    database.close()


def create_login_table():
    """Creates a LOGIN table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS LOGIN
            (ID INTEGER PRIMARY KEY,
            USER_ID           INT    NOT NULL,
            USERNAME       CHAR(500) UNIQUE,
            PASSWORD       CHAR(5000),
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID));''')
    print('Table LOGIN created')
    logging.info('Table LOGIN created')
    cursor.close()
    database.close()


def create_group_table():
    """Creates a user group table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS GROUPS
            (ID INTEGER PRIMARY KEY,
            GROUP_NAME           CHAR(500) NOT NULL UNIQUE,
            CREATED_AT           DATETIME NOT NULL,
            CREATED_BY           INT    NOT NULL,
            FOREIGN KEY (CREATED_BY) REFERENCES USERS(ID));''')
    print('Table GROUPS created')
    logging.info('Table GROUPS created')
    cursor.close()
    database.close()

def create_user_group_table():
    """Creates a user group table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS USER_GROUPS
            (ID INTEGER PRIMARY KEY,
            GROUP_ID           INT    NOT NULL ,
            USER_ID           INT    NOT NULL,
            USER_TIMESTAMP           DATETIME NOT NULL,
            FOREIGN KEY (GROUP_ID) REFERENCES GROUPS(ID),
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
            UNIQUE(GROUP_ID,USER_ID) ON CONFLICT REPLACE);''')
    print('Table USER_GROUPS created')
    logging.info('Table USER_GROUPS created')
    cursor.close()
    database.close()

def create_message_table():
    """Creates a MESSAGES table"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGES
            (ID INTEGER PRIMARY KEY,
            GROUP_ID           INT    NOT NULL ,
            MESSAGE           CHAR(2500),
            SENDER_ID           INT    NOT NULL,
            MESSAGE_TIMESTAMP           DATETIME NOT NULL,
            FOREIGN KEY (GROUP_ID) REFERENCES GROUPS(ID),
            FOREIGN KEY (SENDER_ID) REFERENCES USERS(ID));''')
    print('Table MESSAGES created')
    logging.info('Table MESSAGES created')
    cursor.close()
    database.close()



def populate_tables():
    """insert values to db"""
    database = connect_database()
    cursor = database.cursor()
    cursor.execute(
        '''INSERT INTO ROLES (ROLE) VALUES ('ADMIN'),('NORMAL USER')'''
    )
    # cursor.execute(
    #     f"""INSERT INTO GROUPS (group_name,created_at)
    #     VALUES
    #     ('Web','{datetime.now(timezone.utc)}'),
    #     ('Fire','{datetime.now(timezone.utc)}'),
    #     ('Contra','{datetime.now(timezone.utc)}');"""
    # )
    database.commit()
    cursor.close()
    database.close()
    print('Tables populated')
    logging.info('Tables populated')

def main():
    """Main function"""
    create_database(DATABASE_NAME)
    create_user_table()
    create_role_table()
    create_user_role_table()
    create_login_table()
    create_group_table()
    create_user_group_table()
    create_message_table()
    populate_tables()

if __name__ == '__main__':
    main()
