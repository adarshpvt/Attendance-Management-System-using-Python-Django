# Generated by Django 5.1.3 on 2024-11-25 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amsapp', '0005_coursedb_delete_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='code',
        ),
    ]
