# Generated by Django 4.2.6 on 2024-05-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_university_address_university_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
