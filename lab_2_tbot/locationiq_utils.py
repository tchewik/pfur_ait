import json
import time

import config
import requests


def get_nearbys(latitude, longitude, radius=300, tag="pharmacy"):
    url = "https://eu1.locationiq.com/v1/nearby.php"

    data = {
        "key": config.LOCATIONIQ_TOKEN,
        "lat": latitude,
        "lon": longitude,
        "tag": tag,
        "radius": radius,
        "format": "json",
        "extratags": 1
    }

    response = requests.get(url, params=data)
    return json.loads(response.text)


def get_address(latitude, longitude):
    url = "https://us1.locationiq.com/v1/reverse.php"

    data = {
        "key": config.LOCATIONIQ_TOKEN,
        "lat": latitude,
        "lon": longitude,
        "format": "json"
    }

    response = requests.get(url, params=data)
    try:
        return json.loads(response.text)["address"]
    except KeyError:
        return None


def format_address(json_address):
    res = []
    for key in ["postcode", "state", "road", "house_number"]:
        try:
            res.append(json_address[key])
        except KeyError:
            continue
    return ",".join(res)


with open('data/base_drugstores_supermarkets.csv', "r") as base:
    with open("data/temp_base.csv", "a+") as temp_base:
        _counter = 0
        for line in base.readlines():
            splitted_line = line.split(",")
            name = ''.join(splitted_line[:-2])
            latitude, longitude = splitted_line[-2:]
            json_address = get_address(latitude, longitude)
            if json_address:
                temp_line = "\t".join([name,
                                       latitude,
                                       longitude[:-1],
                                       format_address(json_address)]) + "\n"
                temp_base.write(temp_line)
            else:
                with open("data/temp_base_no_addresses.csv", "a+") as void_base:
                    temp_line = "\t".join([name,
                                           latitude,
                                           longitude])
                    void_base.write(temp_line)

            time.sleep(1.001)
            _counter += 1
            if _counter % 150 == 0:
                print("Processed the line %d" % _counter)
