"""
All tests for this App belong here
"""
import unittest
if __name__ == '__main__':
    from temperature import Temperature
else:
    from temperature.data_science_files.temperature import Temperature
class TestTemperature(unittest.TestCase):
    """
    We inherit from unittest.TestCase to take advantage
    of the large pool of testing capabilities inherent
    there
    """
    def test_for_no_arguments(self):
        """
        Test for arguments
        """
        with self.assertRaises(Exception) as e:
            Temperature()
            self.assertTrue("No arguments given " in e.exception)
    # def test_for_given_arguments(self):
    #     obj = Temperature("my_file", ["berlin", "hamburg"], "2021-10-22")
    #     expected = f"This class displays temperature for these locations: [berlin, hamburg,]"
    #     self.assertEqual(expected, obj.__repr__())

            
        
        