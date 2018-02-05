import csv
import os
from compounds import models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatcm.settings')
import django
django.setup()

def upload_pathway_cpd(file_path):
    with open(file_path) as f:
        for row in csv.reader(f):
            kegg_id, smiles = row
            print kegg_id
            cpd, created = models.KEGGCompound.objects.get_or_create(kegg_id=kegg_id)
            cpd.smiles = smiles
            cpd.save()


def upload_pathway(file_path):
    with open(file_path) as f:
        for row in csv.reader(f):
            name, pathway_id, cate0, cate1 = row
            pathway, created = models.KEGGPathway.objects.get_or_create(kegg_id=pathway_id)
            #if created:
            pathway.name = name
            kegg_cate0, create0 = models.KEGGPathwayCategory.objects.get_or_create(name=cate0)
            kegg_cate1, create1 = models.KEGGPathwayCategory.objects.get_or_create(name=cate1)
            kegg_cate1.category = kegg_cate0
            pathway.category = kegg_cate1
            kegg_cate0.save()
            kegg_cate1.save()
            pathway.save()

def upload_pathway_cpd_mapping(file_path):
    with open(file_path) as f:
        for row in csv.reader(f):
            pathway_id, cpd_id = row
            print pathway_id, cpd_id
            try:
                pathway = models.KEGGPathway.objects.get(kegg_id=pathway_id)
                cpd = models.KEGGCompound.objects.get(kegg_id=cpd_id)
            except:
                print 'error *****************', pathway_id
                continue
            if pathway in cpd.pathway.all():
                continue
            cpd.pathway.add(pathway)
            cpd.save()

def update_kegg_similarity_mapping():
    for cpd in models.KEGGCompound.objects.all():
        print cpd.id, cpd.kegg_id
        cpd.refresh_similarity_to_tcm()

def update_kegg_pathway_kgml():
    for pathway in models.KEGGPathway.objects.all():
        print pathway.id, pathway.kegg_id
        pathway.update_kegg_kgml()



def run():
    DATA_DIR = '/home/jianping/django_test/yatcm/compounds/scripts/data/'
    cpd_file = os.path.join(DATA_DIR, 'kegg_pathway_cpd.csv')
    pathway_file = os.path.join(DATA_DIR, 'kegg_pathway.csv')
    mapping_file = os.path.join(DATA_DIR, 'kegg_pathway_cpd_mapping.csv')
    upload_pathway_cpd(cpd_file)
    upload_pathway(pathway_file)
    upload_pathway_cpd_mapping(mapping_file)
    update_kegg_pathway_kgml()
    update_kegg_similarity_mapping()