from app import app
from flask import render_template, request, session
from utils import create_connection
from models.registration_model import insert_user, get_user_id

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    if request.method == 'POST':
        Login = request.form.get('Login')
        Password = request.form.get('Password')

        conn = create_connection()
        insert_user(conn, Login, Password)

        user_id = get_user_id(conn, Login)
        session['user'] = user_id[0][0]

        return render_template('index.html')


    return render_template('registration.html')
