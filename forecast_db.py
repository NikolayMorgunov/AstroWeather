from peewee import *
import sqlite3


db = SqliteDatabase('forecast.db')


class Forecast(Model):
    longitude = FloatField()
    latitude = FloatField()
    timezone = TextField()
    date_of_forecast = TextField()
    time_of_forecast = TextField()

    weather_descript_morning = TextField()
    asrtro_ok_morning = BooleanField()
    weather_descript_day = TextField()
    astro_ok_day = BooleanField()
    weather_descript_evening = TextField()
    astro_ok_evening = BooleanField()
    weather_descript_night = TextField()
    astro_ok_night = BooleanField()


