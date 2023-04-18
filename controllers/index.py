from app import app
from flask import render_template, request, session
from utils import create_connection
from models.index_model import get_best_songs, \
                                get_best_albums, \
                                get_best_performers, \
                                get_albums, \
                                get_songs, \
                                get_performers, \
                                get_user_song, \
                                add_user_song, \
                                update_user_song, \
                                get_user_album, \
                                add_user_album, \
                                update_user_album, \
                                get_added_songs, \
                                get_added_albums, \
                                delete_song, \
                                delete_album, \
                                get_performer_name, \
                                get_performer_songs, \
                                get_performer_albums, \
                                get_all_songs, \
                                get_rate_songs, \
                                get_all_albums, \
                                get_rate_albums, \
                                get_user_rate_songs, \
                                get_user_rate_albums, \
                                update_rating_song, \
                                add_rating_to_song, \
                                update_rating_album, \
                                add_rating_to_album, \
                                get_password, \
                                get_user_id, \
                                insert_user, \
                                get_user_role, \
                                get_genres_names, \
                                get_performers_by_genre


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    conn = create_connection()
    best_songs = get_best_songs(conn)
    best_albums = get_best_albums(conn)
    best_performers = get_best_performers(conn)

    search = False
    perf_flag = False
    find_songs = ()
    find_albums = ()
    find_performers = ()

    performer_info = ()
    performer_songs = ()
    performer_albums = ()

    user_songs_id = []
    user_albums_id = []

    user_song_rating = ()
    user_albums_rating = ()

    global_rating_songs_dict = create_rating_songs_dict(conn)
    global_rating_albums_dict = create_rating_albums_dict(conn)

    genres = get_genres_names(conn)
    genres_search = False
    performers_by_genre = ()


    if request.values.get('exit'):
        session['user'] = 0
        session['user_role'] = 0

    if request.values.get('Login'):
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        db_password = get_password(conn, Login)

        try:
            if db_password[0][0] != Password:
                return render_template('login.html', bad_data=True)
        except:
            return render_template('login.html', bad_data=True)

        user_id = get_user_id(conn, Login)
        session['user'] = user_id[0][0]

        user_role = get_user_role(conn, session['user'])
        session['user_role'] = user_role[0][0]

    elif request.values.get('Login_reg'):
        Login = request.form.get('Login_reg')
        Password = request.form.get('Password_reg')

        insert_user(conn, Login, Password)

        user_id = get_user_id(conn, Login)
        session['user'] = user_id[0][0]


    if session.get('user') is None:
        session['user'] = 0


    if session.get('rate_song'):
        if session['user'] != 0:
            user_id = session['user']
            song_id = session.pop('rate_song')
            rating = session.pop('rating_song')
            if len(get_user_song(conn, user_id, song_id)) != 0:
                update_rating_song(conn, user_id, song_id, rating)
            else:
                add_rating_to_song(conn, user_id, song_id, rating)

    elif session.get('rate_album'):
        if session['user'] != 0:
            user_id = session['user']
            album_id = session.pop('rate_album')
            rating = session.pop('rating_album')
            if len(get_user_album(conn, user_id, album_id)) != 0:
                update_rating_album(conn, user_id, album_id, rating)
            else:
                add_rating_to_album(conn, user_id, album_id, rating)

    
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


    if request.values.get('like_song'):
        if session['user'] == 0:
            session['add_song'] = request.values.get('like_song')
            return render_template('login.html')
        else:
            user_id = session['user']
            song_id = int(request.values.get('like_song'))
            if len(get_user_song(conn, user_id, song_id)) == 0:
                add_user_song(conn, user_id, song_id)
            else:
                update_user_song(conn, user_id, song_id)

    elif request.values.get('like_album'):
        if session['user'] == 0:
            session['add_album'] = request.values.get('add_song')
            return render_template('login.html')
        else:
            user_id = session['user']
            album_id = int(request.values.get('like_album'))
            if len(get_user_album(conn, user_id, album_id)) == 0:
                add_user_album(conn, user_id, album_id)
            else:
                update_user_album(conn, user_id, album_id)

    elif request.values.get('song_id'):
        if session['user'] == 0:
            session['rate_song'] = request.values.get('song_id')
            session['rating_song'] = request.values.get('rating')
            return render_template('login.html')
        else:
            if len(get_user_song(conn, session['user'], request.values.get('song_id'))) != 0:
                update_rating_song(conn, session['user'], request.values.get('song_id'), request.values.get('rating'))
            else:
                add_rating_to_song(conn, session['user'], request.values.get('song_id'), request.values.get('rating'))

    elif request.values.get('album_id'):
        if session['user'] == 0:
            session['rate_album'] = request.values.get('album_id')
            session['rating_album'] = request.values.get('rating')
            return render_template('login.html')
        else:
            if len(get_user_album(conn, session['user'], request.values.get('album_id'))) != 0:
                update_rating_album(conn, session['user'], request.values.get('album_id'), request.values.get('rating'))
            else:
                add_rating_to_album(conn, session['user'], request.values.get('album_id'), request.values.get('rating'))


    elif request.values.get('delete_song'):
        delete_song(conn, session['user'], request.values.get('delete_song'))

    elif request.values.get('delete_album'):
        delete_album(conn, session['user'], request.values.get('delete_album'))

    elif request.values.get('performer'):
        performer_id = request.values.get('performer')
        performer_info = get_performer_name(conn, performer_id)
        performer_songs = get_performer_songs(conn, performer_id)
        performer_albums = get_performer_albums(conn, performer_id)
        perf_flag = True

    elif request.values.get('Search'):
        search_str = request.values.get('Search').lower().strip()
        find_songs = get_songs(conn, search_str)
        find_albums = get_albums(conn, search_str)
        find_performers = get_performers(conn, search_str)
        search = True

    elif request.values.get('genre_search'):
        genres_search = True
        performers_by_genre = get_performers_by_genre(conn, int(request.values.get('genre_search')))


    if session.get('user') != 0:

        user_songs = get_added_songs(conn, session['user'])
        for id in user_songs:
            user_songs_id.append(id[0])

        user_albums = get_added_albums(conn, session['user'])
        for id in user_albums:
            user_albums_id.append(id[0])

        user_song_rating = create_user_rating_songs_dict(conn, session['user'])
        user_albums_rating = create_user_rating_albums_dict(conn, session['user'])


    html = render_template(
        'index.html',
        songs=best_songs,
        albums=best_albums,
        performers=best_performers,
        search=search,
        find_songs=find_songs,
        find_albums=find_albums,
        find_performers=find_performers,
        user_songs=user_songs_id,
        user_albums=user_albums_id,
        perf_flag=perf_flag,
        performer_info=performer_info,
        performer_songs=performer_songs,
        performer_albums=performer_albums,
        songs_rating=global_rating_songs_dict,
        albums_rating=global_rating_albums_dict,
        user_songs_rating=user_song_rating,
        user_albums_rating=user_albums_rating,
        genres=genres,
        genres_search=genres_search,
        perf_by_genre=performers_by_genre,
        len=len,
        str=str
    )
    return html


def create_rating_songs_dict(conn):
    all_songs_id = get_all_songs(conn)
    all_songs_with_rating = get_rate_songs(conn)

    rating_dict = {}
    for record in all_songs_with_rating:
        rating_dict[record[0]] = record[1]

    for id in all_songs_id:
        if id[0] not in rating_dict:
            rating_dict[id[0]] = 0
        else:
            if rating_dict[id[0]] is None:
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
        else:
            if rating_dict[id[0]] is None:
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
