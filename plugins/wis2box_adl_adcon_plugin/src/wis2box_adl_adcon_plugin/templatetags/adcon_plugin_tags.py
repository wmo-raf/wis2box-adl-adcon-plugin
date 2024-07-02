from django import template

register = template.Library()


@register.inclusion_tag("wagtailadmin/shared/page_breadcrumbs.html")
def wis2box_adl_adcon_plugin_menu():
    return {
        'menu_items': [
            {
                'url': '/admin/wis2box_adl_adcon_plugin/',
                'title': 'ADCON',
                'is_active': False,
            },
        ]
    }
