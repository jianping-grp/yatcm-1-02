# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-01 06:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0104_auto_20171102_1656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keggpathway',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='keggpathwaycategory',
            options={'ordering': ['name']},
        ),
    ]
