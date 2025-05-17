from django.db import models

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    country_id = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'locations'
        
    def __repr__(self):
        return f'country: {self.country}, city: {self.name}'
    
class HistoricalWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='history')
    measurement = models.CharField(max_length=100)
    time = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        unique_together = ('location', 'measurement', 'value', 'time')
        db_table = 'measurements'