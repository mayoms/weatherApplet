__author__ = 'micah'

from jinja2 import Template
import weather



class WeatherWebApp(object):

    def __init__(self, city_data, search_criteria="Portland, OR, US"):
        self.city_data = city_data
        self.search_criteria = search_criteria
        self.city_object = None

    def run(self):
        if not self.city_object:
            self.populate_city_object()
        self.get_current_conditions()
        print self.build_pages()

    def build_pages(self):
        with open('idxtemplate.html','r') as fh:
            page_template = fh.read()

            template = Template(page_template)
            rendered = template.render(cityname = ', '.join([self.city_object.city_attrs.name.capitalize(),
                                                             self.city_object.city_attrs.region.upper()]),
                                     summary = self.city_object.todays_weather['summary'],
                                     rainchance = self.city_object.todays_weather['rainchance'], \
                                     temperature = self.city_object.todays_weather['temperature'], \
                                     humidity = self.city_object.todays_weather['humidity'], \
                                     pressure = self.city_object.todays_weather['pressure'], \
                                     windspeed = self.city_object.todays_weather['windspeed'] )

            return rendered

    def populate_city_object(self):
        if self.search_criteria:
            self.search_criteria = [w.strip().lower() for w in self.search_criteria.split(',')]
            results = self.city_data.search(self.search_criteria)
            if results:
                self.city_object = weather.CityObject(weather.CityAttrs(*results))

    def get_current_conditions(self):
        self.city_object.current_conditions()





def main():
    app_instance = WeatherWebApp(weather.CityDataSearch(weather.PickleFileSerializer().open()))
    app_instance.run()


if __name__ == '__main__':
    main()





