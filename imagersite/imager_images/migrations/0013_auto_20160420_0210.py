# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 02:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0012_auto_20160420_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(default='static/default_cat.jpg', upload_to=''),
        ),
    ]
