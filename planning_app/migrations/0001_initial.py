# Generated by Django 3.1.7 on 2021-08-23 15:13

import datetime

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('city_name', models.CharField(max_length=15)),
                ('distance', models.FloatField(default=0.0)),
                ('address', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=300)),
                ('image', models.URLField(null=True)),
                ('type', models.IntegerField(choices=[(1, 'Place'), (2, 'Hotel')], default=1)),
                ('price', models.PositiveIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
                ('description', models.CharField(max_length=1000)),
                ('price', models.FloatField()),
                ('image', models.URLField(null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning_app.place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('review_text', models.CharField(max_length=700)),
                ('overall_rating', models.IntegerField(
                    choices=[(1, 'Terrible'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=1)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews',
                                            to='planning_app.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='properties',
            field=models.ManyToManyField(related_name='places', to='planning_app.Property'),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_index', models.PositiveIntegerField(default=0,
                                                          validators=[django.core.validators.MinValueValidator(0),
                                                                      django.core.validators.MaxValueValidator(14)])),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days',
                                           to='planning_app.trip')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField(default=0)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities',
                                          to='planning_app.day')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities',
                                            to='planning_app.place')),
            ],
        ),
    ]
