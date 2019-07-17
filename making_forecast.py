from getting_forecast import *
from forecast_db import *


def make_forecast(latitude, longitude, date, time, part_of_day, make_new_item):
    all_forecast = request_to_weather(latitude, longitude)
    if all_forecast['fact']['polar']:
        sunrise = 'polar'
        sunset = 'polar'
    else:
        sunrise = all_forecast['forecast']['sunrise']
        sunset = all_forecast['forecast']['sunset']

    cur_weather = all_forecast['fact']['condition']
    cur_dark_time = (all_forecast['fact']['daytime'] == 'n')
    cur_astro = (cur_weather in ['clear', 'partly-cloudy']) and cur_dark_time

    frst_weather = all_forecast['forecast']['parts'][0]['condition']
    frst_dark_time = (all_forecast['forecast']['parts'][0]['daytime'] == 'n')
    frst_astro = (frst_weather in ['clear', 'partly-cloudy']) and frst_dark_time

    scnd_weather = all_forecast['forecast']['parts'][1]['condition']
    scnd_dark_time = (all_forecast['forecast']['parts'][1]['daytime'] == 'n')
    scnd_astro = (scnd_weather in ['clear', 'partly-cloudy']) and scnd_dark_time

    weather_values = {'clear': 'Clear',
                      'partly-cloudy': 'Partly cloudy',
                      'cloudy': 'Cloudy',
                      'overcast': 'Overcast',
                      'partly-cloudy-and-light-rain': 'Light rain',
                      'partly-cloudy-and-rain': 'Rain',
                      'overcast-and-rain': 'Heavy rain',
                      'overcast-thunderstorms-with-rain': 'Thunderstorms',
                      'cloudy-and-light-rain': 'Light rain',
                      'overcast-and-light-rain': 'Light rain',
                      'cloudy-and-rain': 'Rain',
                      'overcast-and-wet-snow': 'Rain with snow',
                      'partly-cloudy-and-light-snow': 'Light snow',
                      'partly-cloudy-and-snow': 'Snow',
                      'overcast-and-snow': 'Snowfall',
                      'cloudy-and-light-snow': 'Light snow',
                      'overcast-and-light-snow': 'Light snow',
                      'cloudy-and-snow': 'Snow'}

    if make_new_item:
        new_item = Forecast.create_table(longitude=longitude,
                                         latitude=latitude,
                                         date_of_forecast=date,
                                         time_of_forecast=time,
                                         part_of_day=part_of_day,
                                         sunrise=sunrise,
                                         sunset=sunset,
                                         current_weather=weather_values[cur_weather],
                                         current_dark_time=cur_dark_time,
                                         current_astro=cur_astro,
                                         first_period_weather=weather_values[frst_weather],
                                         first_period_dark_time=frst_dark_time,
                                         first_period_astro=frst_astro,
                                         second_period_weather=weather_values[scnd_astro],
                                         second_period_astro=scnd_astro,
                                         second_period_dark_time=scnd_dark_time)
    else:
        item = Forecast.get(Forecast.latitude == latitude and Forecast.longitude == longitude)
        item.longitude=longitude,
        item.latitude=latitude
        item.date_of_forecast=date
        item.time_of_forecast=time
        item.part_of_day=part_of_day
        item.sunrise=sunrise
        item.sunset=sunset
        item.current_weather=weather_values[cur_weather]
        item.current_dark_time=cur_dark_time
        item.current_astro=cur_astro
        item.first_period_weather=weather_values[frst_weather]
        item.first_period_dark_time=frst_dark_time
        item.first_period_astro=frst_astro
        item.second_period_weather=weather_values[scnd_astro]
        item.second_period_astro=scnd_astro
        item.second_period_dark_time=scnd_dark_time
        item.save()
