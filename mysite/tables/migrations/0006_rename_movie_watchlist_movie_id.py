# Generated by Django 4.2 on 2024-10-15 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0005_rename_movie_id_watchlist_movie_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='movie',
            new_name='movie_id',
        ),
    ]