# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-02 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0120_subherb'),
    ]

    operations = [
        migrations.AddField(
            model_name='subherb',
            name='herb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compounds.Herb'),
        ),
    ]
