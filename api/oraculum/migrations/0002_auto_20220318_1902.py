# Generated by Django 2.2.27 on 2022-03-18 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oraculum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weatherforecast',
            old_name='time_zone_offseet',
            new_name='time_zone_offset',
        ),
    ]
