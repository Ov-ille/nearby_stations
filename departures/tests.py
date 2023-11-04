from django.apps import apps
from departures.models import Stations
import pytest

# Create your tests here.


@pytest.mark.django_db
class Test_db:
    def test_models_exist(self):
        assert "Stations" in [x.__name__ for x in apps.get_models()]

    def test_create_station(self):
        Stations.objects.create(station_name="Test1", station_id=1)
        assert Stations.objects.filter(station_name="Test1").exists()
