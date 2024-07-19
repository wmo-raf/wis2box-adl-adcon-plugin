import csv
import logging
from datetime import timezone
from io import StringIO

from django.core.files.base import ContentFile
from django.utils import timezone as dj_timezone
from django.utils.translation import gettext_lazy as _
from wis2box_adl.core.constants import WIS2BOX_CSV_HEADER
from wis2box_adl.core.models import DataIngestionRecord
from wis2box_adl.core.registries import Plugin
from wis2box_adl_adcon_plugin.data import get_adcon_data_for_station
from wis2box_adl_adcon_plugin.db import get_connection
from wis2box_adl_adcon_plugin.models import StationMapping

logger = logging.getLogger(__name__)


class AdconPlugin(Plugin):
    type = "aws_adcon"
    label = _("ADCON Plugin")
    connection_cursor = None

    def get_connection_cursor(self):
        if self.connection_cursor and not self.connection_cursor.closed:
            return self.connection_cursor
        connection = get_connection()
        self.connection_cursor = connection.cursor()

        return self.connection_cursor

    def get_data(self):
        logger.info("[WIS2BOX_ADL_ADCON_PLUGIN] Getting data from ADCON stations")

        station_mappings = StationMapping.objects.filter(station_parameter_mappings__isnull=False).distinct()

        local_time = dj_timezone.localtime()
        logger.info(f"[WIS2BOX_ADL_ADCON_PLUGIN] Local time: {local_time}")

        if station_mappings:
            with self.get_connection_cursor() as cursor:
                some_data_found = False
                for station_mapping in station_mappings:
                    logger.info(f"[WIS2BOX_ADL_ADCON_PLUGIN] Processing data for station "
                                f"{station_mapping.station.name}")

                    station = station_mapping.station
                    station_wis2box_csv_metadata = station.wis2box_csv_metadata

                    parameter_mappings = station_mapping.station_parameter_mappings.all()
                    parameters_as_dict = {}
                    for parameter_mapping in parameter_mappings:
                        parameters_as_dict[parameter_mapping.parameter.pk] = parameter_mapping.parameter

                    station_data = get_adcon_data_for_station(
                        cursor,
                        station_mapping.pk,
                        local_time
                    )

                    if not station_data:
                        continue
                    else:
                        some_data_found = True

                    data_by_date = {}
                    for date, data in station_data.items():
                        # convert the date to UTC. WIS2BOX expects the dates in UTC
                        utc_date = date.replace(tzinfo=timezone.utc)
                        if not data_by_date.get(utc_date):
                            date_info = {
                                "year": utc_date.year,
                                "month": utc_date.month,
                                "day": utc_date.day,
                                "hour": utc_date.hour,
                                "minute": utc_date.minute,
                            }
                            data_by_date[utc_date] = {
                                **station_wis2box_csv_metadata,
                                **date_info
                            }

                        for parameter_id, parameter_data in data.items():
                            for data_value in parameter_data:
                                value = data_value.get('measuringvalue')
                                parameter = parameters_as_dict.get(parameter_id)
                                data_by_date[utc_date].update({parameter.parameter: value})

                    for utc_data_date, data_values in data_by_date.items():
                        logger.info(f"[WIS2BOX_ADL_ADCON_PLUGIN] Saving data for station {station.name} "
                                    f"at {utc_data_date} UTC")

                        filename = f"WIGOS_{station.wigos_id}_{utc_data_date.strftime('%Y%m%dT%H%M%S')}.csv"

                        output = StringIO()
                        writer = csv.writer(output)
                        writer.writerow(WIS2BOX_CSV_HEADER)

                        row_data = []
                        for col in WIS2BOX_CSV_HEADER:
                            col_data = data_values.get(col, "")
                            row_data.append(col_data)

                        writer.writerow(row_data)
                        csv_content = output.getvalue()
                        output.close()

                        file = ContentFile(csv_content, filename)

                        # check if the data ingestion record already exists
                        ingestion_record = DataIngestionRecord.objects.filter(station=station,
                                                                              time=utc_data_date).first()

                        if ingestion_record:
                            # delete the old file
                            ingestion_record.file.delete()
                            ingestion_record.file = file
                        else:
                            ingestion_record = DataIngestionRecord.objects.create(station=station, time=utc_data_date,
                                                                                  file=file)
                        ingestion_record.save()

                        station_mapping.last_imported = utc_data_date
                        station_mapping.save()

                        logger.info(
                            f"[WIS2BOX_ADL_ADCON_PLUGIN] Data saved for station {station.name} at {utc_data_date}")
                if some_data_found:
                    logger.info("[WIS2BOX_ADL_ADCON_PLUGIN] Data ingestion completed")
        else:
            logger.info("[WIS2BOX_ADL_ADCON_PLUGIN] No ADCON station mappings found")

    def parse_data(self):
        pass

    def load_data(self):
        pass
