import mysql.connector
from mysql.connector import Error
from datetime import datetime, timezone

async def createTables():
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = """
        CREATE TABLE IF NOT EXISTS Users(
            id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255)
        );
        CREATE TABLE IF NOT EXISTS Channels(
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS Messages(
            id VARCHAR(255) PRIMARY KEY,
            content TEXT,
            user_id VARCHAR(255),
            channel_id VARCHAR(255),
            created_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (channel_id) REFERENCES Channels(id)
        );"""

    try:
        c = mydb.cursor()
        c.execute(query)
        print('Tables cree avec succes!')
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

async def insertUser(id, username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = f"INSERT INTO Users(id, username) VALUES ('{id}', '{username}');"
    try:
        c = mydb.cursor()
        c.execute(query)
        mydb.commit()
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

async def insertChannel(id, name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = f"INSERT INTO Channels(id, name) VALUES ('{id}', '{name}');"
    try:
        c = mydb.cursor()
        c.execute(query)
        mydb.commit()
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

def getTimestamp(d):
    return d.astimezone(timezone.utc).timestamp()

async def insertMessage(id, content, user_id, channel_id, created_at):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = f"INSERT INTO Messages(id, content, user_id, channel_id, created_at) VALUES ('{id}', '{content}', '{user_id}', '{channel_id}', FROM_UNIXTIME({getTimestamp(created_at)}));"
    try:
        c = mydb.cursor()
        c.execute(query)
        mydb.commit()
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

async def getLastNMessages(n, username):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = f"""
        SELECT
            m.content,
            u.username,
            m.created_at
        FROM
            Messages m
        JOIN
            Users u ON m.user_id = u.id
        WHERE
            u.username = '{username}'
        ORDER BY
            m.created_at DESC
        LIMIT {n};
    """
    try:
        c = mydb.cursor()
        c.execute(query)
        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

async def getLastNMessagesChannel(n, channel_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="ouss",
        password="ouss",
        database="discord"
    )
    query = f"""
        SELECT
            m.content,
            u.username,
            m.created_at
        FROM
            Messages m
        JOIN
            Users u ON m.user_id = u.id
        JOIN
            Channels c ON m.channel_id = c.id
        WHERE
            c.id = '{channel_id}'
        ORDER BY
            m.created_at DESC
        LIMIT {n};
    """
    try:
        c = mydb.cursor()
        c.execute(query)
        rows = c.fetchall()
        
        return rows
    except Error as e:
        print(e)
    finally:
        c.close()
        mydb.close()

    