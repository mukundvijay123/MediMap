# Generated by Django 5.1.4 on 2024-12-21 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_insurance_patient_accident_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='accident',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='accident',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accident', to='api.patient'),
        ),
    ]
