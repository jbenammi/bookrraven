# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookr', '0004_auto_20160525_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='site',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='sound',
            field=models.URLField(blank=True),
        ),
    ]