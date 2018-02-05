import csv
import os
from compounds import models


def upload_sea_pred(sea_file):
    with open(sea_file) as f:
        for row in csv.reader(f):
            chembl_id, cpd_id = row
            print row
            chembl_target, created_chembl_cpd = models.CHEMBLTarget.objects.get_or_create(chembl_id=chembl_id)
            cpd = models.Compound.objects.get(id=int(cpd_id))
            if chembl_target in cpd.related_ChEMBL_targets.all():
                continue
            cpd.related_ChEMBL_targets.add(chembl_target)
            chembl_target.save()
            cpd.save()


def run():
    sea_file = '/home/jianping/django_test/yatcm/compounds/scripts/data/yatcm-sea-pred.csv'
    upload_sea_pred(sea_file)
