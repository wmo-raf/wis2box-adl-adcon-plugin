import logging

from django.conf import settings
from django.core.management import BaseCommand
from wis2box_adl.core.registries import plugin_registry

logger = logging.getLogger(__name__)

WIS2BOX_ADL_ADCON_INIT_DATETIME = getattr(settings, 'WIS2BOX_ADL_ADCON_INIT_DATETIME')


class Command(BaseCommand):
    help = "Get ADCON data"

    def handle(self, *args, **options):
        logger.info('[ADCON]: Getting ADCON data...')

        plugin = plugin_registry.get('aws_adcon')

        data = plugin.get_data()
