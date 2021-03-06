# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 20:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160211_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(through='api.ProjectContributors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectcontributors',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
