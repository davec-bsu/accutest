import requests
import configparser


# get the API kiey from the config file and return it to the caller.
#
def get_apikey():
    config = configparser.ConfigParser()
    config.read('app.config')
    apikey_from_file = config['secrets']['apikey']
    print(apikey_from_file)
    return apikey_from_file


class NoSuchLocation(Exception):
    pass


def get_location():
    location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                'postalcodes/search?apikey=APIKEYGOESHERE&q=02324'

    response = requests.get(location_url)

    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


def get_conditions(key, api_key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' \
        '{}?apikey={}'.format(key, api_key)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))


try:
    apikey = get_apikey()
    location_key = get_location()
    get_conditions(location_key)
except NoSuchLocation:
    print("Unable to get the location")
