# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 01:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_auto_20160412_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='photo',
            field=models.ImageField(null=True, upload_to='photo_files/%Y-%m-%d'),
        ),
    ]