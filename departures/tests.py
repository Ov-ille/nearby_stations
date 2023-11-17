from django.apps import apps
from departures.models import Stations
from departures.views import coord
from departures.helpers import (
    create_stations,
    delete_stations_helper,
    get_nearby_stations_from_vbb,
    get_departures_for_station_from_vbb,
)
import pytest
import requests


# Create your tests here.
@pytest.mark.django_db
class Test_db:
    def test_models_exist(self):
        assert "Stations" in [x.__name__ for x in apps.get_models()]

    def test_create_station(self):
        create_stations({"name": "Test1", "id": 1})
        assert Stations.objects.filter(station_name="Test1").exists()

    def test_delete_stations(self):
        delete_stations_helper()
        assert len(Stations.objects.all()) == 0


@pytest.mark.django_db
class Test_view_stations:
    @pytest.fixture
    def vbb_api_stations(self):
        return get_nearby_stations_from_vbb({**coord, **{"results": 1}})

    @pytest.fixture
    def vbb_api_departures(self, vbb_api_stations):
        return get_departures_for_station_from_vbb(10)

    def test_get_nearby_stations_from_vbb_status(self, vbb_api_stations):
        assert vbb_api_stations["status"] == 200

    def test_get_nearby_stations_from_vbb_response(self, vbb_api_stations):
        if vbb_api_stations["status"] == 200:
            assert all(
                x in vbb_api_stations["response"].json()[0] for x in ["name", "id"]
            )

    def test_get_departures_for_station_from_vbb_status(self, vbb_api_departures):
        assert vbb_api_departures["status"] == 200

    def test_get_departures_for_station_from_vbb_response(self, vbb_api_departures):
        if vbb_api_departures["status"] == 200:
            assert "departures" in vbb_api_departures["response"].json()
