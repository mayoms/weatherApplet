from serialize import PickleFileSerializer


class ReadCityData():
    def __init__(self, location_data, region_codes):

        self.location_data = location_data
        self.region_codes = region_codes
        self.serialized_data = {}

    def parse_country_state(self, city_geodata):

        # Reads file from Geonames (cities5000.txt) containing location data, parses for RegionID (In this case state)
        # Country Code, Latitude and Longitude
        if city_geodata[8] == 'us':
            return city_geodata[10], city_geodata[8], city_geodata[4], city_geodata[5]

        # If not in the united states, first get region name from admin1CodesASCII.txt, using region ID number
        # included in original file outside of the US, CA, GB, etc.. Also the result is reversed as a search of
        # Paris, FR is presumably more likely than Paris, Ile-de-france.
        try:
            region = self.region_codes[city_geodata[8] + '.' + city_geodata[10]]
        except KeyError:
            region = None
        return city_geodata[8], region, city_geodata[4], city_geodata[5]

    def deserialize_file(self):

        for line in self.location_data.readlines():
            line = line.lower().split('\t')
            if line[2] not in self.serialized_data:
                self.serialized_data[line[2]] = self.parse_country_state(line),
            else:
                self.serialized_data[line[2]] = (self.parse_country_state(line),) + self.serialized_data[line[2]]

        return self.serialized_data

def main():
    fh = open('admin1CodesASCII.txt', 'r')
    region_codes = {}
    for line in fh.readlines():
        line = line.lower().split('\t')
        region_codes[line[0]] =  line[2]
    fh.close()

    with open('cities5000.txt', 'r') as fh:
        city_data = PickleFileSerializer()
        city_data.save(ReadCityData(fh, region_codes).deserialize_file())

        opened_data = city_data.open()

        for key in opened_data:
            print key, opened_data[key]

if __name__ == '__main__':
    main()