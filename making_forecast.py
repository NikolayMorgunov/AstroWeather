from getting_forecast import *
from forecast_db import *
from configures import *


def make_forecast(latitude, longitude, date, time, part_of_day, make_new_item):
    all_forecast = request_to_weather(latitude, longitude)
    if abs(latitude) >= 66.562:
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

    if make_new_item:
        item = Forecast.create(longitude=longitude,
                               latitude=latitude,
                               date_of_forecast=date,
                               time_of_forecast=time,
                               part_of_day=part_of_day,
                               sunrise=sunrise,
                               sunset=sunset,
                               current_weather=WEATHER_VALUES[cur_weather],
                               current_dark_time=cur_dark_time,
                               current_astro=cur_astro,
                               first_period_weather=WEATHER_VALUES[frst_weather],
                               first_period_dark_time=frst_dark_time,
                               first_period_astro=frst_astro,
                               second_period_weather=WEATHER_VALUES[scnd_weather],
                               second_period_astro=scnd_astro,
                               second_period_dark=scnd_dark_time)
    else:
        item = Forecast.get(Forecast.latitude == latitude and Forecast.longitude == longitude)
        item.date_of_forecast = date
        item.time_of_forecast = time
        item.part_of_day = part_of_day
        item.sunrise = sunrise
        item.sunset = sunset
        item.current_weather = WEATHER_VALUES[cur_weather]
        item.current_dark_time = cur_dark_time
        item.current_astro = cur_astro
        item.first_period_weather = WEATHER_VALUES[frst_weather]
        item.first_period_dark_time = frst_dark_time
        item.first_period_astro = frst_astro
        item.second_period_weather = WEATHER_VALUES[scnd_weather]
        item.second_period_astro = scnd_astro
        item.second_period_dark = scnd_dark_time
        item.save()
    return item
