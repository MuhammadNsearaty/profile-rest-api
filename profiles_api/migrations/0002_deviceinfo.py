# Generated by Django 3.1.7 on 2021-08-13 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=100, unique=True)),
                ('app_name', models.CharField(max_length=100)),
                ('app_version', models.CharField(max_length=10)),
                ('build_number', models.CharField(max_length=100)),
                ('fcm_token', models.CharField(max_length=255, unique=True)),
                ('os_version', models.CharField(max_length=100)),
                ('os', models.CharField(max_length=10)),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
