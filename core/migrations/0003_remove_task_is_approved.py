# Generated by Django 5.1.6 on 2025-02-08 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_app_package_name_app_app_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_approved',
        ),
    ]
