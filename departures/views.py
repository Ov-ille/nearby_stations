from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from departures.models import Stations
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import StationsSerializer
from .helpers import *

coord = {
    "latitude": 52.52457212288371,
    "longitude": 13.347867741684315,
}


# Create your views here.
@api_view(["GET"])
def get_all_stations_and_departures(request):
    # get stored stations + serialize
    stations = Stations.objects.all()
    serializer = StationsSerializer(stations, many=True)
    # create session and request departures for every station from vbb
    for i in serializer.data:
        r = get_departures_for_station_from_vbb(i["station_id"])
        if r["status"] == 200:
            # add departures in dict for each station
            i["departures"] = r["response"].json()["departures"]
        else:
            # return if one of the api calls has failed
            return Response({"status": r["status"], "response": r["response"]})
    return Response(serializer.data)


@api_view(["GET"])
def get_one_station_and_departures(request, station_id):
    # get stored stations + serialize
    station_detail = Stations.objects.get(station_id=station_id)

    serializer = StationsSerializer(station_detail)
    r = get_departures_for_station_from_vbb(station_id)
    serialized_data = serializer.data.copy()
    if r["status"] == 200:
        # add departures in station dict
        serialized_data["departures"] = r["response"].json()["departures"]
        return Response(serialized_data)
    else:
        return Response({"status": r["status"], "response": r["response"]})


def view_stations(request, results_no=10):
    payload = {**coord, **{"results": results_no}}
    if (
        len(Stations.objects.all()) == 0
    ):  # only do vbb api call if no stations are stored (to save time on page load)
        r = get_nearby_stations_from_vbb(payload)
        if r["status"] == 200:
            for stop in r["response"].json():
                create_stations(stop)
    return render(
        request,
        "index.html",
        context={
            "stations": Stations.objects.values(),
            "number_of_stops": results_no,
        },
    )


def delete_stations(request):
    delete_stations_helper()
    return redirect(view_stations)
