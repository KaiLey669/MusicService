import sqlite3
from sqlite3 import Error
import pandas as pd


db_path = "music_service.sqlite"

table_genre = """
CREATE TABLE IF NOT EXISTS genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT NOT NULL
);
"""

table_performer = """
CREATE TABLE IF NOT EXISTS performer (
    performer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    performer_name TEXT NOT NULL
);
"""

table_type = """
CREATE TABLE IF NOT EXISTS type (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL
)"""

table_album = """
CREATE TABLE IF NOT EXISTS album (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_name TEXT NOT NULL,
    performer_id INTEGER,
    album_year INTEGER,
    type_id INTEGER,
    FOREIGN KEY (performer_id) REFERENCES performer (performer_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (type_id) REFERENCES type (type_id) ON DELETE SET NULL ON UPDATE CASCADE
);
"""

table_genre_performer = """
CREATE TABLE IF NOT EXISTS genre_performer (
    genre_album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_id INTEGER NOT NULL,
    performer_id INTEGER NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (performer_id) REFERENCES performer (performer_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

table_song = """
CREATE TABLE IF NOT EXISTS song (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_name TEXT NOT NULL,
    album_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES album (album_id) ON DELETE SET NULL ON UPDATE CASCADE
);
"""

table_user = """
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_login TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL
);
"""

table_music_list = """
CREATE TABLE IF NOT EXISTS music_list (
    user_id INTEGER,
    song_id INTEGER,
    song_rating INTEGER CHECK(song_rating >= 1 and song_rating <= 10),
    song_comment TEXT,
    song_status INTEGER NOT NULL CHECK(song_status >= 0 and song_status <= 1),
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (song_id) REFERENCES song (song_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id, song_id)
);
"""

table_album_list = """
CREATE TABLE IF NOT EXISTS album_list (
    user_id INTEGER,
    album_id INTEGER,
    album_rating INTEGER CHECK(album_rating >= 1 and album_rating <= 10),
    song_comment TEXT,
    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (album_id) REFERENCES user (album_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    PRIMARY KEY (user_id, album_id)   
);       
"""

insert_user = """
INSERT INTO user (user_name, user_login, user_password)
VALUES 
       ('Vlad', 'slobodchikov_vlad', 'difficult_pass'),
       ('Ivan', 'ivan_dead_inside', 'beer_lover'),
       ('Danil', 'top_8', 'vs_rf'),
       ('Sergey', 'sergey_01', 'qwerty123'),
       ('Oleg', 'oleg_20', 'asd321')
"""

drop_music_list = """
DROP TABLE music_list
"""

print_song = """
SELECT * FROM song
"""

print_user = """
SELECT * FROM user
"""

print_performer = """
SELECT * FROM performer
"""

print_tables = """
SELECT * FROM sqlite_master where type='table';
"""

insert_performer = """
INSERT INTO performer (performer_name)
VALUES 
       ('Three Days Grace'),
       ('Motionless In White'),
       ('Terror Universal'),
       ('Halestorm'),
       ('Slipknot'),       
       ('Solar Fake'),       
       ('Lord Of The Lost'),       
       ('Red'),       
       ('Disturbed'),       
       ('Wildways')       
"""

insert_type = """
INSERT INTO type (type_name)
VALUES
       ('album'),
       ('EP'),
       ('single')
"""

insert_genre = """
INSERT INTO genre (genre_name)
VALUES
       ('nu metal'),
       ('alternative rock'),
       ('alternative metal'),
       ('synth-pop'),
       ('post-grunge'),
       ('gothic metal'),
       ('industrial metal'),
       ('christian rock'),
       ('metalcore'),
       ('heavy metal'),
       ('hard rock')
"""

insert_genre_performer = """
INSERT INTO genre_performer (genre_id, performer_id)
VALUES 
       ( 10, 9),
       ( 3, 9),
       ( 1, 9),
       ( 4, 6),
       ( 9, 2),
       ( 3, 2),
       ( 7, 2),
       ( 1, 2),
       ( 2, 1),
       ( 5, 1),
       ( 3, 3),
       ( 1, 3),
       ( 11, 4),
       ( 3, 4),
       ( 10, 4),
       ( 3, 5),
       ( 1, 5),
       ( 7, 7),
       ( 6, 7),
       ( 2, 8),
       ( 8, 8),
       ( 9, 10),
       ( 2, 10)
"""

insert_album = """
INSERT INTO album (album_name, performer_id, album_year, type_id) 
VALUES 
       ('Enjoy Dystopia', 6, 2021, 1),
       ('Scoring The End Of The World', 2, 2022, 1),
       ('Disquise', 2, 2019, 1),
       ('Evolution', 9, 2018, 1),
       ('The Sickness',9 , 2000, 1),
       ('One-X', 1, 2006, 1),
       ('Make Them Bleed', 3, 2018, 1),
       ('Back From The Dead', 4, 2022, 1),
       ('5: The Grey Chapter', 5, 2014, 1),
       ('All Hope Is Gone', 5, 2008, 1),
       ('Judas', 7, 2021, 1),
       ('Thornstar', 7, 2018, 1),
       ('Declaration', 8, 2020, 1),
       ('End Of Silence', 8, 2006, 1),
       ('Day-X', 10, 2018, 1),
       ('Put In', 10, 2018, 3),
       ('Километры', 10, 2019, 3)
"""

insert_song = """
INSERT INTO song (song_name, album_id)
VALUES 
       ('I Despise You', 1),
       ('Arrive Somewhere', 1),
       ('Meltdown', 2),
       ('Sign Of Life', 2),
       ('Werewolf', 2),
       ('We Become The Night', 2),
       ('Scoring The End Of The World', 2),
       ('Porcelain', 2),
       ('Disquise', 3),
       ('Legacy', 3),
       ('Another Life', 3),
       ('A Reason To Fight', 4),
       ('Are You Ready', 4),
       ('Down With The Sickness', 5),
       ('Pain', 6),
       ('Animal I Have Become', 6),
       ('Never Too Late', 6),
       ('Time Of Dying', 6),
       ('Spines', 7),
       ('Into Darkness', 7),
       ('Back From The Dead', 8),
       ('Wicked Ways', 8),
       ('Strange Girl', 8),
       ('AOV', 9),
       ('The Devil In I', 9),
       ('Killpop', 9),
       ('Sulfur', 10),
       ('Psychosocial', 10),
       ('Dead Memories', 10),
       ('Snuff', 10),
       ('Priest', 11),
       ('Born With A Broken Heart', 11),
       ('The Gospel Of Judas', 11),
       ('Loreley', 12),
       ('Morgana', 12),
       ('Haythor', 12),
       ('The War We Made', 13),
       ('Breath Into Me', 14),
       ('Let Go', 14),
       ('Already Over', 14),
       ('Self Riot', 15),
       ('Breathless', 15),
       ('Lost', 15),
       ('Sky', 15),
       ('Put In', 16),
       ('Километры', 17)
"""

insert_music_list = """
INSERT INTO music_list (user_id, song_id, song_rating, song_status)
VALUES 
       (1, 10, 10, 1), 
       (2, 3, 9, 0), 
       (3, 34, 8, 1), 
       (4, 12, 7, 1), 
       (5, 8, 6, 1), 
       (1, 25, 5, 1),
       (2, 35, 4, 1),
       (3, 46, 3, 1),
       (4, 43, 6, 0),
       (5, 13, 8, 0),
       (1, 40, 9, 0),
       (2, 4, 10, 1),
       (3, 45, 4, 1),
       (4, 23, 9, 0),
       (5, 31, 10, 1),
       (1, 17, 3, 0),
       (2, 30, 2, 1),
       (3, 5, 10, 1),
       (4, 44, 5, 1),
       (5, 1, 8, 0),
       (1, 9, 9, 0),
       (2, 15, 2, 1),
       (3, 14, 3, 1),
       (4, 31, 4, 1),
       (5, 37, 5, 0),
       (1, 39, 8, 0),
       (2, 20, 9, 1),
       (3, 30, 10, 1),
       (4, 5, 10, 1),
       (5, 4, 10, 0),
       (1, 3, 8, 1),
       (2, 2, 7, 1),
       (3, 1, 6, 0),
       (4, 7, 2, 1),
       (5, 43, 9, 1),
       (1, 32, 5, 1),
       (2, 29, 7, 0),
       (3, 28, 9, 1),
       (4, 19, 10, 1),
       (5, 18, 8, 1),
       (1, 11, 9, 1),
       (2, 6, 5, 1),
       (3, 10, 4, 1),
       (4, 45, 8, 1),
       (5, 46, 9, 1),
       (1, 38, 10, 0),
       (2, 41, 5, 0),
       (3, 3, 7, 0),
       (4, 2, 8, 1),
       (5, 7, 9, 1)
"""

insert_album_list = """
INSERT INTO album_list (user_id, album_id, album_rating)
VALUES 
       (1, 1, 10),
       (2, 5, 9),
       (3, 3, 9),
       (4, 6, 8),
       (5, 10, 7),
       (1, 6, 7),
       (2, 2, 6),
       (3, 8, 5),
       (4, 5, 3),
       (5, 9, 4),
       (1, 14, 7),
       (2, 17, 9),
       (3, 4, 10),
       (4, 7, 7),
       (5, 8, 3),
       (1, 16, 6),
       (2, 11, 7),
       (3, 12, 9),
       (4, 3, 3),
       (5, 6, 10),
       (1, 9, 6),
       (2, 7, 9),
       (3, 10, 4),
       (4, 2, 10),
       (5, 15, 4),
       (1, 11, 8),
       (2, 4, 7)
"""

drop_genre_performer = """
DROP TABLE genre_album
"""

query_condition1 = """
SELECT album_name, album_year
FROM album
WHERE album_year <= 2010
ORDER BY album_year
"""

query_condition2 = """
SELECT user_name AS Имя, 
       song_name AS Песня, 
       IIF(song_status = 1, 'Избранное', 'Случайное') AS Статус
FROM user
     JOIN music_list USING (user_id)
     JOIN song USING (song_id)
WHERE user_id = {0} AND song_status = {1}
ORDER BY song_name
"""

query_group1 = """
SELECT album_name, AVG(album_rating)
FROM album_list
     JOIN album USING (album_id)
GROUP BY album_id
"""

query_group2 = """
SELECT song_name, AVG(song_rating)
FROM music_list
     JOIN song USING (song_id)
GROUP BY song_id
"""

query_subquery1 = """
SELECT song_name, album_name
FROM (
         SELECT album_id, song_name, user_id
         FROM song
              LEFT JOIN music_list USING (song_id)
         WHERE user_id IS Null
     )
     JOIN album USING (album_id)
"""

query_subquery2 = """
SELECT user_name, album_name, performer_name
FROM (
        SELECT performer_name, album_name, album_id
        FROM album
             JOIN performer USING (performer_id)
     )
     JOIN album_list USING (album_id)
     JOIN user USING (user_id)
"""

query_correction1 = """
INSERT INTO performer (performer_name)
VALUES ('Our Last Night')
"""

query_correction2 = """
DELETE FROM song
WHERE song_name = 'Sulfur'
"""

query = """
SELECT song_name, user_id
FROM  song
      LEFT JOIN music_list USING (song_id)
"""


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The connectoin error {e} occured")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query is executed")
    except Error as e:
        print(f"The error {e} occured")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Read query is executed")
        return result
    except Error as e:
        print(f"The error {e} occured")


def execute_script(connection, script):
    cursor = connection.cursor()
    try:
        cursor.executescript(script)
        connection.commit()
        print("Query is executed")
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection(db_path)

# execute_query(connection, insert_album_list)

# execute_query(connection, insert_music_list)
# execute_query(connection, insert_song)
# print(pd.read_sql(print_performer, connection))
# print(execute_query(connection, print_performer))

# execute_query(connection, table_performer)
# execute_query(connection, table_genre)
# execute_query(connection, table_type)
# execute_query(connection, table_album)
# execute_query(connection, table_genre_performer)
# execute_query(connection, table_song)
# execute_query(connection, table_user)
# execute_query(connection, table_music_list)
# execute_query(connection, table_album_list)

# execute_query(connection, insert_performer)
# execute_query(connection, insert_type)
# execute_query(connection, insert_genre)
# execute_query(connection, insert_user)
# execute_query(connection, insert_genre_performer)
# execute_query(connection, insert_album)

# print(pd.read_sql(query_condition1, connection))
# print(pd.read_sql(query_condition2.format(1, 1), connection))

# print(pd.read_sql(query_group1, connection))
# print(pd.read_sql(query_group2, connection))

# print(pd.read_sql(query_subquery1, connection))
# print(pd.read_sql(query_subquery2, connection))

# execute_query(connection, query_correction1)
# execute_query(connection, query_correction2)
# print(pd.read_sql(query, connection))

