from django.urls import path
from . import views

urlpatterns = [
    path(
        "stations/<int:station_id>/",
        views.get_one_station_and_departures,
        name="station_detail",
    ),
    path(
        "stations",
        views.get_all_stations_and_departures,
        name="stations",
    ),
    path(
        "deletestations",
        views.delete_stations,
        name="delete_stations",
    ),
    path("", views.view_stations, name="index"),
]
