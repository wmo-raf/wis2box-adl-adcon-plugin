from django.apps import AppConfig
from wis2box_adl.core.registries import plugin_registry


class Wis2BoxAdlAdconPluginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wis2box_adl_adcon_plugin'

    def ready(self):
        from .plugin import AdconPlugin
        plugin_registry.register(AdconPlugin())
