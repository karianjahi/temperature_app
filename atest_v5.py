"""
Testing temperature.py file
"""
# pylint: disable=C0301
import unittest
from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    Class inherits from TestCase to
    take advantage of the elegant methods therein
    """
    LOCATION_FILE = "temperature/data_science_files/data/worldcities.csv"
    USER_LOCATIONS = ["Berlin", "Stuttgart", "Ulm"]
    DATE_OF_REQUEST = "2021-10-19"
    ASSERT_MESSAGE = "This class displays temperature for these locations: [Berlin, Stuttgart, Ulm,]"
    def test_correct_type_instances(self):
        """
        Testing when we expect correct instances
        """
        self._testing_instance_errors()
    def test_wrong_type_locations_file(self):
        """
        Deliberately introducing locations file as dictionary
        and expect an error
        """
        locations_file = {"locations_file": TestTemperature.LOCATION_FILE}
        assert_message = "A string is required as path to locations file"
        self._testing_instance_errors(assert_message=assert_message,
                             locations_file=locations_file,
                             is_correct_instances=False)
    def test_wrong_type_user_locations(self):
        """
        Deliberately make user locations a dictionary
        """
        user_locations = {"user_locations": TestTemperature.USER_LOCATIONS}
        assert_message = "Requested locations should be a list"
        self._testing_instance_errors(assert_message=assert_message,
                             requested_locations=user_locations,
                             is_correct_instances=False)
    def test_wrong_type_single_user_location(self):
        """
        Deliberately render a list member in requested locations a non-string
        """
        user_locations = ["Berlin", "Leipzig", 9412]
        assert_message = '9412 not a string'
        self._testing_instance_errors(assert_message=assert_message,
                             requested_locations=user_locations,
                             is_correct_instances=False)
    def test_integer_type_date(self):
        """
        Deliberately making date an integer
        """
        date=2021-10-20
        assert_message = f"{date} cannot be an integer"
        self._testing_instance_errors(assert_message=assert_message,
                             date_of_request=date,
                             is_correct_instances=False)
    def test_other_type_date(self):
        """
        Try to set a date as a list or dictionary
        """
        date = ["2021-10-22"]
        assert_message = f"{date} must be a string in the format YYYY-MM-DD"
        self._testing_instance_errors(assert_message=assert_message,
                             date_of_request=date,
                             is_correct_instances=False)
    def test_character_length_date(self):
        """
        Test when the date has a short form e.g.
        YY-MM-DD
        """
        date = "21-10-22"
        assert_message = f"{date} must have 10 characters"
        self._testing_instance_errors(assert_message=assert_message,
                             date_of_request=date,
                             is_correct_instances=False)
    def _testing_instance_errors(self,
                        locations_file=LOCATION_FILE,
                        requested_locations=USER_LOCATIONS,
                        date_of_request=DATE_OF_REQUEST, 
                        assert_message=ASSERT_MESSAGE,
                        is_correct_instances=True):
        """
        Testing errors
        """
        inst = Temperature(locations_file,
                           requested_locations,
                           date_of_request)
        if is_correct_instances:
            self.assertEqual(assert_message, str(inst))
        else:
            for instance in range(1, 5):
                try:
                    inst.confirm_instances(instance)
                except ValueError:
                    with self.assertRaises(ValueError) as value_error:
                        inst.confirm_instances(instance)
                    self.assertEqual(assert_message, str(value_error.exception))
            
        