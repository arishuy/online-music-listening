# Generated by Django 4.2 on 2023-05-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_alter_song_cover_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='cover_path',
            field=models.ImageField(blank=True, null=True, upload_to='artist_cover/'),
        ),
    ]
