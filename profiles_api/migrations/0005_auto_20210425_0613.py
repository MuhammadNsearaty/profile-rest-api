# Generated by Django 3.1.7 on 2021-04-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0004_auto_20210418_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
