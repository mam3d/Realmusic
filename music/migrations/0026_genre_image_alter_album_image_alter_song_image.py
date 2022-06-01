# Generated by Django 4.0.3 on 2022-05-31 05:27

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0025_alter_like_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='image',
            field=models.ImageField(default='genre/default.png', upload_to=utils.image.get_file_path),
        ),
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(default='album/default.png', upload_to=utils.image.get_file_path),
        ),
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.ImageField(default='music/default.png', upload_to=utils.image.get_file_path),
        ),
    ]