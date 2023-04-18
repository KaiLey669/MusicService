from sqlite3 import Error
from utils import execute_query, execute_read_query


def insert_user(conn, login, pwd):
    query = f"""
        INSERT INTO user (user_name, user_login, user_password)
        VALUES ("{login}", "{login}", "{pwd}")
    """

    execute_query(conn, query)


def get_user_id(conn, login):
    query = f"""
        SELECT user_id
        FROM user
        WHERE user_login = "{login}"
    """

    return execute_read_query(conn, query)
