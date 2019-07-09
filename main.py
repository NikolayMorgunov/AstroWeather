import requests
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired
from flask import redirect, render_template
from flask import session
from auth_check import *
from users_db import *
from forecast_db import *
from geocoding import *

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
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class ChangeLocation(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Change')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/forecast')
    form = LoginForm()
    username = form.data['username']
    password = form.data['password']
    normal_auth = True
    if form.validate_on_submit():
        if auth_check(username, password):
            session['username'] = username
            return redirect('/forecast')
        else:
            normal_auth = False
    return render_template('login.html', title='Login', form=form, normal_auth=normal_auth,
                           loginned='username' in session)


@app.route('/log_out', methods=['GET', 'POST'])
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    exists = False
    diff_pass = False
    location_exists = True
    username = form.data['username']
    password = form.data['password']
    rep_password = form.data['rep_password']
    country = form.data['country']
    city = form.data['city']
    if form.validate_on_submit():
        if User.select().where(User.username == username):
            exists = True
        elif password != rep_password:
            diff_pass = True
        elif not exist(country, city):
            location_exists = False
        else:
            coords_of_city = coords(country, city)
            longitude = coords_of_city[0]
            latitude = coords_of_city[1]
            user = User.create(username=username, password=password, country=country, city=city, longitude=longitude,
                               latitude=latitude)
            return redirect("/success_register")
    return render_template('register.html', title='Sign up', form=form, exists=exists, diff_pass=diff_pass,
                           location_not_exist=not location_exists,
                           loginned='username' in session)


@app.route('/success_register', methods=['GET', 'POST'])
def success_register():
    if 'username' in session:
        return render_template('success_register.html', title='Register success', loginned='username' in session,
                               username=session['username'])
    else:
        return render_template('success_register.html', title='Register success', loginned='username' in session)


@app.route('/about', methods=['GET', 'POST'])
def about():
    if 'username' in session:
        return render_template('about.html', title='About', loginned='username' in session,
                               username=session['username'])
    else:
        return render_template('about.html', title='About', loginned='username' in session)


@app.route('/change_location', methods=['GET', 'POST'])
def change_location():
    form = ChangeLocation()
    location_exists = True
    country = form.data['country']
    city = form.data['city']
    if form.validate_on_submit():
        if not exist(country, city):
            location_exists = False
        else:
            coords_of_city = coords(country, city)
            longitude = coords_of_city[0]
            latitude = coords_of_city[1]
            user = User.get(User.username == session['username'])
            user.longitude = longitude
            user.latitude = latitude
            user.save()
            return redirect("/success_change")
    return render_template('change_location.html', title='Change location', form=form,
                           location_not_exist=not location_exists,
                           loginned='username' in session, username=session['username'])


@app.route('/success_change', methods=['GET', 'POST'])
def success_change():
    if 'username' in session:
        return render_template('success_change.html', title='Change success', loginned='username' in session,
                               username=session['username'])
    else:
        return render_template('success_change.html', title='Change success', loginned='username' in session)


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    user = User.get(User.username == session['username'])
    longitude = user.longitude
    latitude = user.latitude
    prepared_city = bool(Forecast.select().where(Forecast.latitude == latitude and Forecast.longitude == longitude))



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
