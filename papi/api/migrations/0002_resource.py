# Generated by Django 5.1.4 on 2025-01-12 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dept', models.CharField(max_length=64)),
                ('resource_type', models.CharField(max_length=64)),
            ],
        ),
    ]
