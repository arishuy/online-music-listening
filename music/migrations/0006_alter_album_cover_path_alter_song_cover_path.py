# Generated by Django 4.2 on 2023-05-04 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_artist_cover_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover_path',
            field=models.ImageField(null=True, upload_to='album_cover/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='cover_path',
            field=models.ImageField(null=True, upload_to='song_cover/'),
        ),
    ]
