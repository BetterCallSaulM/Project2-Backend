# Generated by Django 4.2 on 2024-10-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_auto_20241003_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='releaseDate',
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]