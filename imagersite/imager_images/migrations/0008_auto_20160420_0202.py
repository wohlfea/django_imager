# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 02:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0007_album_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(default='static/default_cat.jpg', upload_to=''),
        ),
    ]
