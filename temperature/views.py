from . import models, serializers
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from temperature.errors.customErrors import StationsNotFound
from temperature.generic.common import GenericList
from temperature.responses.resp import successResp
from temperature.lib.serializer import save_serializer_id, create_and_save_serializer
from temperature.data_science_files.temperature import Temperature
from temperature.data_science_files.utils import uniques

class WeatherList(APIView):
    def post(self, request):
        user_id = 2
        lists = GenericList(model=models.Weather,
                            serializer=serializers.WeatherSerializer,
                            deserializer=serializers.WeatherDeserializerList,
                            data={"created_by": user_id})
        data = lists.serialize_data()
        return successResp(data)
    
    def get(self, request):
        lists = GenericList(model=models.Weather, deserializer=serializers.WeatherDeserializerList)
        resp = lists.list_get(request)
        return resp

class WeatherDetail(APIView):
    def get(self,request, weather_id):
        weather = models.Weather.get_by_pk(int(weather_id))
        data = serializers.WeatherDeSerializerDetail(weather_id).data
        data["id"] = weather.id
        data["no_of_known_locations"] = weather.no_of_known_locations
        data["no_of_unknown_locations"] = weather.no_of_unknown_locations
        data["temp_on_api"] = weather.temp_exists_on_api
        data["created_by"] = weather.created_by
        data["created_on"] = str(weather.created_on)
        data["description"] = weather.description
        locations_data = {}
        known_location_objects = models.Location.get_by_weather_id(weather_id)
        known_location_names = [i.location_name for i in known_location_objects]
        known_location_pks = [i.id for i in known_location_objects]
        for known_location_pk, known_location_name in zip(known_location_pks, known_location_names):
            temperature_objects = models.Temperature.get_by_location_id(known_location_pk)
            temperature_dates = [i.date_and_time for i in temperature_objects]
            temperature_values = [i.value for i in temperature_objects]
            single_location_data = []
            for date, value in zip(temperature_dates, temperature_values):
                single_location_data.append({"date": date, "value": value})
            locations_data[known_location_name] = single_location_data
        data["recognized_locations"] = uniques(known_location_names)
        unknown_location_objects = models.UnknownLocation.get_by_weather_id(weather_id)
        unknown_location_names = [i.location_name for i in unknown_location_objects]
        data["unrecognized_locations"] = uniques(unknown_location_names)
        data["temperature_data"] = locations_data
        return successResp(data)
    
    def put(self, request, weather_id):
        put_request_entry = request.data
        if len(put_request_entry) == 0:
            return Response({"message": "error", "Detail": "Date and locations must be provided"})
        if "date_of_request" not in put_request_entry:
            return Response({"message": "error", "Detail": "Date of request is a required field"})
        if "locations" not in put_request_entry:
            return Response({"message": "error", "Detail": "List of locations is a required field"})
        date = put_request_entry["date_of_request"]
        if not isinstance(date, str):
            return Response({"message": "error", "Detail": "Date must be a string"})
        locations = put_request_entry["locations"]
        if not isinstance(locations, list):
            return Response({"message": "error", "Detail": "locations must be a list"})
        for location in locations:
            if not isinstance(location, str):
                return Response({"message": "error", "Detail": f'Requested location {location} must be a string'})
        locations_file = "temperature/data_science_files/data/worldcities.csv"
        test_locations = self.handle_unknown_station_error(date, locations, locations_file)
        valid_locations = test_locations["valid_locations"]
        invalid_locations = test_locations["invalid_locations"]
        if valid_locations == []:
            return Response({"message": "error",
                "Detail": f'Station(s): {invalid_locations} not recognized'
                             })
        test_date = self.handle_unknown_date(date, locations, locations_file)
        if test_date is not None:
            return Response({"message": "error",
                             "Detail": f'Date: {date} not in range'})
        
        self.save_objects_into_database(weather_id, date, locations, locations_file)
        return self.get({}, weather_id)
    
    @staticmethod
    def handle_unknown_station_error(date, locations, locations_file):
        temp_obj = Temperature(locations_file, locations, date)
        try:
            locations = temp_obj.identify_valid_and_invalid_locations()
            temp_obj.raise_error_if_all_locations_unrecognized()
        except:
            locations = temp_obj.identify_valid_and_invalid_locations()
        return locations
    
    @staticmethod
    def handle_unknown_date(date, locations, locations_file):
         temp_obj = Temperature(locations_file, locations, date)
         result = temp_obj.get_temperature_data()
         if isinstance(result, dict):
             return {f'Date {date} not in range'}
             
        
    def save_objects_into_database(self, weather_id, date, locations, locations_file):
        weather = models.Weather.get_by_pk(weather_id)
        temp_obj = Temperature(locations_file, locations, date)
        output_table = temp_obj.get_temperature_data()
        known_locations = [i for i in output_table.columns]
        unknown_locations = [i for i in locations if i.title() not in known_locations]
    
        for known_location in known_locations:
            location_series = output_table[known_location]
            date_times = [i for i in location_series.index]
            values = [i for i in location_series]
            location_pk = save_serializer_id(serializers.LocationSerializer,
                                             data = {
                                                 "weather_id": weather_id,
                                                 "location_name": known_location
                                             })
            for date_time, value in zip(date_times, values):
                create_and_save_serializer(serializers.TemperatureSerializer,
                                                    data = {
                                                        "location_id": location_pk,
                                                        "date_and_time": date_time,
                                                        "value": value
                                                    })
        for unknown_location in unknown_locations:
            create_and_save_serializer(serializers.UnknownLocationSerializer,
                                             data = {
                                                 "weather_id": weather_id,
                                                 "location_name": unknown_location
                                             })
        weather.no_of_known_locations = len(known_locations)
        weather.no_of_unknown_locations = len(unknown_locations)
        weather.temp_exists_on_api = True
        weather.save()
        
        
    
        
        
        
        



