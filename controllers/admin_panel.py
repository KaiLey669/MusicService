from app import app
from flask import render_template, request, session
from utils import create_connection
from models.admin_panel_model import get_albums_names, add_song, \
                                     get_album_id, \
                                     get_performers_names, \
                                     add_album, \
                                     get_performer_id, \
                                     get_song_id, \
                                     delete_song, \
                                     add_performer


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    conn = create_connection()

    list_flag = 'music'
    albums_names_list = get_albums_names(conn)
    performers_names_list = get_performers_names(conn)


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


    html = render_template(
        'admin_panel.html',
        albums_names=albums_names_list,
        performers_names=performers_names_list,
        flag = list_flag,
        len=len,
        str=str)
    
    return html