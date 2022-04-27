"""213"""

import sqlite3

DATABASE_NAME = 'chat_app'

def create_database(database_name):
    """Creates a database"""
    database = sqlite3.connect(f'backend/db/{database_name}.db')
    print(f'Database {database_name} created')
    database.close()

def create_user_table(database_name):
    """Creates a user table"""
    database = sqlite3.connect(f'backend/db/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE USERS
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(500),
            EMAIL          CHAR(500),
            PASSWORD       CHAR(500),
            SALARY  INT);''')

def create_role_table(database_name):
    """Creates a user table"""
    database = sqlite3.connect(f'backend/db/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE ROLES
            (ID INT PRIMARY KEY     NOT NULL,
            ROLE           TEXT    NOT NULL);''')

def create_user_role_table(database_name):
    """Creates a user table"""
    database = sqlite3.connect(f'backend/db/{database_name}.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE USER_ROLES
            (ID INT PRIMARY KEY     NOT NULL,
            USER_ID           INT    NOT NULL ,
            ROLE_ID           INT    NOT NULL,
            FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
            FOREIGN KEY (ROLE_ID) REFERENCES ROLES(ID));''')

def main():
    """Main function"""
    create_database(DATABASE_NAME)
    create_user_table(DATABASE_NAME)
    create_role_table(DATABASE_NAME)
    create_user_role_table(DATABASE_NAME)

if __name__ == '__main__':
    main()
