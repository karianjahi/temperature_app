"""
Testing the main data science script - temperature.py
"""
import unittest
from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    TestCase has elegant methods for testing in python
    """
    LOCATIONS_FILE = "temperature/data_science_files/data/worldcities.csv"
    REQUESTED_LOCATIONS = ["Berlin", "Karlsruhe", "Stuttgart"]
    DATE_OF_REQUEST = "2021-10-18"
    ASSERT_MESSAGE = "This class displays temperature for these locations: [Berlin, Karlsruhe, Stuttgart,]"
    def test_correct_instances(self):
        """
        Testing correct instances
        """
        self._testing_instances()
    def test_wrong_type_locations_file(self):
        """
        Make locations file a dictionary
        """
        locations_file = {"locations_file": TestTemperature.LOCATIONS_FILE}
        assert_message = "A string is required as path to locations file"
        self._testing_instances(locations_file=locations_file, 
                                assert_message=assert_message,
                                is_correct_instances = False)
    def test_wrong_type_requested_locations(self):
        """
        Deliberately alter requested locations type
        to a dictionary
        """
        requested_locations = {"requested_locations": TestTemperature.REQUESTED_LOCATIONS}
        assert_message = "Requested locations should be a list"
        self._testing_instances(requested_locations=requested_locations,
                                assert_message=assert_message,
                                is_correct_instances=False)
    def test_requested_locations_single_item(self):
        """
        Each item in the list of requested locations should be a string
        """
        requested_locations = ["Berlin", "Munich", 91412]
        assert_message = "91412 not a string"
        self._testing_instances(requested_locations=requested_locations,
                                assert_message=assert_message,
                                is_correct_instances=False)
    def test_date_not_string(self):
        """
        Testing if error is captured when date is not string in the required format
        """
        date = 2021-10-18
        assert_message = f"{date} not a string in the format YYYY-MM-DD"
        self._testing_instances(date_of_request=date,
                                assert_message=assert_message,
                                is_correct_instances=False)
    def test_date_length(self):
        """
        Besides being a string the date must have 10 characters
        """
        date = "21-10-18"
        assert_message = f"{date} length does not equal 10"
        self._testing_instances(date_of_request=date,
                                assert_message=assert_message,
                                is_correct_instances=False)
    def _testing_instances(self,
                           locations_file=LOCATIONS_FILE,
                            requested_locations=REQUESTED_LOCATIONS,
                            date_of_request=DATE_OF_REQUEST,
                           assert_message=ASSERT_MESSAGE,
                           is_correct_instances=True):
        """
        Wrapping duplicated test functions into a single one
        """
        temp_inst = Temperature(locations_file, requested_locations, date_of_request)
        if is_correct_instances:
            self.assertEqual(assert_message, str(temp_inst))
        else:
            for instance in range(1, 6):
                try:
                    temp_inst.confirm_instances(instance)
                except:
                    with self.assertRaises(ValueError) as value_error:
                        temp_inst.confirm_instances(instance)
                    self.assertEqual(assert_message, str(value_error.exception))
                        
            
        
        
        
        