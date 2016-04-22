# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 01:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0003_auto_20160412_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
