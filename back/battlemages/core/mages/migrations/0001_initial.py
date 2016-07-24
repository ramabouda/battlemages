# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spells', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('hp_max', models.SmallIntegerField(default=15)),
                ('element', models.CharField(max_length=8)),
                ('spells', models.ManyToManyField(to='spells.Spell')),
            ],
        ),
    ]