# Generated by Django 3.1.7 on 2021-08-14 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels_api', '0006_auto_20210814_2017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user_id',
            new_name='user',
        ),
    ]
