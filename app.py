from flask import Flask, session
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


import controllers.index
import controllers.login
import controllers.registration
import controllers.collection