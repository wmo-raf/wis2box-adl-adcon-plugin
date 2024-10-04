import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Get ADCON data"

    def handle(self, *args, **options):
        from wis2box_adl.core.registries import plugin_registry
        logger.info('[ADCON]: Getting ADCON data...')

        plugin = plugin_registry.get('aws_adcon')

        plugin.run_process()
