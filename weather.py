__author__ = 'micah'

from serialize import PickleFileSerializer

class CityDataSearch(object):

    def __init__(self, ag_city_data):

        self.ag_city_data = ag_city_data

    def search(self, search_criteria):
        try:
            match = self.ag_city_data[search_criteria[0]]
            
            # If more than one city is found, we try to determine the correct city.
            
            if len(match) > 1:
                # If the user gave more than one token (region or country) we can use determine_which_city
                # to try and find a match.

                if len(search_criteria) > 1:
                    deeper_search = self.determine_which_city(search_criteria, match)
                    # If deeper_search is not False, then we return a tuple of the match or possible matches.
                    if deeper_search:
                        return tuple(deeper_search)
                    # If deeper search is False, return the whole list to give users options.
                    return match
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
            if set(search_tokens[1:]) == set(city_tup[:2]):
                return city_tup
            if set(search_tokens) & set(city_tup):
                possible_matches.append(city_tup)

        # If matches are found, return list of matches, otherwise return false.

        if possible_matches:
            return possible_matches
        return False


search_criteria = [w.strip() for w in raw_input("Please enter city, region, country: ").split(',')]
city_location_dict = PickleFileSerializer().open()
city_search = CityDataSearch(city_location_dict)


print city_search.search(search_criteria)


