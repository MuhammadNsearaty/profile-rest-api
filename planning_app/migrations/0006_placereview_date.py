# Generated by Django 3.1.7 on 2021-08-16 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning_app', '0005_day_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='placereview',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
