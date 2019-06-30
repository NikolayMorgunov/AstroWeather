import requests


def exist(country, city):
    country = '+'.join(country.split())
    country = country + ',+'
    city = city.split()
    city = '+'.join(city)
    address = country + city
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(address)
    response_geo = requests.get(geocoder_request)
    json_response = response_geo.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    for i in toponym:
        if i['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] == 'locality':
            return True
    return False


def coords(country, city):
    country = '+'.join(country.split())
    country = country + ',+'
    city = city.split()
    city = '+'.join(city)
    address = country + city
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(address)
    response_geo = requests.get(geocoder_request)
    json_response = response_geo.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    for i in toponym:
        if i['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] == 'locality':
            return i['GeoObject']['Point']['pos'].split()


# print(coords('russia', 'feodosia'))
