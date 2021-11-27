"""
We need to create tests for the temperature.py
file to make sure that changes in future are
detectable in case of a collaboration.
We shall write a class that inherits from TestCase
of the unittest package to take advantage of the
many elegant testing functionalities in the package.
Google 'unittest Testcase' for documentation
We shall remain guided by pylint to keep the file
to the PEP standard
"""
# pylint: disable=C0301
# pylint: disable=W0102
# pylint: disable=R0913
# pylint: disable=W0702
import unittest
from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    This test class inherits from TestCase methods
    of the unittest
    """
    CITIES_DB_FILE = "temperature/data_science_files/data/worldcities.csv"
    USER_CITIES = ["Berlin", "Leipzig", "Cologne", "Dortmund", "Karlsruhe"]
    DATE_OF_REQUEST = "2021-10-18"
    ASSERT_MESSAGE = "This class displays temperature for these locations: [Berlin, Leipzig, Cologne, Dortmund, Karlsruhe,]"
    def _testing_instances(self,
                           locations_file=CITIES_DB_FILE,
                           requested_locations=USER_CITIES,
                           date_of_request=DATE_OF_REQUEST,
                           assert_message=ASSERT_MESSAGE,
                           is_all_correct_instance=True):
        """
        Internal method for testing instances
        """
        temp_obj = Temperature(locations_file,
                               requested_locations,
                               date_of_request)
        if is_all_correct_instance:
            self.assertEqual(assert_message, str(temp_obj))
        else:
            for instance in range(1, 6):
                try:
                    temp_obj.confirm_instances(instance)
                except:
                    with self.assertRaises(ValueError) as error:
                        temp_obj.confirm_instances(instance)
                    self.assertEqual(assert_message, str(error.exception))
        return temp_obj
    def test_confirm_correct_instances(self):
        """
        Testing that the default attributes
        are actually of the right instance (type)
        """
        self._testing_instances()
    def test_wrong_type_locations_file(self):
        """
        Deliberately change the type of locations
        file
        """
        locations_file = {"locations_file": TestTemperature.CITIES_DB_FILE}
        assert_message = "A string is required as path to locations file"
        self._testing_instances(locations_file=locations_file,
                                assert_message=assert_message,
                                is_all_correct_instance=False)
    def test_wrong_type_requested_locations(self):
        """
        Deliberately change the type of user requested
        locations
        """
        user_locations = {"user_locations": TestTemperature.USER_CITIES}
        assert_message = "Requested locations should be a list"
        self._testing_instances(requested_locations=user_locations,
                                assert_message=assert_message,
                                is_all_correct_instance=False)
    def test_wrong_type_date(self):
        """
        Deliberately change the type of given date
        """
        date = {"date": TestTemperature.DATE_OF_REQUEST}
        assert_message = f"{date} not a string in the format YYYY-MM-DD"
        self._testing_instances(date_of_request=date,
                                assert_message=assert_message,
                                is_all_correct_instance=False)
    def test_wrong_type_requested_location_item(self):
        """
        Test if every item in user given locations is a string
        """
        user_locations = ["Berlin", "Karlsruhe", "Stuttgart", 79241]
        assert_message = "79241 not a string"
        self._testing_instances(requested_locations=user_locations,
                                assert_message=assert_message,
                                is_all_correct_instance=False)
    def test_date_integer_instance(self):
        """
        Deliberately setting a date to be an integer
        to trigger error
        """
        date = 2021-10-25
        assert_message = f'{date} not a string in the format YYYY-MM-DD'
        self._testing_instances(date_of_request=date,
                                assert_message=assert_message,
                                is_all_correct_instance=False)
    def test_convert_user_locations_to_ascii(self):
        """
        Test if accents can be converted to ascii
        """
        user_locations = ["Münich", "Berlin", "Düsseldorf", "Köln", "Frankfurt"]
        assert_message = "This class displays temperature for these locations: [Münich, Berlin, Düsseldorf, Köln, Frankfurt,]"
        obj = self._testing_instances(assert_message=assert_message,
                                      requested_locations=user_locations,
                                      is_all_correct_instance=True)
        expected = ["Munich", "Berlin", "Dusseldorf", "Koln", "Frankfurt"]
        self.assertEqual(expected, obj.convert_user_locations_to_ascii())
    def test_identify_valid_and_invalid_locations(self):
        """
        Test for valid and invalid locations
        """
        user_locations = ["Berlin", "Rome", "Toulouse", "Zagreb", "Bucharest", "Frankfurt"]
        assert_message = "This class displays temperature for these locations: [Berlin, Rome, Toulouse, Zagreb, Bucharest, Frankfurt,]"
        obj = self._testing_instances(requested_locations=user_locations,
                                      assert_message=assert_message,
                                      is_all_correct_instance=True)
        expected_valid = sorted(["Berlin", "Frankfurt"])
        expected_invalid = sorted(["Rome", "Toulouse", "Zagreb", "Bucharest"])
        actual_valid = [i.title() for i in sorted(obj.identify_valid_and_invalid_locations()["valid_locations"])]
        actual_invalid = [i.title() for i in sorted(obj.identify_valid_and_invalid_locations()["invalid_locations"])]
        self.assertEqual(expected_valid, actual_valid)
        self.assertEqual(expected_invalid, actual_invalid)
    def test_error_for_unrecognized_locations(self):
        """
        Raise error if all stations are unrecognized
        """
        user_locations = ["Nairobi", "Kampala", "Jakarta"]
        assert_message = "This class displays temperature for these locations: [Nairobi, Kampala, Jakarta,]"
        obj = self._testing_instances(assert_message=assert_message,
                                      requested_locations=user_locations,
                                      is_all_correct_instance=True)
        with self.assertRaises(Exception) as error:
            obj.raise_error_if_all_locations_unrecognized()
        self.assertEqual("['nairobi', 'kampala', 'jakarta'] not recognized", str(error.exception))
    def test_get_geocoordinates(self):
        """
        testing for geocoordinates for berlin
        """
        geo_coords = self._testing_instances().get_geocoordinates()
        expected_berlin_coords = {"lon": 13.3833, "lat": 52.5167}
        actual_berlin_coords = geo_coords["berlin"]
        self.assertEqual(expected_berlin_coords, actual_berlin_coords)
    def test_api_has_temperature_data(self):
        """
        Testing that API has temperature data
        """
        temp_data = self._testing_instances().get_temperature_data()
        expected_column_names = TestTemperature.USER_CITIES
        actual_column_names = [str(i) for i in temp_data.columns]
        for expected, actual in zip(expected_column_names, actual_column_names):
            self.assertEqual(expected, actual)
    def test_weather_api_no_data(self):
        """
        When weather api has found no data
        """
        date = "2024-09-22"
        expected_message = {"status": 404, "Detail": "date not in range"}
        status_message = self._testing_instances(date_of_request=date).get_temperature_data()
        self.assertEqual(expected_message, status_message)
        