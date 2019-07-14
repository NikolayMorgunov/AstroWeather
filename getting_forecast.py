from configures import *
import requests


def request_to_weather(lat, lng):
    hdrs = {'X-Yandex-API-Key': YANDEX_WEATHER_API_CODE}
    weather_request = 'https://api.weather.yandex.ru/v1/informers?lat={}&lon={}'.format(lat, lng)
    response_weather = requests.get(weather_request, headers=hdrs)
    json_response = response_weather.json()
    return json_response

