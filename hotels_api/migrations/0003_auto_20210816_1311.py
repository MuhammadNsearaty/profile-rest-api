# Generated by Django 3.1.7 on 2021-08-16 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels_api', '0002_auto_20210815_2332'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
