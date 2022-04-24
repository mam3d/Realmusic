# Generated by Django 4.0.3 on 2022-04-24 09:35

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0019_alter_like_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(default='album_cover/default.png', upload_to=utils.image.get_file_path),
        ),
    ]
