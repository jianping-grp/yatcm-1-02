import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()
import pandas as pd
from compounds.models import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s-[%(message)s]",
    filename='/home/jianping/django_test/logs/compound_log.txt',
    filemode='w'
)
def extract_cids(cell):
    try:
        return [int(float(x)) for x in cell.split('\n')]
    except:
        return []

def herbs_extract(cell):
    try:
        cell = cell.replace("?", '').strip()
        herbs = cell.split('\n') if cell else []
        for herb in herbs:
            yield herb.split(';')
    except:
        yield []


def upload_compound(line):
    Chinese_name = line['Chinese_name'].strip() if isinstance(line['Chinese_name'], unicode) else None
    Chinese_synonym = line['Chinese_synonym'].split('\n') if isinstance(line['Chinese_synonym'], unicode) else []
    English_name = line['English_name'].strip() if isinstance(line['English_name'], unicode) else None
    English_synonym = line['English_synonym'].split('\n') if isinstance(line['English_synonym'], unicode) else []
    smiles = line['structure'].strip()
    herbs = herbs_extract(line['source'])
    cids = extract_cids(line['cid'])
    cass = line['CAS'].split('\n') if isinstance(line['CAS'], unicode) else []

    compound, created = Compound.objects.get_or_create(
        english_name=English_name,
        chinese_name=Chinese_name,
        smiles=smiles
    )

    for cn_identity in Chinese_synonym:
        chinese_identity, created = ChineseIdentity.objects.get_or_create(identity=cn_identity)
        chinese_identity.compound = compound
        chinese_identity.save()

    for en_identity in English_synonym:
        english_identity, created = EnglishIdentity.objects.get_or_create(identity=en_identity)
        english_identity.compound = compound
        english_identity.save()

    for cid in cids:
        try:
            c, created = CID.objects.get_or_create(cid=cid)
            c.compound = compound
            c.save()
        except CID.DoesNotExist:
            logging.warning("{} Does not find in the CID database".format(cid))
        except CID.MultipleObjectsReturned:
            logging.warning("{} find multiple cid objs in database".format(cid))

    for cas in cass:
        try:
            ca, created = CAS.objects.get_or_create(cas=cas)
            ca.compound = compound
            ca.save()
        except CAS.DoesNotExist:
            logging.warning("{} Does not find in the CAS database".format(cas))
        except CAS.MultipleObjectsReturned:
            logging.warning("{} find multiple cas objs in database".format(cas))

    for herb in herbs:
        try:
            # h, created = Herb.objects.get_or_create(Chinese_name=herb[0], English_name=herb[1])
            h = Herb.objects.get(Chinese_name=herb[0], English_name=herb[1])
            h.compounds.add(compound)
            h.save()
        except Herb.DoesNotExist:
            logging.info("Can not find %s, %s in databasecuo" % (herb[0], herb[1]))
        except Herb.MultipleObjectsReturned:
            logging.info("return multiple herbs %s, %s" % (herb[0], herb[1]))
        except IndexError:
            print('Not exist this herb')

if __name__ == '__main__':
    compound_file = '/home/jianping/django_test/yatcm/compounds/data/34680.xlsx'
    df = pd.read_excel(compound_file)
    for idx, row in df.iterrows():
        print(idx)
        upload_compound(row)

