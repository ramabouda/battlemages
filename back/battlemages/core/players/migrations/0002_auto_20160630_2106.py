# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_player_friends_+', to='players.Player'),
        ),
    ]