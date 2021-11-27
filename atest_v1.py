"""
All tests for this App belong here
"""
import unittest
if __name__ == '__main__':
    from temperature import Temperature
else:
    from temperature.data_science_files.temperature import Temperature
    ALL_LOCATIONS_DB_FILE = "temperature/data_science_files/data/worldcities.csv"
class TestTemperature(unittest.TestCase):
    """
    We inherit from unittest.TestCase to take advantage
    of the large pool of testing capabilities inherent
    there
    """
    def test_for_full_arguments(self):
        obj = Temperature("my_file", ["berlin", "hamburg"], "2021-10-22")
        expected = f"This class displays temperature for these locations: [berlin, hamburg,]"
        self.assertEqual(expected, obj.__repr__())
    def test_partial_arguments(self):
        with self.assertRaises(Exception) as e:
            Temperature(locations_file="Some/path/to/file")
            self.assertTrue("Too few arguments given")
    def test_instances(self):
        """
        Test instances and date format
        """
        obj = Temperature(85412, {"locations": ["berlin", "karlsruhe", "stuttgart"]}, "22-10-22")
        with self.assertRaises(ValueError):
            obj.confirm_instances(1)
            self.assertTrue("Location file should be a string")
        with self.assertRaises(ValueError):
            obj.confirm_instances(2)
            self.assertTrue("Requested locations should be a list")
        obj = Temperature(85412, ["karlsruhe", 2421, {"temp": 22}], "22-10-22")
        with self.assertRaises(ValueError):
            obj.confirm_instances(3)
            self.assertTrue("Each item in requested locations should be a string")
        obj = Temperature(85412, ["karlsruhe", 2421, {"temp": 22}], 22342)   
        with self.assertRaises(ValueError):
            obj.confirm_instances(4)
            self.assertTrue("Date must be a string")
        obj = Temperature(85412, ["karlsruhe", 2421, {"temp": 22}], "22-10-22")  
        with self.assertRaises(ValueError):
            obj.confirm_instances(5)
            self.assertTrue("Date must be a 10 character string in the format YYYY-mm-dd")
        
    def test_ascii_conversion(self):
        """
        Accents to ascii tests
        """
        user_locations = ["berlin", "köln", "münchen", "düsseldorf"]
        obj = Temperature("/path/to/file", user_locations, "some_date")
        expected_list = ["berlin", "koln", "munchen", "dusseldorf"]
        actual_list = obj.convert_user_locations_to_ascii()
        for expected, actual in zip(expected_list, actual_list):
            self.assertEqual(expected, actual)
    def test_read_world_cities_from_db(self):
        """
        Test if we can read from database
        """
        locations = ["Karlsruhe"]
        date = "some_date"
        expected_n_columns = 11
        expected_n_rows = 41001
        table = Temperature(ALL_LOCATIONS_DB_FILE, locations, date).read_world_cities_from_database()
        expected_latitude = 49.0167
        actual_latitude = [i-0 for i in table[table["city_ascii"] == locations[0]]["lat"]][0]
        self.assertEqual(expected_n_columns, len(table.columns))
        self.assertEqual(expected_n_rows, len(table))
        self.assertEqual(expected_latitude, actual_latitude) 
    def test_valid_and_invalid_locations(self):
        """
        testing if valid/invalid cities can be flushed out!
        """
        user_locations = ["Berlin", "Nairobi", "Los Angeles", "Karlsruhe", "Stuttgart", "Dortmund"]
        date = "some_date"
        temp_obj = Temperature(ALL_LOCATIONS_DB_FILE, user_locations, date)
        temp_obj.identify_valid_and_invalid_locations()
        invalids = sorted(["Nairobi", "Los Angeles"])
        valids = sorted(["Berlin", "Karlsruhe", "Stuttgart", "Dortmund"])
        result_dict = temp_obj.identify_valid_and_invalid_locations()
        actual_invalids = sorted([i.title() for i in result_dict["invalid_locations"]])
        actual_valids = sorted([i.title() for i in result_dict["valid_locations"]])        
        for invalid, actual_invalid in zip(invalids, actual_invalids):
            self.assertEqual(invalid, actual_invalid)
        for valid, actual_valid in zip(valids, actual_valids):
            self.assertEqual(valid, actual_valid)
    def test_raise_exception_for_all_cities_unrecognized(self):
        """
        Can an exception be raised if all cities are unrecognized?
        """
        user_cities = ["Rome", "Kingston", "Lagos", "Jakarta", "Zagreb"]
        date = "some_date"
        temp_obj = Temperature(ALL_LOCATIONS_DB_FILE, user_cities, date)
        with self.assertRaises(Exception):
            temp_obj.raise_error_if_all_locations_unrecognized()
    def test_geocoordinates(self):
        """
        Testing geocoordinates
        """
        user_locations = ["Leipzig", "Berlin"]
        date = "some_date"
        temp_obj = Temperature(ALL_LOCATIONS_DB_FILE, user_locations, date)
        expected_geo_coordinates = {'berlin': {'lon': 13.3833, 'lat': 52.5167},
                                    'leipzig': {'lon': 12.3833, 'lat': 51.3333}}
        self.assertEqual(expected_geo_coordinates, temp_obj.get_geocoordinates())
    def test_get_temperature_data_for_available_data(self):
        """
        testing if we can get temperature data for available
        """
        user_locations = ["Leipzig", "Berlin"]
        date = "2021-09-15"
        temp_obj = Temperature(ALL_LOCATIONS_DB_FILE, user_locations, date)
        temp_data = temp_obj.get_temperature_data()
        self.assertEqual([i for i in temp_data.columns], user_locations)
        self.assertEqual([len(temp_data)][0], 25)
        self.assertEqual(str(temp_data.index[0]), "2021-09-15 00:00:00+00:00")
        self.assertEqual(str(temp_data.index[-1]), "2021-09-16 00:00:00+00:00")
    def test_for_404_error_message(self):
        """
        In case there is no data in the API, we expect
        a 404 message
        """
        user_locations = ["Leipzig", "Berlin"]
        date = "2022-09-15"
        temp_obj = Temperature(ALL_LOCATIONS_DB_FILE, user_locations, date)
        status_message = temp_obj.get_temperature_data()
        self.assertEqual(status_message["status"], 404)
        self.assertEqual(status_message["Detail"], "date not in range")
        
        
        


        
        

        
        
        
        
        
        
        
        
        
        
        
        
        


            
        
        