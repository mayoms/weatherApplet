__author__ = 'micah'

from serialize import PickleFileSerializer
from collections import namedtuple
import forecastio
import pprint

APIKEY = '9ee79b186c41009279bf49c90f8bd8e4'

WeatherObject = namedtuple('WeatherObject', ['time','summary','icon','sunrise','sunset','high_temp','low_temp'])

class CityDataSearch(object):

    def __init__(self, ag_city_data):

        self.ag_city_data = ag_city_data

    def search(self, search_criteria):
        try:
            match = self.ag_city_data[search_criteria[0]]
            # If more than one city is found, and the user gave additional data we try to determine the correct city.
            if len(match) > 1 and len(search_criteria) > 1:
                deeper_search = self.determine_which_city(search_criteria, match)
                if deeper_search:
                    return search_criteria[0], tuple(deeper_search)
        # If a match is found or only one token given, return the Match or possible matches respectively.
            return search_criteria[0], match

        except KeyError:
            # If no match is found, return None.
            return None

    def determine_which_city(self, search_tokens, matches):
        # Creates a list, because even with multiple criteria more than one match can exist.
        possible_matches = []

        # Loop through and check for matches, depending on token count.

        for city_tup in matches:
            if set(search_tokens[1:]) == set(city_tup[:2]):
                return city_tup
            if set(search_tokens) & set(city_tup):
                possible_matches.append(city_tup)

        # If matches are found, return list of matches, otherwise return false.
        return possible_matches

class CityObject(object):

    def __init__(self, city_name, country, region, lat, lng):

        self.city_name = city_name
        self.region = region
        self.country = country
        self.lat = lat
        self.lng = lng

    @property
    def CurrentConditions(self):

        forecast = forecastio.load_forecast(APIKEY, self.lat, self.lng)
        currently = forecast.currently()

        return {
                "summary":currently.summary,
                "icon":currently.icon,
                "temperature": currently.temperature,
                "windspeed": currently.windSpeed,
                "humidity": currently.humidity,
                "pressure": currently.pressure,
                "rainchance": currently.precipProbability,
                "time": currently.time
                }

    @property
    def Forecast(self):
        forecast_data = []
        forecast = forecastio.load_forecast(APIKEY,self.lat, self.lng)
        daily = forecast.daily()
        for daily_data_point in daily.data[1:]:
            forecast_data.append(WeatherObject( daily_data_point.time, daily_data_point.summary,
                                                daily_data_point.icon, daily_data_point.sunriseTime,
                                                daily_data_point.sunsetTime, daily_data_point.temperatureMin,
                                                daily_data_point.temperatureMax))
        return forecast_data


search_criteria = [w.strip() for w in raw_input('Please enter city, region, country: ').split(',')]
city_location_dict = PickleFileSerializer().open()
city_search = CityDataSearch(city_location_dict)


results = city_search.search(search_criteria)

if results and len(results[1]) > 1:
    print 'Did you mean: '
    for itr, x in enumerate(results):
        print itr, x
    choice = int(raw_input('>'))
    chosen_city = CityObject(results[0],*results[1][choice])
elif len(results[1]) == 1:
    chosen_city = CityObject(results[0], *results[1][0])




pprint.pprint(chosen_city.CurrentConditions)

print "Forecast for " + chosen_city.city_name, chosen_city.region, chosen_city.country
for item in chosen_city.Forecast:
    print ', '.join(['{0}={1}'.format(k, getattr(item, k)) for k in item._fields])











