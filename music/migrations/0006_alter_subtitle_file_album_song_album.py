# Generated by Django 4.0.3 on 2022-04-02 09:17

from django.db import migrations, models
import django.db.models.deletion
import utils.image
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
        ('music', '0005_alter_subtitle_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[utils.validators.subtitle_validator]),
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(default='media/music_cover/default.png', upload_to=utils.image.get_file_path)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='artist.artist')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='music.genre')),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='songs', to='music.album'),
        ),
    ]