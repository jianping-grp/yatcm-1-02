# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0079_chembl_same_or_similar'),
    ]

    operations = [
        migrations.AddField(
            model_name='compound',
            name='chembls',
            field=models.ManyToManyField(blank=True, to='compounds.ChEMBL'),
        ),
    ]