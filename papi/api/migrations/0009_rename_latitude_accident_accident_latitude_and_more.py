# Generated by Django 5.1.4 on 2025-01-14 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_patient_hospital'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accident',
            old_name='latitude',
            new_name='accident_latitude',
        ),
        migrations.RenameField(
            model_name='accident',
            old_name='longitude',
            new_name='accident_longitude',
        ),
    ]
