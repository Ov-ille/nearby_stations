from django.apps import apps
from departures.models import Stations
from departures.views import coord
import pytest
import requests

# Create your tests here.


@pytest.mark.django_db
class Test_db:
    def test_models_exist(self):
        assert "Stations" in [x.__name__ for x in apps.get_models()]

    def test_create_station(self):
        Stations.objects.create(station_name="Test1", station_id=1)
        assert Stations.objects.filter(station_name="Test1").exists()


@pytest.mark.django_db
class Test_view_index:
    def test_station_length(self):
        stations = Stations.objects
        assert type(len(stations.all())) is int

    @pytest.fixture
    def vbb_api_response(self):
        return requests.get(
            "https://v6.vbb.transport.rest/locations/nearby",
            params={**coord, **{"results": 1}},
        )

    def test_vbb_api_status(self, vbb_api_response):
        assert vbb_api_response.status_code == 200

    def test_add_stations_from_api_response(self, vbb_api_response):
        list_of_stops = [x["name"] for x in vbb_api_response.json()]
        for stop in vbb_api_response.json():
            Stations.objects.create(station_name=stop["name"], station_id=stop["id"])
        error = False
        for stop in list_of_stops:
            if stop not in Stations.objects.all().values_list(
                "station_name", flat=True
            ):
                error = True
        assert error == False
