"""
Testing temperature.py
"""
import temperature
from temperature.data_science_files.temperature import Temperature
import unittest
CITIES_DATABASE_FILE = "temperature/data_science_files/data/worldcities.csv"
USER_LOCATIONS = ["Berlin", "Leipzig"]
DATE_OF_REQUEST = "2021-10-17"
class TestTemperature(unittest.TestCase):
    """
    We use TestCase of the unittest package
    to take advantage of the many easy to use
    methods in the class
    """
    def _get_object(self,
                    locations_file=CITIES_DATABASE_FILE, 
                    user_locations=USER_LOCATIONS,
                    date_of_request=DATE_OF_REQUEST):
        """
        Get the temperature object
        """
        return Temperature(locations_file, 
                           user_locations,
                           date_of_request)
    def test_for_correct_instances(self):
        """
        Testing correct instances
        """
        temp_obj = self._get_object()
        for instance in range(1, 6):
            temp_obj.confirm_instances(instance)
            expected = 'This class displays temperature for these locations: [Berlin, Leipzig,]'
            self.assertEqual(expected, temp_obj.__repr__())
        return temp_obj
    def _testing_instances(self,
                           assert_message,
                           method_name,
                           locations_file=CITIES_DATABASE_FILE,
                           user_locations=USER_LOCATIONS,
                           date_of_request=DATE_OF_REQUEST):
        """
        internal method for testing instances
        """
        temp_obj = self._get_object(locations_file, user_locations, date_of_request)
        for instance in range(1, 6):
            try:
                try:
                    temp_obj.__repr__()
                except:
                    "Representation not possible all instances wrong type"
                temp_obj.confirm_instances(instance)
            except:
                print(f'\nInstance {instance}  in {method_name} handled well by TestCase')
                with self.assertRaises(ValueError) as error:
                    temp_obj.confirm_instances(instance)
                self.assertEqual(assert_message, str(error.exception))
    def test_wrong_type_locations_file(self):
        """
        Test wrong locations file
        """
        locations_file = {"file": CITIES_DATABASE_FILE}
        self._testing_instances(assert_message="A string is required as path to locations file",
                                method_name="test_wrong_type_locations_file",
                                locations_file=locations_file)
    def test_wrong_user_locations(self):
        """
        Test error for wrong type user_locations
        """
        user_locations = {"file": USER_LOCATIONS}
        self._testing_instances(assert_message="Requested locations should be a list",
                                method_name="test_wrong_user_locations",
                                user_locations=user_locations)
    def test_wrong_type_date(self):
        """
        When date is of wrong type
        """
        date = 2021-10-22
        self._testing_instances(assert_message=f'{date} not a string in the format YYYY-mm-dd',
                                method_name="test_wrong_type_date",
                                date_of_request=date)
    def test_unusual_date_format(self):
        """
        When date is not in the format YYYY-MM-DD
        """
        date = "21-10-22"
        self._testing_instances(assert_message=f'{date} not a string in the format YYYY-mm-dd',
                                method_name="test_wrong_type_date",
                                date_of_request=date)
    def test_at_least_user_location_not_string(self):
        """
        Test for a list of user locations when at least
        one is not a string
        """
        user_locations = ["Berlin", "Dresden", 9414, "Karlsruhe", "Mannheim"]
        self._testing_instances(assert_message= "9414 not a string",
                                method_name="test_at_least_user_location_not_string",
                                user_locations=user_locations)
    def test_convert_to_ascii(self):
        """
        Testing if we can convert accents to ascii
        """
        requested_locations = ["Düsseldorf", "Münich", "Köln", "Karlsruhe", "Mainz"]
        temp_obj = Temperature(CITIES_DATABASE_FILE, requested_locations, DATE_OF_REQUEST)
        expected = ["Dusseldorf", "Munich", "Koln", "Karlsruhe", "Mainz"]
        self.assertEqual(expected, temp_obj.convert_user_locations_to_ascii())
    def test_valid_and_invalid_stations(self):
        """
        Testing for valid and invalid stations
        """
        user_stations = ["Stuttgart", "Hannover", "Kiel", "Berlin", "Rome", "Zagreb", "Bucharest"]
        temp_obj = Temperature(locations_file=CITIES_DATABASE_FILE,
                               requested_locations=user_stations,
                               date_of_request=DATE_OF_REQUEST)
        inv_val_stns = temp_obj.identify_valid_and_invalid_locations()
        inv_expected = sorted(["Rome", "Zagreb", "Bucharest"])
        val_expected = sorted(["Stuttgart", "Hannover", "Kiel", "Berlin"])
        inv_actual = [i.title() for i in sorted(inv_val_stns["invalid_locations"])]
        val_actual = [i.title() for i in sorted(inv_val_stns["valid_locations"])]
        self.assertEqual(val_expected, val_actual)
        self.assertEqual(inv_expected, inv_actual)
    def test_raise_error_if_all_locations_unrecognized(self):
        """
        Testing error for unrecognized locations
        """
        user_locations = ["Nairobi", "Stockholm", "Bucharest", "Jakarta"]
        temp_obj = Temperature(CITIES_DATABASE_FILE, user_locations, DATE_OF_REQUEST)
        with self.assertRaises(Exception) as error:
            temp_obj.raise_error_if_all_locations_unrecognized()
        self.assertEqual("['nairobi', 'stockholm', 'bucharest', 'jakarta'] not recognized", str(error.exception))
    def test_get_geocoordinates(self):
        """
        Testing geocoordinates
        """
        geo_coords = self.test_for_correct_instances().get_geocoordinates()
        expected = {'berlin': {'lon': 13.3833, 
                               'lat': 52.5167},
                    'leipzig': {'lon': 12.3833, 
                                'lat': 51.3333}
                    }
        self.assertEqual(expected, geo_coords)
    def test_temperature_data_when_expected(self):
        """
        Testing temperature data when we actually
        expect it to be present
        """
        temperature_data = self._get_object().get_temperature_data()
        expected_column_names = sorted(["Berlin", "Leipzig"])
        actual_column_names = sorted([i for i in temperature_data.columns])
        self.assertEqual(expected_column_names, actual_column_names)
        actual_values = [i for i in temperature_data.loc["2021-10-17 07:00:00+00:00"]]
        print(actual_values)
        expected_values = [6.4, 5.6]
        self.assertEqual(expected_values, actual_values)
    def test_404_error_when_data_not_available(self):
        """
        Test that a 404 error is flagged if no data in the API
        """
        actual_flag = self._get_object(date_of_request="2024-10-22").get_temperature_data()
        expected_flag = {"status": 404, "Detail": 'date not in range'}
        self.assertEqual(expected_flag, actual_flag)
        
        
        
    
        
        
        
        

        
        
        
