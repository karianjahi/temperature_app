backend API: Unit testing
- As a data scientist, your code will most likely be made available for production through a backend API
- What is an API?
- Agreement between front-end and backend on:
	API format:
		- GET a list of objects
		- GET one object
		- Updating an object (PUT)
		- delete an object
- the fact that the API should undergo testing before deployment
- How various errors should be handled from backend
- The backend developers must align each API to the agreed format
- requirements.txt file



I have created a simple non-machine learning temperature forecasts script that does the following:
	- Requests for a weather API from a website (brightsky) given a list of purely German cities and a date
	- Selects temperature data from the API
	- Creates a temperature only API for the selected cities ready to be deployed to the front end.
Specifically, the script has one class called Temperature with the following methods:
1. __init__ (Constructor class): The attributes of a class instance
	The attributes are as follows:
	i. locations_file: The file name with geo-coordinates of all cities in the world. Should be a string
	ii. requested_locations: a list of german cities each as string
	iii. date_of_request: a date as string in the format YYYY-MM-DD
2. __repr__ (Class representation): How an instance of the class should be represented
3. confirm_instances: A method that tests whether the various attributes are of the right type
4. convert_user_locations_to_ascii
5. read_world_cities_from_database: Basically reads the locations_file
6. select_german_locations_only_from_database
7. identify_valid_and_invalid_locations
8. raise_error_if_all_locations_unrecognizable
9. get_geocoordinates
10. get_weather_api_for_single_location
11. get_temperature_data 

The script above is then deployed in production using a django-driven infrastructure
A demonstration shall be shown afterwards how the deployment works using a tool called POSTMAN


Unit testing:
- unittest package has a TestCase class that has elegant methods for testing your code.
- We shall use unittest.TestCase methods to test the script
- We shall determine the coverage (or the percentage covered by tests and which lines are unvisited)
- pytest and coverage shall be used to make the tests
- We shall also use pylint to ensure that our tests are upto PEP code standard.