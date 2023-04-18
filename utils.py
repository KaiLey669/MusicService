import sqlite3
from sqlite3 import Error


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('music_service.sqlite')
    except Error as e:
        print(f"The connection error '{e}' occured")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred in read query")