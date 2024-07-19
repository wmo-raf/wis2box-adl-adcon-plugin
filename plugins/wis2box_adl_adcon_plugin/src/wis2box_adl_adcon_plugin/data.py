import logging

from dateutil.relativedelta import relativedelta
from django.conf import settings

from .db import get_data_for_parameters
from .models import StationMapping

logger = logging.getLogger(__name__)

WIS2BOX_ADL_ADCON_INIT_DATETIME = getattr(settings, 'WIS2BOX_ADL_ADCON_INIT_DATETIME')


def get_adcon_data_for_station(connection_cursor, station_mapping_id, local_time):
    station_mapping = StationMapping.objects.get(pk=station_mapping_id)

    station = station_mapping.station
    last_imported = station_mapping.last_imported

    if last_imported:
        # set the timezone of the last_imported date to the station timezone
        last_imported = last_imported.replace(tzinfo=station.timezone)

    # use the default date if the last_imported date is not set
    if not last_imported:
        last_imported = WIS2BOX_ADL_ADCON_INIT_DATETIME
        # set the timezone of the default last_imported date to the station timezone
        last_imported = last_imported.replace(tzinfo=station.timezone)

    # make sure local_time timezone is set to the station timezone
    local_time = local_time.replace(tzinfo=station.timezone)

    # get the difference in months between the last imported date and the current date
    r = relativedelta(last_imported, local_time)
    months_difference = abs((r.years * 12) + r.months)

    # create a list of dates starting from the last imported date to the current date, with a step of 1 month
    date_list = [last_imported + relativedelta(months=i) for i in range(months_difference + 1)]

    logger.info(f'[WIS2BOX_ADL_ADCON_PLUGIN] Getting data for {station}')

    station_data = {}

    station_parameter_mappings = station_mapping.station_parameter_mappings.all()
    tag_ids = [station_parameter_mapping.analog_tag_node_id for station_parameter_mapping in station_parameter_mappings]
    station_parameter_mappings_by_tag_id = {station_parameter_mapping.analog_tag_node_id: station_parameter_mapping for
                                            station_parameter_mapping in station_parameter_mappings}

    for i, date in enumerate(date_list):
        start_date = date
        # get the next date in the list or the current date if there is no next date
        end_date = date_list[i + 1] if i + 1 < len(date_list) else local_time

        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        # get the data for all the parameters
        adcon_parameters_data = get_data_for_parameters(connection_cursor, tag_ids, start_timestamp, end_timestamp,
                                                        station)

        # organize the parameters data by date
        for tag_id, parameter_data in adcon_parameters_data.items():
            parameter = station_parameter_mappings_by_tag_id.get(tag_id).parameter

            if not parameter_data:
                continue

            for p_date, values in parameter_data.items():
                if p_date not in station_data:
                    station_data[p_date] = {}
                station_data[p_date][parameter.pk] = values

    if not station_data:
        logger.info(f'[WIS2BOX_ADL_ADCON_PLUGIN]: No data found for {station} since {last_imported}')

    return station_data
