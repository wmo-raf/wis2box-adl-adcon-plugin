from datetime import datetime

import dj_database_url
import psycopg2
from django.conf import settings

from .constants import ADCON_PARAMETER_SUBCLASSES


def get_connection():
    db_config = dj_database_url.parse(settings.WIS2BOX_ADL_ADCON_DATABASE_URL)

    connection = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT']
    )

    return connection


def get_adcon_stations():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""SELECT id, displayname,latitude,longitude,timezoneid 
                            FROM node_60 WHERE dtype ='DeviceNode' and latitude is not null and longitude is not null""")
        stations = cursor.fetchall()

    stations = [dict(zip([column.name for column in cursor.description], station)) for station in stations]

    return stations


def get_adcon_parameters_for_station(adcon_station_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT id, displayname,subclass
                FROM node_60  WHERE dtype ='AnalogTagNode' and parent_id = %s""", (adcon_station_id,)
        )

        parameters = cursor.fetchall()

    parameters = [dict(zip([column.name for column in cursor.description], parameter)) for parameter in parameters]

    parameters = [parameter for parameter in parameters if parameter["subclass"] in ADCON_PARAMETER_SUBCLASSES]

    return parameters


def get_data_for_parameters(conn_cursor, parameter_ids, start_date, end_date, station):
    station_timezone = station.timezone

    # tag_id is the ADCON parameter id
    # status=0 means the data is valid

    if not parameter_ids:
        raise ValueError("No parameter ids provided")

    tag_ids_placeholders = ', '.join(['%s'] * len(parameter_ids))
    query = f"""
        SELECT tag_id, enddate, startdate, measuringvalue
        FROM historiandata
        WHERE tag_id IN ({tag_ids_placeholders})
        AND startdate >= %s
        AND enddate <= %s
        AND status = 0
    """

    parameters = parameter_ids + [start_date, end_date]
    conn_cursor.execute(query, parameters)

    data = conn_cursor.fetchall()

    # organize the data by tag_ids(parameters) and dates
    parameter_data_by_tag_id_by_date = {}

    for data_point in data:
        data_point = dict(zip([column.name for column in conn_cursor.description], data_point))

        end_date = datetime.fromtimestamp(data_point['enddate'], tz=station_timezone)
        start_date = datetime.fromtimestamp(data_point['startdate'], tz=station_timezone)
        tag_id = data_point['tag_id']

        time_diff = (end_date - start_date).total_seconds() / 60

        # 10 and 15 minutes interval,
        # take obs with greater than 3 minutes sampling and less than 20
        if 3 <= time_diff < 20:
            data_point["enddate"] = end_date
            data_point["startdate"] = start_date

            if not parameter_data_by_tag_id_by_date.get(tag_id):
                parameter_data_by_tag_id_by_date[tag_id] = {}

            if parameter_data_by_tag_id_by_date.get(tag_id).get(end_date):
                parameter_data_by_tag_id_by_date[tag_id][end_date].append(data_point)
            else:
                parameter_data_by_tag_id_by_date[tag_id][end_date] = [data_point]

    return parameter_data_by_tag_id_by_date
