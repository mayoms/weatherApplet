from serialize import PickleFileSerializer


class ReadCityData():
    def __init__(self, file_handler):

        self.file_handler = file_handler
        self.serialized_data = {}

    def parse_country_state(self, city_geodata):

        if city_geodata[8] == 'US':
            return city_geodata[10], city_geodata[4], city_geodata[5]
        return city_geodata[8], city_geodata[4], city_geodata[5]

    def deserialize_file(self):

        for line in self.file_handler.readlines():
            line = line.split('\t')
            if line[2] not in self.serialized_data:
                self.serialized_data[line[2]] = self.parse_country_state(line),
            else:
                self.serialized_data[line[2]] = (self.parse_country_state(line),) + self.serialized_data[line[2]]

        return self.serialized_data


def main():
    with open('cities5000.txt', 'r') as fh:
        city_data = PickleFileSerializer()
        city_data.save(ReadCityData(fh).deserialize_file())

        opened_data = city_data.open()

        for key in opened_data:
            print(key, opened_data[key])


if __name__ == '__main__':
    main()