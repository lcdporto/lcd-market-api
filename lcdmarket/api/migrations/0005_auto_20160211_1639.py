# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160211_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='areas',
            field=models.ManyToManyField(through='api.ProjectAreas', to='api.Tag'),
        ),
        migrations.AddField(
            model_name='projectareas',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Project'),
        ),
        migrations.AddField(
            model_name='projectareas',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tag'),
        ),
    ]
