# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 21:01
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'FriendRequests',
                'verbose_name': 'FriendRequest',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('registration_date', models.DateField()),
                ('ranking', models.IntegerField()),
                ('gold', models.IntegerField(default=0)),
                ('friends', models.ManyToManyField(related_name='_player_friends_+', to='players.Player')),
            ],
            options={
                'verbose_name_plural': 'Players',
                'verbose_name': 'Player',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='player_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_from', to='players.Player'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='player_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_to', to='players.Player'),
        ),
    ]
