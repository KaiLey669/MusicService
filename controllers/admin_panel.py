from app import app
from flask import render_template, request, session
from utils import create_connection
from models.admin_panel_model import get_albums_names, add_song, \
                                     get_album_id, \
                                     get_performers_names, \
                                     add_album


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

    if request.values.get('added_album_name'):
        pass


    html = render_template(
        'admin_panel.html',
        albums_names=albums_names_list,
        performers_names=performers_names_list,
        flag = list_flag,
        len=len,
        str=str)
    
    return html