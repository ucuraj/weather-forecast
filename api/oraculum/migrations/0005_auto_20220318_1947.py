# Generated by Django 2.2.27 on 2022-03-18 22:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oraculum', '0004_auto_20220318_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherforecast',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
