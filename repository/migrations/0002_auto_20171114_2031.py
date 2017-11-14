# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-14 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='floor',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='楼层'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.ManyToManyField(related_name='role', to='repository.Role'),
        ),
    ]
