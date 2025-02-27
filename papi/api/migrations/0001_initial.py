# Generated by Django 5.1.4 on 2025-01-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital_name', models.CharField(max_length=32)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('addr', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=32)),
                ('state_name', models.CharField(max_length=32)),
                ('pincode', models.IntegerField()),
                ('contact', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
    ]
