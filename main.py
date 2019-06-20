import requests
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'

from flask import redirect, render_template
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_astronomy'


