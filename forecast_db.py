from peewee import *
import sqlite3

db = SqliteDatabase('forecast.db')


class Forecast(Model):
    longitude = FloatField()
    latitude = FloatField()
    date_of_forecast = TextField()
    time_of_forecast = TextField()
    part_of_day = TextField()
    sunrise = TextField()
    sunset = TextField()

    current_weather = TextField()
    current_dark_time = BooleanField()
    current_astro = BooleanField()
    first_period_weather = TextField()
    first_period_astro = BooleanField()
    first_period_dark_time = BooleanField()
    second_period_weather = TextField()
    second_period_astro = BooleanField()
    second_period_dark = BooleanField()

    class Meta:
        database = db
