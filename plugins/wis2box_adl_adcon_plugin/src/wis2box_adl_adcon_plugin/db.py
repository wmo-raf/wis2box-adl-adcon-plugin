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
