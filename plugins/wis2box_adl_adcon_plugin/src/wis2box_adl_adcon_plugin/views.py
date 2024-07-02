from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from wagtail.admin import messages
from wagtail.admin.widgets import HeaderButton
from wagtail_modeladmin.helpers import AdminURLHelper, PermissionHelper

from .forms import ParameterMappingForm
from .models import StationMapping, StationParameterMapping
from wagtail.admin.ui.tables import Column, Table


def wis2box_adl_adcon_plugin_index(request):
    template_name = 'wis2box_adl_adcon_plugin/index.html'

    breadcrumbs_items = [
        {"url": "", "label": _("ADCON Plugin")},
    ]

    station_mapping_admin_helper = AdminURLHelper(StationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    adcon_plugin_menu_items = [
        {
            "label": StationMapping._meta.verbose_name_plural,
            "url": station_mapping_index_url,
            "icon_name": "snippet",
        }
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "menu_items": adcon_plugin_menu_items,
    }

    return render(request, template_name, context)


def station_parameter_mapping_list(request, station_mapping_id):
    queryset = StationParameterMapping.objects.filter(station=station_mapping_id)

    station_mapping_admin_helper = AdminURLHelper(StationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    breadcrumbs_items = [
        {"url": reverse("wis2box_adl_adcon_plugin_index"), "label": _("ADCON Plugin")},
        {"url": station_mapping_index_url, "label": StationMapping._meta.verbose_name_plural},
        {"url": "", "label": _("Station Parameter Mapping")},
    ]

    # Get search parameters from the query string.
    try:
        page_num = int(request.GET.get("p", 0))
    except ValueError:
        page_num = 0

    user = request.user
    all_count = queryset.count()
    result_count = all_count
    paginator = Paginator(queryset, 20)

    try:
        page_obj = paginator.page(page_num + 1)
    except InvalidPage:
        page_obj = paginator.page(1)

    permission_helper = PermissionHelper(StationParameterMapping)

    buttons = [
        HeaderButton(
            label=_('Add Station Parameter Mapping'),
            url=reverse("station_parameter_mapping_create", args=[station_mapping_id]),
            icon_name="plus",
        ),
    ]

    columns = [
        Column("station", label=_("Title")),
        Column("parameter", label=_("Parameter")),
        Column("analog_tag_node_id", label=_("ADCON Node ID")),
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "all_count": all_count,
        "result_count": result_count,
        "paginator": paginator,
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "user_can_create": permission_helper.user_can_create(user),
        "header_buttons": buttons,
        "table": Table(columns, page_obj.object_list),
    }

    return render(request, "wis2box_adl_adcon_plugin/station_parameter_mapping_list.html", context)


def station_parameter_mapping_create(request, station_mapping_id):
    template_name = "wis2box_adl_adcon_plugin/station_parameter_mapping_create.html"

    station_mapping_admin_helper = AdminURLHelper(StationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")
    station_mapping = StationMapping.objects.get(pk=station_mapping_id)

    breadcrumbs_items = [
        {
            "url": reverse("wis2box_adl_adcon_plugin_index"),
            "label": _("ADCON Plugin")},
        {

            "url": station_mapping_index_url,
            "label": StationMapping._meta.verbose_name_plural},
        {
            "url": reverse("station_parameter_mapping_list", args=[station_mapping_id]),
            "label": _("Station Parameter Mapping")},
        {
            "url": "",
            "label": _("Create Station Parameter Mapping")},
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "header_icon": "snippet",
        "page_subtitle": _("Create Station Parameter Mapping"),
        "submit_button_label": _("Create"),
        "action_url": reverse("station_parameter_mapping_create", args=[station_mapping_id]),
    }

    if request.method == "POST":
        form = ParameterMappingForm(request.POST, initial={"station_mapping": station_mapping_id})

        if form.is_valid():
            station_parameter_mapping_data = {
                "station": station_mapping,
                "parameter": form.cleaned_data["parameter"],
                "analog_tag_node_id": form.cleaned_data["adcon_parameter"],
            }
            try:
                StationParameterMapping.objects.create(**station_parameter_mapping_data)

                messages.success(request, _("Station Parameter Mapping created successfully."))

                return redirect(reverse("station_parameter_mapping_list", args=[station_mapping_id]))
            except Exception as e:
                form.add_error(None, e)

                print(e)

                context["form"] = form
                return render(request, template_name, context)
        else:
            context["form"] = form
            return render(request, template_name, context)

        pass
    else:
        form = ParameterMappingForm(initial={"station_mapping": station_mapping_id})
        context["form"] = form

    return render(request, template_name, context)
