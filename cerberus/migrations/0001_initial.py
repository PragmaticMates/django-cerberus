# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lockout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=None, max_length=255, blank=True, null=True, verbose_name='username', db_index=True)),
                ('failed_attempts', models.PositiveIntegerField(default=0, verbose_name='failed attempts')),
                ('ip_address', models.IPAddressField(default=None, null=True, verbose_name='IP address', blank=True)),
                ('user_agent', models.CharField(default=None, max_length=1024, null=True, verbose_name='user agent', blank=True)),
                ('params_get', models.TextField(verbose_name='GET params')),
                ('params_post', models.TextField(verbose_name='POST params')),
                ('is_locked', models.BooleanField(default=False, db_index=True, verbose_name='locked')),
                ('is_expired', models.BooleanField(default=False, verbose_name='expired')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
                'db_table': 'cerberus_lockouts',
                'verbose_name': 'lockout',
                'verbose_name_plural': 'lockouts',
            },
        ),
    ]
