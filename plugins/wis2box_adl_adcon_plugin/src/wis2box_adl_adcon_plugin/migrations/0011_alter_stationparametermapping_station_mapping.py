# Generated by Django 5.0.6 on 2024-07-03 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wis2box_adl_adcon_plugin', '0010_alter_stationparametermapping_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationparametermapping',
            name='station_mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='station_parameter_mappings', to='wis2box_adl_adcon_plugin.stationmapping', verbose_name='Station Mapping'),
        ),
    ]