# Generated by Django 5.0.6 on 2024-07-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wis2box_adl_adcon_plugin', '0011_alter_stationparametermapping_station_mapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='stationparametermapping',
            name='last_imported',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Imported'),
        ),
    ]
