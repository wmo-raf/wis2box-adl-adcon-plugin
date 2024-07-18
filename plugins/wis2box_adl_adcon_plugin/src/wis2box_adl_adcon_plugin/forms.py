from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from wis2box_adl_adcon_plugin.db import get_adcon_parameters_for_station
from wis2box_adl_adcon_plugin.models import StationParameterMapping, StationMapping


class ParameterMappingForm(WagtailAdminModelForm):
    station_mapping = forms.ModelChoiceField(queryset=StationMapping.objects.all(), widget=forms.HiddenInput())
    adcon_parameter = forms.ChoiceField(choices=[])

    class Meta:
        model = StationParameterMapping
        fields = ["parameter", "adcon_parameter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get("initial", {})
        station_mapping_id = initial.get("station_mapping")
        station_mapping = StationMapping.objects.get(id=station_mapping_id)

        existing_parameters = StationParameterMapping.objects.filter(station_mapping=station_mapping)
        existing_adcon_parameter_node_ids = [parameter.analog_tag_node_id for parameter in existing_parameters]

        parameters = get_adcon_parameters_for_station(station_mapping.device_node_id)

        # Filter out parameters that are already mapped
        parameters = [parameter for parameter in parameters if parameter["id"] not in existing_adcon_parameter_node_ids]

        existing_parameters_ids = [parameter.parameter_id for parameter in existing_parameters]

        # Filter out parameters that are already mapped
        self.fields["parameter"].queryset = self.fields["parameter"].queryset.exclude(id__in=existing_parameters_ids)

        self.fields["adcon_parameter"].choices = [(parameter["id"], parameter["displayname"]) for parameter in
                                                  parameters]
