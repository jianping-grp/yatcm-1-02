# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from compounds.models import *
from models import Target, ChEMBL
# Register your models here.

@admin.register(EnglishIdentity)
class EnglishIdentityAdmin(admin.ModelAdmin):
    pass

@admin.register(ChineseIdentity)
class ChineseIdentityAdmin(admin.ModelAdmin):
    pass

class EnglishIdentityInline(admin.TabularInline):
    model = EnglishIdentity

class ChineseIdentityInline(admin.TabularInline):
    model = ChineseIdentity

@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    search_fields = (
        'english_name',
        'chinese_name'
    )
    # inlines = [
    #     EnglishIdentityInline,
    #     ChineseIdentityInline
    # ]

    exclude = [
        'mol_block',
        'mol',
        'bfp',
        'related_compounds',
        'mol_file',
        'mol_image',
        'chembls',

    ]

@admin.register(Herb)
class HerbAdmin(admin.ModelAdmin):
    filter_horizontal = ['compounds']
    search_fields = (
        'English_name',
        'Chinese_name'
    )
    exclude = ['related_herbs', 'compounds']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    search_fields = (
        'pinyin_name',
        'chinese_name'
    )

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    pass

@admin.register(ChEMBL)
class ChEMBLAdmin(admin.ModelAdmin):
    pass

# @admin.register()
