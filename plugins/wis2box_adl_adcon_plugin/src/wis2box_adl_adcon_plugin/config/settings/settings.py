import os

from django.core.exceptions import ImproperlyConfigured


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
