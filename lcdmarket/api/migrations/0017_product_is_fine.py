# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-30 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20160925_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_fine',
            field=models.BooleanField(default=False),
        ),
    ]
