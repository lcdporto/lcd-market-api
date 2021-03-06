# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160211_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='projectareas',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectareas',
            name='tag',
        ),
        migrations.AlterField(
            model_name='project',
            name='areas',
            field=models.ManyToManyField(through='api.Inter', to='api.Tag'),
        ),
        migrations.DeleteModel(
            name='ProjectAreas',
        ),
        migrations.AddField(
            model_name='inter',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Project'),
        ),
        migrations.AddField(
            model_name='inter',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tag'),
        ),
    ]
