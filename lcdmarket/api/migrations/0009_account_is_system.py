# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-08 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20160220_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_system',
            field=models.BooleanField(default=False),
        ),
    ]