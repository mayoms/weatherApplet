__author__ = 'micah'

import weather
import datetime
from prettytable import PrettyTable


days_dict = {
    0:"Monday",
    1:"Tuesday",
    2:"Wednesday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday"
}

class WeatherApp(object):

    def __init__(self, city_data):

        self.city_data = city_data
        self.command_prompt = '>'
        self.city_object = None


    def command_loop(self):
        print 'Welcome to the Weather App. What would you like to do?'
        while True:
            command = raw_input(self.command_prompt).strip().lower()
            if command == 'help':
                self.help()
            elif command =='current':
                self.current()
            elif command == 'search':
                self.populate_city_object()
            elif command == 'forecast':
                self.forecast()
            elif command == 'weekend':
                self.forecast('weekend=True')
            elif command == 'quit':
                break
            else:
                print 'Command not found, try "help"'
                continue

    def help(self):
        print 'Commands: help, search, current, forecast, weekend, quit.'

    def populate_city_object(self):
        search_criteria = raw_input('Please enter city, region, country: ')
        if search_criteria:
            search_criteria = [w.strip() for w in search_criteria.split(',')]
            results = self.city_data.search(search_criteria)
            if results:
                if isinstance(results[0],tuple):
                    while True:
                        for itr, x in enumerate(results):
                            print str(itr+1), " ".join([i.capitalize() for i in x[:3]])
                        try:
                            choice = int(raw_input('Please select a city: ')) -1
                            results = results[choice]
                            break
                        except ValueError, IndexError:
                            print "Please choose a numeric value from the list."
                            continue
                self.city_object = weather.CityObject(weather.CityAttrs(*results))
                self.command_prompt = self.city_object.city_attrs.name + ',' + self.city_object.city_attrs.region + ' >'
                return
        print "No results found for '" + ' '.join(search_criteria) + "'."


    def current(self):

        if self.city_object:
            if not self.city_object.todays_weather:
                self.city_object.current_conditions()
            current_conditions = PrettyTable([self.city_object.city_attrs.name,
                                              self.city_object.city_attrs.region + ', ' + self.city_object.city_attrs.country])
            current_conditions.align = 'l'
            for key, value in self.city_object.todays_weather.iteritems():
                if key is not 'icon':
                    current_conditions.add_row([key, value])
            print current_conditions
            return
        print "No city selected, please 'search'."


    def forecast(self, weekend=None):
        if self.city_object:
            if not self.city_object.weekly_weather:
                self.city_object.weekly_forecast()
            if weekend:
                if datetime.datetime.now().weekday() in [5,6]:
                    gen = (day for day in self.city_object.weekly_weather[4:] if day.time.weekday() in [4,5,6])
                else:
                    gen = (day for day in self.city_object.weekly_weather if day.time.weekday() in [4,5,6])
            else:
                gen = (day for day in self.city_object.weekly_weather)
            seven_day_forecast = PrettyTable()
            seven_day_forecast.align = 'l'
            seven_day_forecast.add_column('',['Summary','Sunrise','Sunset','High','Low'])
            for object in gen:
                seven_day_forecast.add_column(days_dict[object.time.weekday()], [object.summary,
                                object.sunrise.time().strftime('%I:%M %p'), object.sunset.time().strftime('%I:%M %p'),
                                object.high_temp, object.low_temp])
            print seven_day_forecast
            return
        print "No city selected, please 'search'."

def main():

    app_instance = WeatherApp(weather.CityDataSearch(weather.PickleFileSerializer().open()))
    app_instance.command_loop()

if __name__ == '__main__':

    main()