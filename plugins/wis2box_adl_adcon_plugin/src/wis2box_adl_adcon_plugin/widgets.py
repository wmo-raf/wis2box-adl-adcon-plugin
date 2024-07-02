from django.forms import widgets

from .db import get_adcon_stations


class AdconStationSelectWidget(widgets.Select):
    def __init__(self, attrs=None, choices=()):
        blank_choice = [("", "---------")]

        station_choices = [(station["id"], station["displayname"]) for station in get_adcon_stations()]

        super().__init__(attrs, blank_choice + station_choices)
