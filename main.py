import requests
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired
from flask import redirect, render_template
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_astronomy'


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rep_password = PasswordField('Repeat password', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Sign up')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
