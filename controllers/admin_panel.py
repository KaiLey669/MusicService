from app import app
from flask import render_template, request, session
from utils import create_connection
from models.admin_panel_model import get_albums_names


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    conn = create_connection()

    list_flag = 'music'
    albums_names_list = get_albums_names(conn)
    # print(albums_names_list)

    if request.values.get('flag'):
        list_flag = request.values.get('flag')
    

    html = render_template(
        'admin_panel.html',
        albums_names=albums_names_list,
        flag = list_flag,
        len=len,
        str=str)
    
    return html