from django.db import models


# Create your models here.
class Stations(models.Model):
    station_name = models.CharField(max_length=200)
    station_id = models.BigIntegerField()

    def __str__(self):
        return self.station_name
