import requests
import json
from lab_2_tbot import config


def get_nearbys(latitude, longitude, radius=300, tag='pharmacy'):
    url = "https://eu1.locationiq.com/v1/nearby.php"

    data = {
        'key': config.LOCATIONIQ_TOKEN,
        'lat': latitude,
        'lon': longitude,
        'tag': tag,
        'radius': radius,
        'format': 'json',
        'extratags': 1
    }

    response = requests.get(url, params=data)
    return json.loads(response.text)


def get_address(latitude, longitude):
    url = "https://us1.locationiq.com/v1/reverse.php"

    data = {
        'key': config.LOCATIONIQ_TOKEN,
        'lat': latitude,
        'lon': longitude,
        'format': 'json'
    }

    response = requests.get(url, params=data)
    return json.loads(response.text)