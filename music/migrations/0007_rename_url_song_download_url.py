# Generated by Django 4.0.3 on 2022-04-05 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_alter_subtitle_file_album_song_album'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='url',
            new_name='download_url',
        ),
    ]