from app import app
from flask import render_template, request, session
from utils import create_connection
from models.admin_panel_model import get_albums, add_song, \
                                     get_album_id, \
                                     get_performers, \
                                     add_album, \
                                     get_performer_id, \
                                     get_song_id, \
                                     delete_song, \
                                     add_performer, \
                                    get_album_by_perf, \
                                    get_song_by_album


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    conn = create_connection()

    list_flag = 'music'
    albums_list = get_albums(conn)
    performers_list = get_performers(conn)


    if request.values.get('flag'):
        list_flag = request.values.get('flag')

    if request.values.get('added_song_name'):
        song_name = request.values.get('added_song_name')
        album_name = request.values.get('new_song_album')
        album_id = get_album_id(conn, album_name)[0][0]

        add_song(conn, song_name, album_id)

    if request.values.get('delete_performer'):
        performer_id = get_performer_id(conn, request.values.get('delete_performer'))[0][0]
        album_id = get_album_id(conn, request.values.get('delete_values'))[0][0]
        song_id = get_song_id(conn, request.values.get('delete_song'), album_id, performer_id)[0][0]

        delete_song(conn, song_id)


    if request.values.get('added_album_name'):
        album_name = request.values.get('added_album_name')
        performer_id = get_performer_id(conn, request.values.get('new_album_performer'))[0][0]
        type_id = int(request.values.get('album_type'))

        add_album(conn, album_name, performer_id, type_id)

    
    if request.values.get('added_perf_name'):
        performer_name = request.values.get('added_perf_name')

        add_performer(conn, performer_name)

    
    if request.values.get('delete_song'):
        delete_song(conn, request.values.get('delete_song'))


    html = render_template(
        'admin_panel.html',
        albums_list=albums_list,
        performers_list=performers_list,
        flag = list_flag,
        len=len,
        str=str)
    
    return html


@app.route('/admin_albums', methods=['GET'])
def admin_albums():
    perf_id = request.values.get('perf_id')

    if not perf_id:
        return {}

    conn = create_connection()
    
    albums_by_perf = get_album_by_perf(conn, perf_id)
    return {'albums': [
        {'album_id': row[1],
         'album_name': row[0]}
        for row in albums_by_perf
    ]}


@app.route('/admin_songs', methods=['GET'])
def admin_songss():
    album_id = request.values.get('album_id')

    if not album_id:
        return {}

    conn = create_connection()
    
    songs_by_album = get_song_by_album(conn, album_id)
    return {'songs': [
        {'song_id': row[1],
         'song_name': row[0]}
        for row in songs_by_album
    ]}