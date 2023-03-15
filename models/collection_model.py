from sqlite3 import Error


def get_songs(conn, user_id):
    query = f"""
        SELECT song_name, performer_name, song_id, album_id
        FROM music_list
            JOIN song USING (song_id)
            JOIN album USING (album_id)
            JOIN performer USING (performer_id)
        WHERE user_id = {user_id} AND song_status = 1
    """

    return execute_read_query(conn, query)


def get_albums(conn, user_id):
    query = f"""
        SELECT album_name, performer_name, album_id
        FROM album_list
            JOIN album USING (album_id)
            JOIN performer USING (performer_id)
        WHERE user_id = {user_id} AND album_status = 1
    """

    return execute_read_query(conn, query)


def delete_user_song(conn, user_id, song_id):
    query = f"""
        UPDATE music_list 
        SET song_status = 0
        WHERE user_id = {user_id} AND song_id = {song_id}
    """

    return execute_query(conn, query)


def delete_user_album(conn, user_id, album_id):
    query = f"""
        UPDATE album_list 
        SET album_status = 0
        WHERE user_id = {user_id} AND album_id = {album_id}
    """

    return execute_query(conn, query)


# --------------------------------

def get_all_songs(conn):
    query = """
        SELECT song_id
        FROM song
    """

    return execute_read_query(conn, query)


def get_rate_songs(conn):
    query = """
        SELECT song_id, AVG(song_rating) AS rating
        FROM music_list
        GROUP BY song_id
        ORDER BY song_id
    """

    return execute_read_query(conn, query)


def get_all_albums(conn):
    query = """
        SELECT album_id
        FROM album
    """

    return execute_read_query(conn, query)


def get_rate_albums(conn):
    query = """
        SELECT album_id, AVG(album_rating) AS rating
        FROM album_list
        GROUP BY album_id
        ORDER BY album_id
    """

    return execute_read_query(conn, query)

# --------------------------------

# --------------------------------

def get_user_rate_songs(conn, user_id):
    query = f"""
        SELECT song_id, song_rating
        FROM music_list
        WHERE user_id = {user_id}
    """

    return execute_read_query(conn, query)

def get_user_rate_albums(conn, user_id):
    query = f"""
        SELECT album_id, album_rating
        FROM album_list
        WHERE user_id = {user_id}
    """

    return execute_read_query(conn, query)

# --------------------------------

# Добавления рейтинга для песни, которая уже в коллекции пользователя
def update_rating_song(conn, user_id, song_id, rating):
    query = f"""
        UPDATE music_list
        SET song_rating = {rating}
        WHERE user_id = {user_id} AND song_id = {song_id}
    """

    execute_query(conn, query)


# Добавление записи в music_list с установленным рейтингом(трек не добавлен в коллекцию юзера)
def add_rating_to_song(conn, user_id, song_id, rating):
    query = f"""
        INSERT INTO music_list (user_id, song_id, song_rating, song_status)
        VALUES ({user_id}, {song_id}, {rating}, 0)
    """

    execute_query(conn, query)


def update_rating_album(conn, user_id, album_id, rating):
    query = f"""
        UPDATE album_list
        SET album_rating = {rating}
        WHERE user_id = {user_id} AND album_id = {album_id}
    """

    execute_query(conn, query)


def add_rating_to_album(conn, user_id, album_id, rating):
    query = f"""
        INSERT INTO music_list (user_id, album_id, album_rating, album_status)
        VALUES ({user_id}, {album_id}, {rating}, 0)
    """

    execute_query(conn, query)

# -----------------------------------------------------------------------------------

def get_user_song(conn, user_id, song_id):
    query = f"""
        SELECT user_id, song_id, song_status, song_rating
        FROM music_list
        WHERE user_id = {user_id} AND song_id = {song_id}
    """

    return execute_read_query(conn, query)


def get_user_album(conn, user_id, album_id):
    query = f"""
        SELECT user_id, album_id, album_status
        FROM album_list
        WHERE user_id = {user_id} AND album_id = {album_id}
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