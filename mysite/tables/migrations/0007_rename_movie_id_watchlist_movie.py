# Generated by Django 4.2 on 2024-10-15 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0006_rename_movie_watchlist_movie_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='movie_id',
            new_name='movie',
        ),
    ]
