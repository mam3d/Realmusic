# Generated by Django 4.0.3 on 2022-04-02 11:51

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=utils.image.get_file_path),
        ),
    ]
