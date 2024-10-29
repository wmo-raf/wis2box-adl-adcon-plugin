# Generated by Django 5.1.2 on 2024-10-29 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('wis2box_adl_adcon_plugin', '0002_alter_stationparametermapping_parameter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdconSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_stations_with_coords', models.BooleanField(default=True, help_text='Only show stations that have latitude and longitude in the ADCON Station Linking', verbose_name='Filter Stations with Coordinates')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'ADCON Settings',
                'verbose_name_plural': 'ADCON Settings',
            },
        ),
    ]
