"""
testing temperature.py
"""
import unittest
from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    Make use of Testcase methods
    """
    LOCATIONS_FILE = "temperature/data_science_files/data/worldcities.csv"
    REQUESTED_LOCATIONS = ["Berlin", "Stuttgart"]
    DATE_OF_REQUEST = "2021-10-25"
    def test_correct_instances(self):
        """
        test for correct instances
        """
        inst = Temperature(locations_file=TestTemperature.LOCATIONS_FILE,
                           requested_locations=TestTemperature.REQUESTED_LOCATIONS,
                           date_of_request=TestTemperature.DATE_OF_REQUEST)
        assert_message = "locations are: Berlin Stuttgart"
        self.assertEqual(assert_message, str(inst))
    
    def test_wrong_type_locations_file(self):
        """
        supply wrong type locations file
        """
        locations_file = {"locations_file": "jlsjflsjf"}
        assert_message = "A string is required as path to locations file"
        inst = Temperature(locations_file=locations_file,
                           requested_locations=TestTemperature.REQUESTED_LOCATIONS,
                           date_of_request=TestTemperature.DATE_OF_REQUEST)
        for instance_count in range(1, 5):
            try:
                inst.confirm_instances(instance_count)
            except ValueError:
                with self.assertRaises(ValueError) as value_error:
                    inst.confirm_instances(instance_count)
                self.assertEqual(assert_message, str(value_error.exception))
