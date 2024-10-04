from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import StationMapping
from .views import (
    wis2box_adl_adcon_plugin_index,
    station_parameter_mapping_list,
    station_parameter_mapping_create,
    data_ingestion_records,
    station_parameter_mapping_delete
)


@hooks.register('register_admin_urls')
def urlconf_wis2box_adl_adcon_plugin():
    return [
        path('wis2box_adl_adcon_plugin/', wis2box_adl_adcon_plugin_index, name='wis2box_adl_adcon_plugin_index'),
        path('wis2box_adl_adcon_plugin/station_parameter_mapping/<int:station_mapping_id>/',
             station_parameter_mapping_list, name='station_parameter_mapping_list'),
        path('wis2box_adl_adcon_plugin/station_parameter_mapping/delete/<int:station_parameter_mapping_id>/',
             station_parameter_mapping_delete, name='station_parameter_mapping_delete'),
        path('wis2box_adl_adcon_plugin/station_parameter_mapping/<int:station_mapping_id>/create/',
             station_parameter_mapping_create,
             name='station_parameter_mapping_create'),
        path('adcon_ingestion_records/', data_ingestion_records, name='adcon_ingestion_records'),
    ]


class StationMappingPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        return False


class StationMappingAdmin(ModelAdmin):
    model = StationMapping
    add_to_admin_menu = False
    permission_helper_class = StationMappingPermissionHelper

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["parameter_mapping"]

        self.parameter_mapping.__func__.short_description = _('Parameter Mapping')

    def parameter_mapping(self, obj):
        label = _("Parameter Mapping")

        url = reverse("station_parameter_mapping_list", args=[obj.id])

        button_html = f"""
            <a href="{url}" class="button button-small button--icon bicolor">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ul icon" aria-hidden="true">
                        <use href="#icon-list-ul"></use>
                    </svg>
                </span>
              {label}
            </a>
        """
        return mark_safe(button_html)


modeladmin_register(StationMappingAdmin)


@hooks.register("register_wis2box_adl_plugin_menu_items")
def register_wis2box_adl_menu_items():
    url = reverse("wis2box_adl_adcon_plugin_index")

    menu_items = [
        MenuItem(label=gettext("ADCON"), url=url, icon_name="cog", order=1000)
    ]

    return menu_items
