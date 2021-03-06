# Generated by Django 3.1.7 on 2021-07-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels_api', '0003_location_distance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='rank',
            new_name='guestrating',
        ),
        migrations.RemoveField(
            model_name='location',
            name='distance',
        ),
        migrations.AddField(
            model_name='place',
            name='distance',
            field=models.FloatField(default=0.0),
        ),
    ]
