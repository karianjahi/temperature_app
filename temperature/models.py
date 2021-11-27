from django.db import models
class Weather(models.Model):
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True)
    no_of_known_locations = models.BigIntegerField(null=True)
    no_of_unknown_locations = models.BigIntegerField(null=True)
    temp_exists_on_api = models.BooleanField(default=False)
    @staticmethod
    def get_by_pk(pk):
        return Weather.objects.get(id=pk)
    def update_name(self, name):
        self.name = name
        self.save()

class Location(models.Model):
    weather_id = models.ForeignKey(Weather, on_delete=models.CASCADE)
    location_id = models.BigIntegerField(null=True)
    location_name = models.TextField(blank=True)
    #longitude = models.FloatField(null=True)
    #latitude = models.FloatField(null=True)
    @staticmethod
    def get_by_weather_id(weather_id: int):
        return Location.objects.filter(weather_id=weather_id)

class UnknownLocation(models.Model):
    weather_id = models.ForeignKey(Weather, on_delete=models.CASCADE)
    location_id = models.BigIntegerField(null=True)
    location_name = models.TextField(blank=True)
    #longitude = models.FloatField(null=True)
    #latitude = models.FloatField(null=True)
    @staticmethod
    def get_by_weather_id(weather_id: int):
        return UnknownLocation.objects.filter(weather_id=weather_id)
    
class Temperature(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(blank=True)
    value = models.FloatField(null=True)
    @staticmethod
    def get_by_location_id(location_id: int):
        return Temperature.objects.filter(location_id=location_id)
