# Generated by Django 5.0.6 on 2024-11-15 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0009_postmodel_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect.userreg')),
            ],
        ),
    ]
