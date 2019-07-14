from peewee import *
import sqlite3


db = SqliteDatabase('users.db')


class User(Model):
    username = CharField()
    password = CharField()
    country = CharField()
    city = CharField()
    longitude = FloatField()
    latitude = FloatField()

    class Meta:
        database = db
