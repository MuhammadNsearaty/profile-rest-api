# Generated by Django 3.1.7 on 2021-08-15 20:32

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_text', models.CharField(max_length=100000)),
                ('date', models.DateField(default=datetime.date.today)),
                ('image', models.URLField(null=True)),
                ('title', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('city_name', models.CharField(max_length=15)),
                ('distance', models.FloatField(default=0.0)),
                ('guest_rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('kinds', models.CharField(default='', max_length=1000)),
                ('description', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('image', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HotelReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_rating', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('city_name', models.CharField(max_length=15)),
                ('distance', models.FloatField(default=0.0)),
                ('guest_rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('kinds', models.CharField(default='', max_length=1000)),
                ('address', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
                ('image', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('image', models.URLField()),
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
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_api.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=5000)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels_api.place')),
            ],
        ),
    ]
