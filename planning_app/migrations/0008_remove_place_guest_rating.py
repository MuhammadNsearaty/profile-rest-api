# Generated by Django 3.1.7 on 2021-08-16 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning_app', '0007_auto_20210816_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='guest_rating',
        ),
    ]
