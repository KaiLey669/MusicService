from sqlite3 import Error
from utils import execute_query, execute_read_query

# Songs -----------------------------------------------------------
def get_albums(conn):
    query = """
        SELECT album_name, album_id 
        FROM album
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


def get_song_id(conn, song_name, album_id, performer_id):
    query = f"""
        SELECT song_id
        FROM song
            JOIN album USING(album_id)
            JOIN performer USING(performer_id)
        WHERE song_name = '{song_name}' AND album_id = {album_id} AND performer_id = {performer_id}
    """

    return execute_read_query(conn, query)


def delete_song(conn, song_id):
    query = f"""
        DELETE FROM song
        WHERE song_id = {song_id}
    """

    execute_query(conn, query)


# Songs -----------------------------------------------------------

# Albums ----------------------------------------------------------
def get_performers(conn):
    query = """
        SELECT performer_name, performer_id
        FROM performer
        ORDER BY performer_name
    """

    return execute_read_query(conn, query)


def add_album(conn, album_name, performer_id, type_id):
    query = f"""
        INSERT INTO album (album_name, performer_id, type_id)
        VALUES ('{album_name}', {performer_id}, {type_id})
    """

    execute_query(conn, query)


def get_performer_id(conn, performer_name):
    query = f"""
        SELECT performer_id
        FROM performer
        WHERE performer_name = '{performer_name}'
    """

    return execute_read_query(conn, query)
# Albums ----------------------------------------------------------


# Perf ----------------------------------------------------------

def add_performer(conn, performer_name):
    query = f"""
        INSERT INTO performer (performer_name)
        VALUES ('{performer_name}')
    """

    execute_query(conn, query)

# Perf ----------------------------------------------------------


def get_album_by_perf(conn, perf_id):
    query = f"""
        SELECT album_name, album_id
        FROM album
        WHERE performer_id = {perf_id}
    """

    return execute_read_query(conn, query)


def get_song_by_album(conn, album_id):
    query = f"""
        SELECT song_name, song_id
        FROM song
        WHERE album_id = {album_id}
    """

    return execute_read_query(conn, query)


def delete_album(conn, album_id):
    query = f"""
        DELETE FROM album
        WHERE album_id = {album_id}
    """

    execute_query(conn, query)


def delete_performer(conn, perf_id):
    query = f"""
        DELETE FROM performer
        WHERE performer_id = {perf_id}
    """

    execute_query(conn, query)
