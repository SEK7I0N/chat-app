<img src="/src/chatter-io.png" alt="Chatter-io Logo" style=" display: block;margin-left: auto; margin-right: auto; width: 50%;"/>

# Chatter.io

## Table of Contents


  - [About <a name = "about">Chatter.io</a>](#about-chatterio) 
  - [Prerequisites <a name = "Prerequisites"></a>](#prerequisites-)
  - [Getting Started <a name = "getting_started"></a>](#getting-started-)
  - [Database <a name = "database"></a>](#database-)

#### About <a name = "about"></a>

The goal of this project is to make a chatting platform which can connect users and the topics in they are interested in all while providing a seamless experience between various platforms and with different means of communication.

#### Prerequisites <a name = "Prerequisites"></a>

You will require at least python 3.10 to run the app as intended. If you have the python version install then use this command to install the dependency for your system.

```
$~> cd backend
$~> pip install --upgrade -r requirements.txt
```

The `pip install` command will upgrade the local pip and install the required libraries which are required for this application to run properly

#### Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```
$~> cd backend
$~> uvicorn main:app --reload (run with reload tag in case you want to run in development mode)
```
The `uvicorn main:app` command will start the backend server for the application.

#### Database <a name = "database"></a>

This is the ER Diagram for this application

<img src="/src/er_diagram.png" alt="ER diagram for chatter-io database" style=" display: block;margin-left: auto; margin-right: auto;"/>

There are few pointer in for this diagram.

  - I think it would have been better to save the username and password(hashed) in the users table insted of the login. My intention was to have login table which holds when the user had logged in (like a last login feature with all history)
- For current use case I chose to go with SQLite DB but for future it would be better to have a mix of different db like mongoDB for storing message for other details. While maintaining the user groups relationship in a RDBMs like PostgreSQL/ SQLServer