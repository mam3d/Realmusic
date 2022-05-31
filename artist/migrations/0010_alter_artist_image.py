# Generated by Django 4.0.3 on 2022-05-31 05:27

from django.db import migrations, models
import utils.image


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0009_alter_follow_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.ImageField(default='artist/default.png', upload_to=utils.image.get_file_path),
        ),
    ]
