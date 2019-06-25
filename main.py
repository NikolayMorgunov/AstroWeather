import requests
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired
from flask import redirect, render_template
from flask import session
from auth_check import *
from users_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_astronomy'

User.create_table()


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
    if 'username' in session:
        return redirect('/main_page')
    form = LoginForm()
    username = form.data['username']
    password = form.data['password']
    normal_auth = True
    if form.validate_on_submit():
        if auth_check(username, password):
            session['username'] = username
            return redirect('/main_page')
        else:
            normal_auth = False
    return render_template('login.html', title='Вход', form=form, normal_auth=normal_auth)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
