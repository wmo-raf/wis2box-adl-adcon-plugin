import io
import sys
import time
import zoneinfo
from datetime import timedelta
from random import random

import psycopg2
from django.utils import timezone

from .db import get_connection
from .models import StationParameterMapping

params = {
    "air_temperature": {
        "value_range": (0, 40),
    },
    "wind_speed": {
        "value_range": (0, 30),
    },
    "wind_direction": {
        "value_range": (0, 360),
    },
    "relative_humidity": {
        "value_range": (0, 100),
    },
    "precipitation_intensity": {
        "value_range": (0, 50),
    },
}


class IteratorFile(io.TextIOBase):
    """ given an iterator which yields strings,
    return a file like object for reading those strings """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")

        except StopIteration as e:
            # soak up StopIteration. this block is not necessary because
            # of finally, but just to be explicit
            pass

        except Exception as e:
            print("uncaught exception: {}".format(e))

        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # save the remainder for next read
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)


def generate_fake_db_data(start_date, end_date):
    data = []
    for station_param_mapping in StationParameterMapping.objects.all():
        analog_tag_node_id = station_param_mapping.analog_tag_node_id
        parameter = station_param_mapping.parameter.parameter

        if parameter not in params:
            continue

        value_range = params[parameter]["value_range"]

        random_value = random() * (value_range[1] - value_range[0]) + value_range[0]
        # 2 decimal places
        random_value = round(random_value, 2)

        data.append({
            "tag_id": analog_tag_node_id,
            "measuringvalue": random_value,
            "status": 0,
            "type": 0,
            "startdate": int(start_date.timestamp()),
            "enddate": int(end_date.timestamp()),
        })

    return data


def generate(state):
    current_time = timezone.localtime(timezone=zoneinfo.ZoneInfo("Africa/Addis_Ababa"))

    minute = current_time.minute

    if minute < 15:
        start_date = current_time.replace(minute=0, second=0, microsecond=0)
    elif minute < 30:
        start_date = current_time.replace(minute=15, second=0, microsecond=0)
    elif minute < 45:
        start_date = current_time.replace(minute=30, second=0, microsecond=0)
    else:
        start_date = current_time.replace(minute=45, second=0, microsecond=0)

    end_date = start_date + timedelta(minutes=15)

    if not state.get(end_date):
        state.update({end_date: {}})

    if not state[end_date].get(end_date.minute):
        data = generate_fake_db_data(start_date, end_date)
        state[end_date][end_date.minute] = True

        return data


def run_periodic():
    state = {}
    while True:
        data = generate(state)
        if data:
            args = []
            for item in data:
                val = (item["tag_id"], item["measuringvalue"], item["status"], item["type"], item["startdate"],
                       item["enddate"])
                args.append(val)

            f = IteratorFile(("{}\t{}\t{}\t{}\t{}\t{}".format(x[0], x[1], x[2], x[3], x[4], x[5]) for x in args))

            connection = get_connection()

            try:

                print("Copying data to database....")
                with connection.cursor() as cursor:
                    cursor.copy_from(f, 'historiandata',
                                     columns=('tag_id', 'measuringvalue', 'status', 'type', 'startdate', 'enddate'))

                    connection.commit()

                connection.close()

                print("Data copied to database")

            except psycopg2.errors.UniqueViolation:
                print("Existing record found. Skipping data copy to database")
                pass

        else:
            print("No data generated. Waiting for 15 minutes to elapse..")

        # sleep for 5 minutes
        print("Sleeping for 5 minutes....")
        time.sleep(300)
