__author__ = 'micah'

from serialize import PickleFileSerializer
from collections import namedtuple
import forecastio

APIKEY = 'apikey'

CityAttrs = namedtuple('City', ['name', 'country', 'region', 'lat', 'lng'])
WeatherObject = namedtuple('WeatherObject', ['time','summary','icon','sunrise','sunset','high_temp','low_temp'])

class CityDataSearch(object):

    def __init__(self, ag_city_data):

        self.ag_city_data = ag_city_data

    def search(self, search_criteria):
        try:
            match = self.ag_city_data[search_criteria[0]]
            # If more than one city is found, and the user gave additional data we try to determine the correct city.
            if len(match) > 1 and len(search_criteria) > 1:
                deeper_search = self.determine_which_city(search_criteria[1:], match)
                if deeper_search:
                    return deeper_search if len(deeper_search) > 1 else deeper_search[0]
        # If a match is found or only one token given, return the Match or possible matches respectively.
            return match

        except KeyError:
            # If no match is found, return None.
            return None

    def determine_which_city(self, search_tokens, matches):
        # Creates a list, because even with multiple criteria more than one match can exist.
        possible_matches = []

        # Loop through and check for matches, depending on token count.

        for city_tup in matches:
            if set(search_tokens) == set(city_tup[1:3]):
                return city_tup
            if set(search_tokens) & set(city_tup):
                possible_matches.append(city_tup)

        # If matches are found, return list of matches, otherwise return false.
        return possible_matches

class CityObject(object):

    def __init__(self, city_attrs):

        self.city_attrs = city_attrs
        self.todays_weather = None
        self.weekly_weather = []

    def current_conditions(self):

        forecast = forecastio.load_forecast(APIKEY, self.city_attrs.lat, self.city_attrs.lng)
        currently = forecast.currently()

        self.todays_weather= \
            {
                "summary":currently.summary,
                "icon":currently.icon,
                "temperature": currently.temperature,
                "windspeed": currently.windSpeed,
                "humidity": currently.humidity,
                "pressure": currently.pressure,
                "rainchance": currently.precipProbability,
                "time": currently.time
                }

    def weekly_forecast(self):
        forecast_data = []
        forecast = forecastio.load_forecast(APIKEY,self.city_attrs.lat, self.city_attrs.lng)
        daily = forecast.daily()
        for daily_data_point in daily.data[1:]:
            self.weekly_weather.append(WeatherObject( daily_data_point.time, daily_data_point.summary,
                                                daily_data_point.icon, daily_data_point.sunriseTime,
                                                daily_data_point.sunsetTime,daily_data_point.temperatureMax,
                                                daily_data_point.temperatureMin))



if __name__ == '__main__':
    main()