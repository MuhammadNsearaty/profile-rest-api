# Generated by Django 3.1.7 on 2021-08-14 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels_api', '0007_auto_20210814_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='imageUri',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='imageUri',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
