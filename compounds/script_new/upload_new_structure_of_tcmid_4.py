import os
import xlrd
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()
from compounds.models import *
from compounds.models import TCMID_Herbs, Compound_MS

def upload_new_compound(line):
    tcmid_idx = int(line['idx'])
    smile = line['structure'].strip() if isinstance(line['structure'], unicode) else None
    cid_list = line['cid'].split('\n') if isinstance(line['cid'], unicode) else None
    herb_list = line['herbs_info'] if isinstance(line['herbs_info'], unicode) else []
    ms_link = line['ms_link'] if isinstance(line['ms_link'], unicode) else []


    # compound = Compound.objects.get(smiles=smile)
    compound, created = Compound.objects.get_or_create(smiles=smile)
    compound.tcmid_idx = tcmid_idx
    compound.save()
    for cid in cid_list:
        cid_object, created = CID.objects.get_or_create(cid=int(cid))
        cid_object.compound = compound
        cid_object.save()

    for herb in herb_list:
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
            print

    for link in ms_link:
        link_object, created = Compound_MS.objects.get_or_create(ms_link=link)
        link_object.compound = compound
        link_object.save()

if __name__ == '__main__':
    compound_file = '/home/jianping/django_test/yatcm/compounds/data/rm_same_cid_structure.xlsx'
    df = pd.read_excel(compound_file)
    for idx, row in df.iterrows():
        print(idx)
        upload_new_compound(row)

