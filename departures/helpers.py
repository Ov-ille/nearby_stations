import requests
from departures.models import Stations

coord = {
    "latitude": 52.52457212288371,
    "longitude": 13.347867741684315,
}


def create_stations(stop):
    Stations.objects.create(station_name=stop["name"], station_id=stop["id"])


def delete_stations_helper():
    Stations.objects.all().delete()


def get_nearby_stations_from_vbb(payload):
    r = requests.get(
        "https://v6.vbb.transport.rest/locations/nearby",
        params=payload,
        timeout=(0.25, None),
    )
    return {"status": r.status_code, "response": r}


def get_departures_for_station_from_vbb(station_id):
    r = requests.get(
        f"https://v6.vbb.transport.rest/stops/{station_id}/departures",
        params={"results": 3},
        timeout=(0.25, None),
    )
    return {"status": r.status_code, "response": r}
