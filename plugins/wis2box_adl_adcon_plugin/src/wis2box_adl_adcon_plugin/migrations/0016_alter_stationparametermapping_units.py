# Generated by Django 5.0.6 on 2024-10-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wis2box_adl_adcon_plugin', '0015_stationparametermapping_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationparametermapping',
            name='units',
            field=models.CharField(default=None, max_length=10, verbose_name='Units'),
        ),
    ]
