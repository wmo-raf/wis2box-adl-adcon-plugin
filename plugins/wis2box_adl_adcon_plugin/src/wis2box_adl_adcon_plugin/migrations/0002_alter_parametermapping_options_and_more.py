# Generated by Django 5.0.6 on 2024-07-02 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wis2box_adl_adcon_plugin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parametermapping',
            options={'verbose_name': 'ADCON Parameter Mapping', 'verbose_name_plural': 'ADCON Parameter Mapping'},
        ),
        migrations.AlterModelOptions(
            name='stationmapping',
            options={'verbose_name': 'ADCON Station Mapping', 'verbose_name_plural': 'ADCON Station Mapping'},
        ),
        migrations.AlterModelOptions(
            name='stationparametermapping',
            options={'verbose_name': 'ADCON Station Parameter Mapping', 'verbose_name_plural': 'ADCON Station Parameter Mapping'},
        ),
    ]
