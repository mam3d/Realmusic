# Generated by Django 4.0.3 on 2022-04-25 09:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0021_song_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='view',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2022, 4, 25, 9, 50, 17, 840061, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
