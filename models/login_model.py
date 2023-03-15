from sqlite3 import Error


def get_password(conn, login):
    query = f"""
        SELECT user_password
        FROM user
        WHERE user_login = "{login}"
    """

    return execute_read_query(conn, query)


def get_user_id(conn, login):
    query = f"""
        SELECT user_id
        FROM user
        WHERE user_login = "{login}"
    """

    return execute_read_query(conn, query)


def get_best_songs(conn):
    query = """
        SELECT song_name, performer_name, song_id, album_id, AVG(song_rating) as rating
        FROM music_list JOIN
            song USING (song_id),
            album USING (album_id),
            performer USING (performer_id)
        GROUP BY song_id
        ORDER BY rating DESC
        LIMIT 5
    """

    return execute_read_query(conn, query)

def get_best_albums(conn):
    query = """
        SELECT album_name, performer_name, album_id, AVG(album_rating) as rating
        FROM album_list 
            JOIN album USING (album_id)
            JOIN performer USING (performer_id)
        GROUP BY album_id
        ORDER BY rating DESC
        LIMIT 5
    """

    return execute_read_query(conn, query)


def get_best_performers(conn):
    query = """
        SELECT performer_name, performer_id, COUNT(performer_id) AS rating
        FROM music_list 
            JOIN song USING (song_id)
            JOIN album USING (album_id)
            JOIN performer USING (performer_id)
        GROUP BY performer_id
        ORDER BY rating  DESC
    """

    return execute_read_query(conn, query)


def get_user_song(conn, user_id, song_id):
    query = f"""
        SELECT user_id, song_id, song_status
        FROM music_list
        WHERE user_id = {user_id} AND song_id = {song_id}
    """

    return execute_read_query(conn, query)

# Добавление записи в music_list(новая запись без рейтинга и еще не добавленная в коллекцию)
def add_user_song(conn, user_id, song_id):
    query = f"""
        INSERT INTO music_list (user_id, song_id, song_status)
        VALUES ({user_id}, {song_id}, 1)
    """

    execute_query(conn, query)

# Если юзер уже оценил трек
def update_user_song(conn, user_id, song_id):
    query = f"""
        UPDATE music_list
        SET song_status = 1
        WHERE user_id = {user_id} AND song_id = {song_id}
    """

    execute_query(conn, query)


def get_user_album(conn, user_id, album_id):
    query = f"""
        SELECT user_id, album_id, album_status
        FROM album_list
        WHERE user_id = {user_id} AND album_id = {album_id}
    """

    return execute_read_query(conn, query)


def add_user_album(conn, user_id, album_id):
    query = f"""
        INSERT INTO album_list (user_id, album_id, album_status)
        VALUES ({user_id}, {album_id}, 1)
    """

    execute_query(conn, query)


def update_user_album(conn, user_id, album_id): 
    query = f"""
        UPDATE album_list
        SET album_status = 1
        WHERE user_id = {user_id} AND album_id = {album_id}
    """

    execute_query(conn, query)


def get_added_songs(conn, user_id):
    query = f"""
        SELECT song_id
        FROM music_list
        WHERE user_id = {user_id} AND song_status = 1 
    """

    return execute_read_query(conn, query)


def get_added_albums(conn, user_id):
    query = f"""
        SELECT album_id
        FROM album_list
        WHERE user_id = {user_id} AND album_status = 1 
    """

    return execute_read_query(conn, query)


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