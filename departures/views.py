from django.http import HttpResponse
from django.shortcuts import render
import requests
from departures.models import Stations

coord = {
    "latitude": 52.52457212288371,
    "longitude": 13.347867741684315,
}


# Create your views here.
def index(request, results_no=10):
    payload = {**coord, **{"results": results_no}}
    stations = Stations.objects
    if (
        len(stations.all()) == 0
    ):  # only do vbb api call if no stations are stored (to save time on page load)
        r = requests.get(
            "https://v6.vbb.transport.rest/locations/nearby", params=payload
        )
        list_of_stops = [x["name"] for x in r.json()]
        for stop in r.json():
            stations.create(station_name=stop["name"], station_id=stop["id"])
    else:
        list_of_stops = [x["station_name"] for x in stations.values()]
    return render(
        request,
        "index.html",
        context={"stops": list_of_stops, "number_of_stops": results_no},
    )
