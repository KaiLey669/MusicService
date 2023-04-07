from app import app
from flask import render_template, request, session, url_for
from utils import create_connection
from models.login_model import get_password, \
                               get_user_id, \
                               get_best_performers, \
                               get_best_songs, \
                               get_best_albums, \
                               get_user_song, \
                               add_user_song, \
                               update_user_song, \
                               get_user_album, \
                               add_user_album, \
                               update_user_album, \
                               get_added_songs, \
                               get_added_albums, \
                               get_all_songs, \
                               get_rate_songs, \
                               get_all_albums, \
                               get_rate_albums, \
                               get_user_rate_songs, \
                               get_user_rate_albums, \
                               get_user_role


@app.route('/login', methods=['GET', 'POST'])
def login():

    user_songs_id = []
    user_albums_id = []

    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        conn = create_connection()
        db_password = get_password(conn, Login)

        try:
            if db_password[0][0] != Password:
                return render_template('login.html', bad_data=True)
        except:
            return render_template('login.html', bad_data=True)

        user_id = get_user_id(conn, Login)
        session['user'] = user_id[0][0]
        user_role = get_user_role(conn, user_id)

        best_songs = get_best_songs(conn)
        best_albums = get_best_albums(conn)
        best_performers = get_best_performers(conn)

        user_songs = get_added_songs(conn, session['user'])
        for id in user_songs:
            user_songs_id.append(id[0])

        user_albums = get_added_albums(conn, session['user'])
        for id in user_albums:
            user_albums_id.append(id[0])


        if session.get('add_song'):
            if session['user'] != 0:
                user_id = session['user']
                song_id = session.pop('add_song')
                if len(get_user_song(conn, user_id, song_id)) == 0:
                    add_user_song(conn, user_id, song_id)
                else:
                    update_user_song(conn, user_id, song_id) 

        elif session.get('add_album'):
            if session['user'] != 0:
                user_id = session['user']
                album_id = session.pop('add_album')
                if len(get_user_album(conn, user_id, album_id)) == 0:
                    add_user_album(conn, user_id, album_id)
                else:
                    update_user_album(conn, user_id, album_id)

        global_rating_songs_dict = create_rating_songs_dict(conn)
        global_rating_albums_dict = create_rating_albums_dict(conn)

        user_song_rating = create_user_rating_songs_dict(conn, session['user'])
        user_albums_rating = create_user_rating_albums_dict(conn, session['user'])

        # return url_for('index', methods=['GET'])

        return render_template('index.html',
                                songs=best_songs,
                                albums=best_albums,
                                performers=best_performers,
                                search=False,
                                user_songs=user_songs_id,
                                user_albums=user_albums_id,
                                songs_rating=global_rating_songs_dict,
                                albums_rating=global_rating_albums_dict,
                                user_songs_rating=user_song_rating,
                                user_albums_rating=user_albums_rating,
                                user_role = user_role[0][0],
                                len=len,
                                str=str)


    return render_template('login.html')


def create_rating_songs_dict(conn):
    all_songs_id = get_all_songs(conn)
    all_songs_with_rating = get_rate_songs(conn)

    rating_dict = {}
    for record in all_songs_with_rating:
        rating_dict[record[0]] = record[1]

    for id in all_songs_id:
        if id[0] not in rating_dict:
            rating_dict[id[0]] = 0

    return rating_dict


def create_rating_albums_dict(conn):
    all_albums_id = get_all_albums(conn)
    all_albums_with_rating = get_rate_albums(conn)

    rating_dict = {}
    for record in all_albums_with_rating:
        rating_dict[record[0]] = record[1]

    for id in all_albums_id:
        if id[0] not in rating_dict:
            rating_dict[id[0]] = 0

    return rating_dict


def create_user_rating_songs_dict(conn, user_id):
    all_songs_id = get_all_songs(conn)
    songs_with_user_rating = get_user_rate_songs(conn, user_id)

    rating_dict = {}
    for record in songs_with_user_rating:
        rating_dict[record[0]] = record[1]

    for id in all_songs_id:
        if id[0] not in rating_dict:
            rating_dict[id[0]] = 0
        else:
            if rating_dict[id[0]] is None:
                rating_dict[id[0]] = 0

    return rating_dict


def create_user_rating_albums_dict(conn, user_id):
    all_albums_id = get_all_albums(conn)
    albums_with_user_rating = get_user_rate_albums(conn, user_id)

    rating_dict = {}
    for record in albums_with_user_rating:
        rating_dict[record[0]] = record[1]

    for id in all_albums_id:
        if id[0] not in rating_dict:
            rating_dict[id[0]] = 0
        else:
            if rating_dict[id[0]] is None:
                rating_dict[id[0]] = 0

    return rating_dict