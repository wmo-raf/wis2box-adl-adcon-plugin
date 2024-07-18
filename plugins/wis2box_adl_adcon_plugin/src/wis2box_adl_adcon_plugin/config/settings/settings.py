import os
from datetime import datetime

from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone


def setup(settings):
    """
    This function is called after WIS2Box ADL has setup its own Django settings file but
    before Django starts. Read and modify provided settings object as appropriate
    just like you would in a normal Django settings file. E.g.:

    settings.INSTALLED_APPS += ["some_custom_plugin_dep"]
    """

    # Add wagtail_modeladmin to the installed apps if it is not already there.
    if 'wagtail_modeladmin' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ['wagtail_modeladmin']

    WIS2BOX_ADL_ADCON_DATABASE_URL = os.getenv('WIS2BOX_ADL_ADCON_DATABASE_URL')

    if not WIS2BOX_ADL_ADCON_DATABASE_URL:
        raise ImproperlyConfigured('WIS2BOX_ADL_ADCON_DATABASE_URL environment variable is not set')

    settings["WIS2BOX_ADL_ADCON_DATABASE_URL"] = WIS2BOX_ADL_ADCON_DATABASE_URL

    WIS2BOX_ADL_ADCON_INIT_DATETIME = os.getenv('WIS2BOX_ADL_ADCON_INIT_DATETIME')

    local_time = timezone.localtime()
    if WIS2BOX_ADL_ADCON_INIT_DATETIME:
        date_format = "%Y-%m-%d %H:%M"
        try:
            timezone.activate(settings.TIME_ZONE)
            init_datetime = datetime.strptime(WIS2BOX_ADL_ADCON_INIT_DATETIME, date_format)
            init_datetime = timezone.make_aware(init_datetime)

            if init_datetime > local_time:
                init_datetime = local_time
            settings["WIS2BOX_ADL_ADCON_INIT_DATETIME"] = init_datetime
        except ValueError as e:
            raise ImproperlyConfigured(f"WIS2BOX_ADL_ADCON_INIT_DATETIME environment variable is not in the "
                                       f"correct format. Expected format: {date_format}, provided "
                                       f"value: '{WIS2BOX_ADL_ADCON_INIT_DATETIME}' ")
    else:
        settings["WIS2BOX_ADL_ADCON_INIT_DATETIME"] = local_time
