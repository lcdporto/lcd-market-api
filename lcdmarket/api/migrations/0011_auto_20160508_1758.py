# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-08 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]
