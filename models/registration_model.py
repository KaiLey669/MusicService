from sqlite3 import Error


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