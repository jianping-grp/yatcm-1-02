# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-02 16:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0102_auto_20171102_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chembl',
            name='canonical_smi',
        ),
        migrations.RemoveField(
            model_name='chembl',
            name='max_phase',
        ),
        migrations.RemoveField(
            model_name='chembl',
            name='oral',
        ),
        migrations.RemoveField(
            model_name='chembl',
            name='pref_name',
        ),
        migrations.RemoveField(
            model_name='chembl',
            name='prodrug',
        ),
    ]