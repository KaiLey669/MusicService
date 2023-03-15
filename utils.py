import sqlite3
from sqlite3 import Error


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('music_service.sqlite')
    except Error as e:
        print(f"The connection error '{e}' occured")

    return connection
