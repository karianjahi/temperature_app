"""
Create a class that reads in a Weather API and displays
temperature data in form of a table/map
"""
# pylint: disable=C0301
# pylint: disable=E0611
# pylint: disable=E0401
# pylint: disable=R1721
import requests
import pandas as pd

#from utils import convert_special_german_accents_into_ascii as to_ascii
# switch here for plot demos!
from temperature.data_science_files.utils import convert_special_german_accents_into_ascii as to_ascii
# from utils import convert_special_german_accents_into_ascii as to_ascii
class Temperature:
    """
    This is the class whose methods are going to
    generate the temperature table/map
    """
    def __init__(self, locations_file:str,
                 requested_locations:list,
                 date_of_request:str):
        """
        Constructor class
        """
        self.locations_file = locations_file
        self.requested_locations = requested_locations
        self.date_of_request = date_of_request
    def confirm_instances(self, instance_count):
        """
        The given arguments should conform
        to required instances
        instance_count:  a number denoting which instance is
        being tested. 
        1 for the path to the database locations table 
        2 and 3 for requested locations
        4 and 5 for date
        """
        if instance_count == 1:
            if not isinstance(self.locations_file, str):
                raise ValueError("A string is required as path to locations file")
        if instance_count == 2:
            if not isinstance(self.requested_locations, list):
                raise ValueError("Requested locations should be a list")
        if instance_count == 3:
            if isinstance(self.requested_locations, list):
                for item in self.requested_locations:
                    if not isinstance(item, str):
                        raise ValueError(f'{item} not a string')
        if instance_count == 4:
            if isinstance(self.date_of_request, int):
                raise ValueError( f'{self.date_of_request} cannot be an integer')
            elif not isinstance(self.date_of_request, str):
                    raise ValueError(f'{self.date_of_request} must be a string')
            else:
                date_splits = self.date_of_request.split("-")
                year_length = len(date_splits[0])
                mon_length = len(date_splits[1])
                day_length = len(date_splits[2])
                if year_length != 4 or mon_length != 2 or day_length !=2:
                    raise ValueError(f'{self.date_of_request} is not in the format YYYY-MM-DD')
    def __repr__(self):
        """
        class representation
        """
        for instance in range(1, 5):
            self.confirm_instances(instance)
        locations = ""
        for location in self.requested_locations:
            locations = locations + " " + location
        return f'locations are: {locations.strip()}'
    def convert_user_locations_to_ascii(self):
        """
        Remove German accents and replace with ascii
        """
        return [to_ascii(location) for location in self.requested_locations]
    def read_world_cities_from_database(self):
        """
        read location database
        return dataframe
        """
        return pd.read_csv(self.locations_file)
    def select_german_locations_only_from_database(self):
        """
        Limit locations database table to Germany only
        return dataframe table
        """
        table = self.read_world_cities_from_database()
        table["location"] = [i.lower() for i in table["city_ascii"]]
        return table[table["country"] == "Germany"]
    def identify_valid_and_invalid_locations(self):
        """
        considers only cities in Germany
        return dictionary of valid and invalid locations
        """
        database_locations = [i for i in self.select_german_locations_only_from_database()["location"]]
        valid_locations = []
        invalid_locations = []
        for location in self.convert_user_locations_to_ascii():
            location = location.lower()
            if location in database_locations:
                valid_locations.append(location)
            else:
                invalid_locations.append(location)
        return {
            "valid_locations": valid_locations,
            "invalid_locations": invalid_locations
            }
    def raise_error_if_all_locations_unrecognized(self):
        """
        Before we can request temperature data for the given locations,
        we need to ensure that we have at least one valid location.
        An exception should be raised otherwise
        """
        locations = self.identify_valid_and_invalid_locations()
        if locations["valid_locations"] == []:
            raise Exception(f'{locations["invalid_locations"]} not recognized')
    def get_geocoordinates(self):
        """
        Longitudes and latitudes for each location
        return a dictionary.
        """
        self.raise_error_if_all_locations_unrecognized()
        locations_table = self.select_german_locations_only_from_database()
        geocoordinates_dict = {}
        valid_locations = self.identify_valid_and_invalid_locations()["valid_locations"]
        for location in valid_locations:
            geocoords = locations_table[locations_table["location"] == location][["lat", "lng"]]
            geocoordinates_dict[location] = {"lon": list(geocoords["lng"])[0],
                                             "lat": list(geocoords["lat"])[0]}
        return geocoordinates_dict
    def get_temperature_data(self):
        """
        Get weather API for each of the valid locations
        return dataframe
        """
        for instance in range(1, 5):
            self.confirm_instances(instance)
        geocodes_dict = self.get_geocoordinates()
        temperature_table_list = []
        for location in geocodes_dict:
            lon = geocodes_dict[location]["lon"]
            lat = geocodes_dict[location]["lat"]
            request_in_json = self.get_weather_api_for_single_location(lon,
                                                                       lat,
                                                                       self.date_of_request)
            if "title" in request_in_json:
                if request_in_json["title"] == "404 Not Found":
                    return {"status": 404, "Detail": "date not in range"}
            weather_api_list = request_in_json["weather"]
            timestamp = []
            temperature = []
            for item in weather_api_list:
                timestamp.append(item["timestamp"])
                temperature.append(item["temperature"])
            location_temp_table = pd.DataFrame({"time": timestamp,
                                                location: temperature})
            location_temp_table.set_index("time", inplace=True)
            location_temp_table.index = pd.to_datetime(location_temp_table.index)
            temperature_table_list.append(location_temp_table)
        results_table = pd.concat(temperature_table_list, axis=1)
        results_table.columns = [i.title() for i in results_table.columns]
        return results_table
    @staticmethod
    def get_weather_api_for_single_location(lon, lat, date):
        """
        Given lon and lat, get weather API
        from brightsky for a single location
        """
        api_url = f'https://api.brightsky.dev/weather?lat={lat}&lon={lon}&date={date}'
        return requests.get(api_url).json()
# if __name__ == '__main__':
#     LOCATION_FILE = "temperature/data_science_files/data/worldcities.csv"
#     REQUESTED_LOCATION = ["Nairobi", "Los Angeles", "Berlin"]
#     DATE_OF_REQUEST = "2021-11-16"
#     OBJ = Temperature(LOCATION_FILE, REQUESTED_LOCATION, DATE_OF_REQUEST)
#     print(OBJ.identify_valid_and_invalid_locations())
