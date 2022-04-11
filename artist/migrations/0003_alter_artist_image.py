# Generated by Django 4.0.3 on 2022-04-02 12:43

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_artist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.ImageField(default='media/artist_iamge/default.png', upload_to='', verbose_name=utils.image.get_file_path),
        ),
    ]