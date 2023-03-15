from app import app
from flask import render_template, request, session
from utils import create_connection
from models.collection_model import get_albums, get_songs, delete_user_song, delete_user_album, \
                                    get_all_songs, \
                                    get_rate_songs, \
                                    get_all_albums, \
                                    get_rate_albums, \
                                    get_user_rate_songs, \
                                    get_user_rate_albums, \
                                    update_rating_song, \
                                    update_rating_album, \
                                    add_rating_to_song, \
                                    add_rating_to_album, \
                                    get_user_album, \
                                    get_user_song


@app.route('/collection', methods=['GET', 'POST'])
def collection():
    conn = create_connection()
    current_user = session['user']
    list_flag = 'music' # Список песен

    user_songs_id = []
    user_albums_id = []


    if request.values.get('flag'):
        list_flag = request.values.get('flag')

    if request.values.get('delete_song'):
        song_id = int(request.values.get('delete_song'))
        delete_user_song(conn, current_user, song_id)

    if request.values.get('delete_album'):
        album_id = int(request.values.get('delete_album'))
        delete_user_album(conn, current_user, album_id)

    if request.values.get('song_id'):
        if session['user'] == 0:
            session['rate_song'] = request.values.get('song_id')
            session['rating_song'] = request.values.get('rating')
            return render_template('login.html')
        else:
            if len(get_user_song(conn, session['user'], request.values.get('song_id'))) != 0:
                update_rating_song(conn, session['user'], request.values.get('song_id'), request.values.get('rating'))
            else:
                add_rating_to_song(conn, session['user'], request.values.get('song_id'), request.values.get('rating'))

    if request.values.get('album_id'):
        if session['user'] == 0:
            session['rate_album'] = request.values.get('album_id')
            session['rating_album'] = request.values.get('rating')
            return render_template('login.html')
        else:
            if len(get_user_album(conn, session['user'], request.values.get('album_id'))) != 0:
                update_rating_album(conn, session['user'], request.values.get('album_id'), request.values.get('rating'))
            else:
                add_rating_to_album(conn, session['user'], request.values.get('album_id'), request.values.get('rating'))
    

    songs = get_songs(conn, current_user)
    for id in songs:
        user_songs_id.append(id[2])

    albums = get_albums(conn, current_user)
    for id in albums:
        user_albums_id.append(id[2])


    global_rating_songs_dict = create_rating_songs_dict(conn)
    global_rating_albums_dict = create_rating_albums_dict(conn)

    user_song_rating = create_user_rating_songs_dict(conn, session['user'])
    user_albums_rating = create_user_rating_albums_dict(conn, session['user'])
    
    html = render_template(
        'collection.html',
        songs=songs,
        albums=albums,
        flag=list_flag,
        user_songs=user_songs_id,
        user_albums=user_albums_id,
        songs_rating=global_rating_songs_dict,
        albums_rating=global_rating_albums_dict,
        user_songs_rating=user_song_rating,
        user_albums_rating=user_albums_rating,
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