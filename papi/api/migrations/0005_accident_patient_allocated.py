# Generated by Django 5.1.4 on 2025-01-13 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_consistsof'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('accident_details', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=64)),
                ('gender', models.CharField(blank=True, max_length=16, null=True)),
                ('blood_group', models.CharField(max_length=8)),
                ('contact', models.CharField(max_length=16)),
                ('accident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='api.accident')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='api.hospital')),
                ('insurance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='api.insurance')),
            ],
        ),
        migrations.CreateModel(
            name='Allocated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_allocated', models.IntegerField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_resources', to='api.resource')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocated_resources', to='api.patient')),
            ],
        ),
    ]
