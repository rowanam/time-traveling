# Generated by Django 3.2.23 on 2023-12-14 23:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trips', '0005_auto_20231213_0428'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomTrip',
            new_name='Trip',
        ),
    ]
