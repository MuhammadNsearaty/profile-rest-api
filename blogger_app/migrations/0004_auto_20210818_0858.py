# Generated by Django 3.1.7 on 2021-08-18 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger_app', '0003_auto_20210816_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
