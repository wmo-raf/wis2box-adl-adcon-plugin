from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from wis2box_adl_adcon_plugin.widgets import AdconStationSelectWidget


class StationMapping(models.Model):
    station = models.OneToOneField("core.Station", on_delete=models.CASCADE, verbose_name=_("Station"))
    device_node_id = models.PositiveIntegerField(verbose_name=_("Device Node ID"), help_text=_("Device Node ID"),
                                                 unique=True)

    panels = [
        FieldPanel('station'),
        FieldPanel('device_node_id', widget=AdconStationSelectWidget),
    ]

    class Meta:
        verbose_name = _("ADCON Station Mapping")
        verbose_name_plural = _("ADCON Station Mapping")

    def __str__(self):
        return f"{self.station} - {self.device_node_id}"


@register_snippet
class StationParameterMapping(models.Model):
    station = models.ForeignKey(StationMapping, on_delete=models.CASCADE, verbose_name=_("Station Mapping"))
    parameter = models.OneToOneField("core.DataParameter", on_delete=models.CASCADE, verbose_name=_("Parameter"))
    analog_tag_node_id = models.PositiveIntegerField(verbose_name=_("Analog Tag Node ID"), unique=True)

    class Meta:
        verbose_name = _("ADCON Station Parameter Mapping")
        verbose_name_plural = _("ADCON Station Parameter Mapping")
        ordering = ["station"]
        constraints = [
            models.UniqueConstraint(fields=['station', 'parameter'], name='unique_station_parameter')
        ]

    def __str__(self):
        return f"{self.station} - {self.parameter} - {self.analog_tag_node_id}"
