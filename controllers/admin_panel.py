from app import app
from flask import render_template, request, session
from utils import create_connection


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():

    list_flag = 'music'

    if request.values.get('flag'):
        list_flag = request.values.get('flag')
    

    html = render_template(
        'admin_panel.html',
        flag = list_flag)
    
    return html