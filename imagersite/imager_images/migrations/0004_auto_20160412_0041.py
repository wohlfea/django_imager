# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_auto_20160412_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='album',
        ),
        migrations.AddField(
            model_name='image',
            name='albums',
            field=models.ManyToManyField(related_name='images', to='imager_images.Album'),
        ),
    ]
