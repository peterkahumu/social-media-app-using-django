# Generated by Django 5.0.6 on 2024-08-17 20:13

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateField(default=datetime.datetime(2024, 8, 17, 23, 13, 7, 561089))),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]
