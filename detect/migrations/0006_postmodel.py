# Generated by Django 5.0.6 on 2024-11-14 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0005_alter_userreg_pro_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_pic', models.FileField(blank=True, null=True, upload_to='post_pics/')),
                ('description', models.TextField(blank=True, null=True)),
                ('likes_count', models.IntegerField(blank=True, null=True)),
                ('liked_users', models.ManyToManyField(null=True, related_name='liked_posts', to='detect.userreg')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='detect.userreg')),
            ],
        ),
    ]
