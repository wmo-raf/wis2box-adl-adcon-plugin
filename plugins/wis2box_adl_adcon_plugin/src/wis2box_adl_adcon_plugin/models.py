from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wis2box_adl.core.units import units

from .widgets import AdconStationSelectWidget


@register_snippet
class StationMapping(models.Model):
    station = models.OneToOneField("core.Station", on_delete=models.CASCADE, verbose_name=_("Station"),
                                   help_text=_("Station to link with ADCON"))
    device_node_id = models.PositiveIntegerField(verbose_name=_("ADCON Device Node"),
                                                 help_text=_("ADCON Device Node"),
                                                 unique=True)
    last_imported = models.DateTimeField(verbose_name=_("Last Imported"), null=True, blank=True)

    panels = [
        FieldPanel('station'),
        FieldPanel('device_node_id', widget=AdconStationSelectWidget),
    ]

    class Meta:
        verbose_name = _("ADCON Station Link")
        verbose_name_plural = _("ADCON Stations Link")

    def __str__(self):
        return f"{self.station} - {self.device_node_id}"


@register_snippet
class StationParameterMapping(models.Model):
    station_mapping = models.ForeignKey(StationMapping, on_delete=models.CASCADE, verbose_name=_("Station Mapping"),
                                        related_name="station_parameter_mappings")
    parameter = models.ForeignKey("core.DataParameter", on_delete=models.CASCADE, verbose_name=_("Parameter"))
    analog_tag_node_id = models.PositiveIntegerField(verbose_name=_("Analog Tag Node ID"), unique=True)
    units = models.CharField(max_length=10, verbose_name=_("Units"), default=None)

    class Meta:
        verbose_name = _("ADCON Station Parameter Mapping")
        verbose_name_plural = _("ADCON Station Parameter Mapping")
        ordering = ["station_mapping"]
        constraints = [
            models.UniqueConstraint(fields=['station_mapping', 'parameter'], name='unique_station_mapping_parameter')
        ]

    def __str__(self):
        return f"{self.station_mapping} - {self.parameter} - {self.analog_tag_node_id}"

    def get_standardized_value(self, value):
        quantity = value * units(self.units)
        final_units = self.parameter.units_pint
        value_converted = quantity.to(final_units).magnitude

        return value_converted
