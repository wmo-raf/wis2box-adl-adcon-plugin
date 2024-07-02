from django.utils.translation import gettext_lazy as _
from wis2box_adl.core.registries import Plugin


class AdconPlugin(Plugin):
    type = "aws_adcon"
    label = _("ADCON Plugin")

    def get_data(self):
        pass

    def parse_data(self):
        pass

    def load_data(self):
        pass
