import requests
from flask import Flask, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from auth_check import *
from users_db import *
from forecast_db import *
from geocoding import *
from timezonefinder import *
from month import *
from making_forecast import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_astronomy'

User.create_table()
Forecast.create_table()
tf = TimezoneFinder(in_memory=True)


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
            user.country = country
            user.city = city
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
    timezone = tf.timezone_at(lat=latitude, lng=longitude)
    time_request = 'http://worldtimeapi.org/api/timezone/' + timezone
    response_time = requests.get(time_request)
    json_response = response_time.json()
    datetime = json_response['datetime']
    date = datetime[:10]
    year = datetime[:4]
    month = digit_word_month(datetime[5:7])
    day = datetime[8:10]
    time = datetime[11:16]
    hours = int(time[:2])
    part_of_day = ['Night', 'Morning', 'Day', 'Evening'][hours // 6]

    need_new_forecast_item = not (
        bool(Forecast.select().where(Forecast.latitude == latitude and Forecast.longitude == longitude)))
    if need_new_forecast_item:
        item = make_forecast(latitude, longitude, date, time, part_of_day, True)
    else:
        item = Forecast.get(Forecast.latitude == latitude and Forecast.longitude == longitude)
        if not (item.date_of_forecast == date and item.part_of_day == part_of_day):
            item = make_forecast(latitude, longitude, date, time, part_of_day, False)

    parts_timing = {'Night': '6:00', 'Morning': '12:00', 'Day': '18:00', 'Evening': '00:00'}
    dark_time = {True: "Dark time", False: "Light time"}
    astro_norm = {True: "Good time for astronomy", False: "Bad time for astronomy"}

    text = [[time + ' - ' + parts_timing[part_of_day], item.current_weather, dark_time[
        item.current_dark_time], astro_norm[item.current_astro] + '\n']]

    if part_of_day == 'Night':
        second_period = '6:00 - 12:00'
        third_period = '12:00 - 18:00'
    elif part_of_day == 'Morning':
        second_period = '12:00 - 18:00'
        third_period = '18:00 - 00:00'
    elif part_of_day == 'Day':
        second_period = '18:00 - 00:00'
        third_period = '00:00 - 06:00'
    else:
        second_period = '00:00 - 06:00'
        third_period = '6:00 - 12:00'

    text.append([second_period, item.first_period_weather, dark_time[item.first_period_dark_time], \
                 astro_norm[item.first_period_astro]])
    text.append([third_period, item.second_period_weather, dark_time[item.second_period_dark], \
                 astro_norm[item.second_period_astro]])

    if item.sunrise == 'polar':
        return render_template('forecast.html', title='Forecast', loginned='username' in session,
                               username=session['username'], city=user.city, day=day, month=month, year=year,
                               not_polar=False, text=text)
    else:
        return render_template('forecast.html', title='Forecast', loginned='username' in session,
                               username=session['username'], city=user.city, day=day, month=month, year=year,
                               not_polar=True, sunrise=item.sunrise, sunset=item.sunset, text=text)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
