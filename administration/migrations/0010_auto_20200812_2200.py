# Generated by Django 3.0.8 on 2020-08-12 22:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0009_auto_20200812_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 12, 22, 0, 55, 109494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 12, 22, 0, 55, 108372, tzinfo=utc)),
        ),
    ]