# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-01 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0114_auto_20180201_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herb',
            name='Chinese_name',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
