# Generated by Django 4.0.3 on 2022-04-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_artist_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]