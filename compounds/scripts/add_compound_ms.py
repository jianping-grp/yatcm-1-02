import os
import xlrd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()

from compounds.models import *
from compounds.models import Compound_MS, TCMID_Herbs
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def upload_cid_ms(row_number):
    print row_number
    row = table_cid.row_values(row_number)
    tcmid_idx = int(row[0])
    cid = int(row[2].strip())
    ms_link = row[5].split('\n') if row[5] else []
    herbs_info = row[4].split('\n') if row[5] else []

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

def upload_structure_ms(row_number):
    print row_number
    row = table_structure.row_values(row_number)
    tcmid_idx = row[4]
    structure = row[0].strip()
    cid_list = row[1].split('\n') if row[1] else []
    herbs_info = row[2].split('\n') if row[2] else []
    ms_link = row[3].split('\n') if row[3] else []
    Chinese_name = row[5].strip()
    Chinese_synonym = row[6].strip()
    English_name = row[7].strip()
    English_synonym = row[8].strip()


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
    similar_cid_file = '/home/jianping/data/merged/data_base_result/new_hanle_source/remend/tcmid/similar_cid.xlsx'
    similar_structure_file = '/home/jianping/data/merged/data_base_result/new_hanle_source/remend/tcmid/similar_structure.xlsx'

    table_cid = xlrd.open_workbook(similar_cid_file).sheet_by_index(0)
    table_structure = xlrd.open_workbook(similar_structure_file).sheet_by_index(0)

    nrows_cid = table_cid.nrows
    nrows_structure = table_structure.nrows


    # map(upload_cid_ms, range(1, nrows_cid))
    map(upload_structure_ms, range(1, nrows_structure))
    print 'Done!!!'