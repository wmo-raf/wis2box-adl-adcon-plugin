from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .widgets import AdconStationSelectWidget


@register_snippet
class StationMapping(models.Model):
    station = models.OneToOneField("core.Station", on_delete=models.CASCADE, verbose_name=_("Station"))
    device_node_id = models.PositiveIntegerField(verbose_name=_("Device Node ID"), help_text=_("Device Node ID"),
                                                 unique=True)
    last_imported = models.DateTimeField(verbose_name=_("Last Imported"), null=True, blank=True)

    panels = [
        FieldPanel('station'),
        FieldPanel('device_node_id', widget=AdconStationSelectWidget),
        FieldPanel('last_imported'),
    ]

    class Meta:
        verbose_name = _("ADCON Station Mapping")
        verbose_name_plural = _("ADCON Station Mapping")

    def __str__(self):
        return f"{self.station} - {self.device_node_id}"


class StationParameterMapping(models.Model):
    station_mapping = models.ForeignKey(StationMapping, on_delete=models.CASCADE, verbose_name=_("Station Mapping"),
                                        related_name="station_parameter_mappings")
    parameter = models.OneToOneField("core.DataParameter", on_delete=models.CASCADE, verbose_name=_("Parameter"))
    analog_tag_node_id = models.PositiveIntegerField(verbose_name=_("Analog Tag Node ID"), unique=True)

    class Meta:
        verbose_name = _("ADCON Station Parameter Mapping")
        verbose_name_plural = _("ADCON Station Parameter Mapping")
        ordering = ["station_mapping"]
        constraints = [
            models.UniqueConstraint(fields=['station_mapping', 'parameter'], name='unique_station_mapping_parameter')
        ]

    def __str__(self):
        return f"{self.station_mapping} - {self.parameter} - {self.analog_tag_node_id}"
