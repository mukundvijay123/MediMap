# Generated by Django 5.1.4 on 2025-01-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_resource'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=32, null=True)),
                ('cover', models.IntegerField()),
                ('addr', models.CharField(max_length=64, null=True)),
                ('email', models.CharField(max_length=64, null=True)),
                ('website_url', models.CharField(max_length=64, null=True)),
            ],
        ),
    ]