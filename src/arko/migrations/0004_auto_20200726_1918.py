# Generated by Django 3.0.8 on 2020-07-26 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arko', '0003_device_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='seenAgo',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 19, 18, 53, 907472)),
        ),
        migrations.AlterField(
            model_name='device',
            name='lastSeen',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 19, 18, 53, 907472)),
        ),
    ]
