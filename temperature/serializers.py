from rest_framework import serializers
from .models import Weather, Location, UnknownLocation, Temperature
class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("created_by",)

class WeatherDeserializerList(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("id", 
                  "name", 
                  "created_on", 
                  "created_by", 
                  "description")
class WeatherDeSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("id", 
                  "name", 
                  "created_on", 
                  "created_by", 
                  "description",
                  "no_of_known_locations",
                  "no_of_unknown_locations",
                  "temp_exists_on_api")

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("weather_id",
                  "location_name",
                  # "longitude",
                  # "latitude"
                  )

class UnknownLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnknownLocation
        fields = ("weather_id",
                  "location_name",
                  # "longitude",
                  # "latitude"
                  )

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ("location_id",
                  "date_and_time",
                  "value")