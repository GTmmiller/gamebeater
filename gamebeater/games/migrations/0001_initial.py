# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.CharField(default="There's no description for this genre yet.", max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('emulatable', models.BooleanField(default=False)),
                ('generation', models.PositiveSmallIntegerField(default=8)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(to='games.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(to='games.Platform'),
        ),
    ]
