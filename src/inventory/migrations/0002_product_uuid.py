# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-22 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.CharField(blank=True, default='', max_length=36),
        ),
    ]
