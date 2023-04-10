from sqlite3 import Error


# Songs -----------------------------------------------------------
def get_albums_names(conn):
    query = """
        SELECT album_name FROM album
        ORDER BY album_name
    """

    return execute_read_query(conn, query)


def add_song(conn, song_name, album_id):
    query = f"""
        INSERT INTO song (song_name, album_id)
        VALUES ('{song_name}', {album_id})
    """

    execute_query(conn, query)


# Не будет работать, если в таблице есть альбомы с одинаковым названием
def get_album_id(conn, album_name):
    query = f"""
        SELECT album_id
        FROM album
        WHERE album_name = '{album_name}' 
    """

    return execute_read_query(conn, query)
# Songs -----------------------------------------------------------

# Albums ----------------------------------------------------------
def get_performers_names(conn):
    query = """
        SELECT performer_name
        FROM performer
    """

    return execute_read_query(conn, query)


def add_album(conn, album_name, performer_id, type_id):
    query = f"""
        INSERT INTO album (album_name, performer_id, type_id)
        VALUES ('{album_name}', {performer_id}, {type_id})
    """

    execute_query(conn, query)


# Albums ----------------------------------------------------------





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