# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_remove_album_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='imager_images.Image'),
        ),
        migrations.RemoveField(
            model_name='image',
            name='albums',
        ),
        migrations.AddField(
            model_name='image',
            name='albums',
            field=models.ImageField(default='static/default_cat.jpg', upload_to=''),
        ),
    ]
