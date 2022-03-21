"""
Testing temperature.py file
"""
# pylint: disable=W0102
# pylint: disable=R0913
import unittest
from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    By inheriting TestCase, we now have all the test
    methods that we intend to use
    """
    LOCATIONS_FILE = "temperature/data_science_files/data/worldcities.csv"
    REQUESTED_USER_CITIES = ["Berlin", "Hannover", "Hamburg", "Karlsruhe"]
    DATE_OF_REQUEST = "2021-10-24"
    EXPECTED_ASSERT_MESSAGE = "locations are: Berlin Hannover Hamburg Karlsruhe"
    def test_correct_instances(self):
        """
        In this case, we only want to
        confirm that no error is issued
        when we supply the right instances
        """
        self._testing_instances()
    def test_wrong_type_locations_file(self):
        """
        We deliberately supply a locations file that is not a string
        """
        locations_file = {"locations_file": TestTemperature.LOCATIONS_FILE}
        expected_assert_message = "A string is required as path to locations file"
        self._testing_instances(locations_file=locations_file,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def test_wrong_type_requested_locations(self):
        """
        Deliberately supply the wrong locations type
        """
        requested_cities = {"requested_locations": TestTemperature.REQUESTED_USER_CITIES}
        expected_assert_message = "Requested locations should be a list"
        self._testing_instances(requested_locations=requested_cities,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def test_requested_locations_single_item_string(self):
        """
        Here we deliberately make on member of the user cities
        an integer and catch the error
        """
        requested_cities = ["Berlin", "Cologne", "Konstanz", 924144]
        expected_assert_message = "924144 not a string"
        self._testing_instances(requested_locations=requested_cities,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def test_date_integer(self):
        """
        The date cannot be an integer
        """
        date_of_request = 20211022
        expected_assert_message = f'{date_of_request} cannot be an integer'
        self._testing_instances(date_of_request=date_of_request,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def test_date_not_string_and_not_integer(self):
        """
        Deliberately make date a non-string
        """
        date_of_request = {"date_of_request": TestTemperature.DATE_OF_REQUEST}
        expected_assert_message = f'{date_of_request} must be a string'
        self._testing_instances(date_of_request=date_of_request,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def test_date_wrong_length(self):
        """
        Deliberately shorten the length of date string
        """
        date_of_request = "21-10-22"
        expected_assert_message = f"{date_of_request} is not in the format YYYY-MM-DD"
        self._testing_instances(date_of_request=date_of_request,
                                expected_assert_message=expected_assert_message,
                                is_instances_correct=False)
    def _testing_instances(self, locations_file=LOCATIONS_FILE,
                           requested_locations=REQUESTED_USER_CITIES,
                           date_of_request=DATE_OF_REQUEST,
                           expected_assert_message=EXPECTED_ASSERT_MESSAGE,
                           is_instances_correct=True):
        temp_instance = Temperature(locations_file,
                                    requested_locations,
                                    date_of_request)
        if is_instances_correct:
            self.assertEqual(expected_assert_message, str(temp_instance))
        else:
            for instance in range(1, 5):
                try:
                    temp_instance.confirm_instances(instance)
                except ValueError:
                    with self.assertRaises(ValueError) as value_error:
                        temp_instance.confirm_instances(instance)
                    self.assertEqual(expected_assert_message, str(value_error.exception))
                   