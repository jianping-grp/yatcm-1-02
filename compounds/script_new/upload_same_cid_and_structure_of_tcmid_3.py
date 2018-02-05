import os
import xlrd
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()

from compounds.models import *
from compounds.models import Compound_MS, TCMID_Herbs
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def upload_cid(line):
    tcmid_idx = line['idx']
    cid = int(line['cid'])
    ms_link = line['ms_link'].split('\n') if isinstance(line['ms_link'], unicode) else []
    herbs_info = line['herbs_info'].split('\n') if isinstance(line['herbs_info'], unicode) else []

    cid = CID.objects.get(cid=cid)
    compound = cid.compound
    for link in ms_link:
        ms, created = Compound_MS.objects.get_or_create(ms_link=link)
        ms.compound = compound
        ms.save()
    compound.tcmid_idx = tcmid_idx
    try:
        compound.save()
    except:
        print "The structure is not error"
    for herb in herbs_info:
        try:
            temp_list = herb.split(':')
            http_index = temp_list.index('http')
            English_name = ':'.join(temp_list[:http_index])
            tcmid_link = ':'.join(temp_list[http_index:])
            # tcmid_link = temp_list[1] + ':' + temp_list[2]
            tcmid_herb, created = TCMID_Herbs.objects.get_or_create(English_name=English_name, tcmid_link=tcmid_link)
            tcmid_herb.compounds.add(compound)
            tcmid_herb.save()
        except ValueError:
            print cid

def upload_structure(line):
    tcmid_idx = line['idx']
    structure = line['structure'].strip()
    cid_list = line['cid'].split('\n') if line['cid'] else []
    herbs_info = line['herbs_info'].split('\n') if isinstance(line['herbs_info'], unicode) else []
    ms_link = line['ms_link'].split('\n') if isinstance(line['ms_link'], unicode) else []
    Chinese_name = line['Chinese_name'] if isinstance(line['Chinese_name'], unicode) else None
    Chinese_synonym = line['Chinese_synonym'] if isinstance(line['Chinese_synonym'], unicode) else None
    English_name = line['English_name'] if isinstance(line['English_name'], unicode) else None
    English_synonym = line['English_synonym'] if isinstance(line['English_synonym'], unicode) else None

    try:
        compound = Compound.objects.get(smiles=structure)
    except ObjectDoesNotExist:
        compound = Compound.objects.get(chinese_name=Chinese_name, english_name=English_name)
    compound.tcmid_idx = tcmid_idx
    try:
        compound.save()
    except:
        print "The structure has error!!!"
    for cid in cid_list:
        cid_object, created = CID.objects.get_or_create(cid=cid)
        cid_object.compound = compound
        cid_object.save()
    for link in ms_link:
        ms, created = Compound_MS.objects.get_or_create(ms_link=link)
        ms.compound = compound
        ms.save()

    for herb in herbs_info:
        try:
            temp_list = herb.split(':')
            http_index = temp_list.index('http')
            English_name = ':'.join(temp_list[:http_index])
            tcmid_link = ':'.join(temp_list[http_index:])
            # tcmid_link = temp_list[1] + ':' + temp_list[2]
            tcmid_herb, created = TCMID_Herbs.objects.get_or_create(English_name=English_name, tcmid_link=tcmid_link)
            tcmid_herb.compounds.add(compound)
            tcmid_herb.save()
        except ValueError:
            print structure

if __name__ == '__main__':
    similar_cid_file = '/home/jianping/django_test/yatcm/compounds/data/same_cid.xlsx'
    similar_structure_file = '/home/jianping/django_test/yatcm/compounds/data/same_structure.xlsx'

    df_cid = pd.read_excel(similar_cid_file)
    df_structure = pd.read_excel(similar_structure_file)

    for idx, row in df_cid.iterrows():
        print idx
        upload_cid(row)
    for idx, row in df_structure.iterrows():
        print(idx)
        upload_structure(row)
    print 'Done!!!!'




    print 'Done!!!'