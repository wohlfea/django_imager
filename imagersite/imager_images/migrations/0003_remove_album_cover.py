# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 01:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0002_auto_20160420_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='cover',
        ),
    ]